# coding=utf-8
from keras.models import Model
from keras.layers import Input, Embedding, Bidirectional, LSTM, Dropout, \
    TimeDistributed, Concatenate, Dense, GRU, Conv1D, \
    LeakyReLU, MaxPooling1D, Flatten, concatenate
from keras.layers.normalization import BatchNormalization
from crf_layer import CRF
from keras.layers.core import *
from keras.layers.recurrent import LSTM
from keras.models import *
from keras.layers import merge


class BiLSTM_CRF():
    """
    两输入：main_input(字序列), auxiliary_input(对应的相同timestep的词序列)
    单输出：char_wise IOB label
    """

    def __init__(self, n_input_char, char_embedding_mat, n_input_word,
                 keep_prob, n_lstm, keep_prob_lstm, n_entity,
                 optimizer, batch_size, epochs, word_embedding_mat=None,
                 n_filter=None, kernel_size=None):
        self.n_input_char = n_input_char
        self.char_embedding_mat = char_embedding_mat
        self.n_vocab_char = char_embedding_mat.shape[0]
        self.n_embed_char = char_embedding_mat.shape[1]
        self.n_input_word = n_input_word
        self.word_embedding_mat = word_embedding_mat
        self.n_vocab_word = word_embedding_mat.shape[0]
        self.n_embed_word = word_embedding_mat.shape[1]
        self.keep_prob = keep_prob
        self.n_lstm = n_lstm
        self.keep_prob_lstm = keep_prob_lstm
        self.n_filter = n_filter
        self.kernel_size = kernel_size

        self.n_entity = n_entity
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.epochs = epochs

        # self.build_simple()
        # self.build()
        self.build2()
        # self.build3()
        # self.build4()
        # self.build_attention()

    def attention_3d_block(self, inputs):
        # if True, the attention vector is shared across the input_dimensions where the attention is applied.
        SINGLE_ATTENTION_VECTOR = False
        APPLY_ATTENTION_BEFORE_LSTM = False
        # inputs.shape = (batch_size, time_steps, input_dim)
        input_dim = int(inputs.shape[2])
        time_steps = int(inputs.shape[1])
        a = Permute((2, 1))(inputs)
        # a = Reshape((input_dim, ))(a)  # this line is not useful. It's just to know which dimension is what.
        a = Dense(time_steps, activation='softmax')(a)
        if SINGLE_ATTENTION_VECTOR:
            a = Lambda(lambda x: K.mean(x, axis=1), name='dim_reduction')(a)
            a = RepeatVector(input_dim)(a)
        a_probs = Permute((2, 1), name='attention_vec')(a)
        output_attention_mul = merge([inputs, a_probs], name='attention_mul', mode='mul')
        return output_attention_mul

    def build_simple(self):
        # main
        char_input = Input(shape=(self.n_input_char,), name='main_input')
        char_embed = Embedding(input_dim=self.n_vocab_char,
                               output_dim=self.n_embed_char,
                               weights=[self.char_embedding_mat],
                               input_length=self.n_input_char,
                               mask_zero=True,
                               trainable=False)(char_input)
        char_embed_drop = Dropout(self.keep_prob)(char_embed)
        # auxiliary
        word_input = Input(shape=(self.n_input_word,), name='auxiliary_input')
        word_embed = Embedding(input_dim=self.n_vocab_word,
                               output_dim=self.n_embed_word,
                               weights=[self.word_embedding_mat],
                               input_length=self.n_input_word,
                               mask_zero=True,
                               trainable=False)(word_input)
        word_embed_drop = Dropout(self.keep_prob)(word_embed)
        # concatenation
        concat = Concatenate(axis=-1)([char_embed_drop, word_embed_drop])
        concat_drop = TimeDistributed(Dropout(self.keep_prob))(concat)
        blstm = Bidirectional(LSTM(self.n_lstm, return_sequences=True,
                                   dropout=self.keep_prob_lstm,
                                   recurrent_dropout=self.keep_prob_lstm))(concat_drop)

        crf = CRF(units=self.n_entity, learn_mode='join',
                  test_mode='viterbi', sparse_target=False)
        output = crf(blstm)

        self.model_simple = Model(inputs=[char_input, word_input],
                                  outputs=output)
        self.model_simple.compile(optimizer=self.optimizer,
                                  loss=crf.loss_function,
                                  metrics=[crf.accuracy])
        print(self.model_simple.summary())

    def build(self):
        # main
        char_input = Input(shape=(self.n_input_char,), name='main_input')
        char_embed = Embedding(input_dim=self.n_vocab_char,
                               output_dim=self.n_embed_char,
                               weights=[self.char_embedding_mat],
                               input_length=self.n_input_char,
                               mask_zero=True,
                               trainable=False)(char_input)
        char_embed_drop = Dropout(self.keep_prob)(char_embed)
        bilstm = Bidirectional(GRU(self.n_lstm, return_sequences=True,
                                   dropout=self.keep_prob_lstm,
                                   recurrent_dropout=self.keep_prob_lstm)
                               )(char_embed_drop)
        # auxiliary
        word_input = Input(shape=(self.n_input_word,), name='auxiliary_input')
        word_embed = Embedding(input_dim=self.n_vocab_word,
                               output_dim=self.n_embed_word,
                               weights=[self.word_embedding_mat],
                               input_length=self.n_input_word,
                               mask_zero=True,
                               trainable=False)(word_input)
        word_embed_drop = Dropout(self.keep_prob)(word_embed)
        lstm = Bidirectional(GRU(self.n_lstm, return_sequences=True,
                                 dropout=self.keep_prob_lstm,
                                 recurrent_dropout=self.keep_prob_lstm)
                             )(word_embed_drop)

        # concatenation
        concat = Concatenate(axis=-1)([bilstm, lstm])
        concat_drop = TimeDistributed(Dropout(self.keep_prob))(concat)

        # crf = CRF(units=self.n_entity, learn_mode='join',
        #           test_mode='viterbi', sparse_target=False)
        # output = crf(concat_drop)
        output = TimeDistributed(Dense(self.n_entity, activation='softmax'))(concat_drop)
        # crf = CRF(units=self.n_entity, learn_mode='join',
        #       test_mode='viterbi', sparse_target=False)
        # output = crf(bilstm)
        #

        self.model = Model(inputs=[char_input, word_input],
                           outputs=output)
        self.model.compile(optimizer=self.optimizer,
                           loss='categorical_crossentropy', metrics=['accuracy'])
        print(self.model.summary())

    def build2(self):
        # main
        char_input = Input(shape=(self.n_input_char,))
        char_embed = Embedding(input_dim=self.n_vocab_char,
                               output_dim=self.n_embed_char,
                               input_length=self.n_input_char,
                               weights=[self.char_embedding_mat],
                               mask_zero=False,
                               trainable=False)(char_input)
        char_embed_drop = Dropout(self.keep_prob)(char_embed)

        # # #attention
        # attention_probs = Dense(int(char_embed_drop.shape[2]), activation='softmax', name='attention_vec')(
        #     char_embed_drop)
        # attention_mul = merge([char_embed_drop, attention_probs], name='attention_mul', mode='mul')

        # auxiliary
        word_input = Input(shape=(self.n_input_word,))
        word_embed = Embedding(input_dim=self.n_vocab_word,
                               output_dim=self.n_embed_word,
                               input_length=self.n_input_word,
                               weights=[self.word_embedding_mat],
                               mask_zero=False,
                               trainable=False)(word_input)
        word_embed_drop = Dropout(self.keep_prob)(word_embed)
        # 使用CNN提取word的n_gram特征
        word_conv = Conv1D(self.n_filter, kernel_size=self.kernel_size,
                           strides=1, padding='same',
                           kernel_initializer='he_normal')(word_embed_drop)
        word_conv = BatchNormalization(axis=-1)(word_conv)
        word_conv = LeakyReLU(alpha=1 / 5.5)(word_conv)

        # concatenation
        concat = Concatenate(axis=-1)([char_embed_drop, word_conv])
        concat_drop = TimeDistributed(Dropout(self.keep_prob))(concat)
        #

        bilstm = Bidirectional(GRU(units=self.n_lstm,
                                   return_sequences=True,
                                   dropout=self.keep_prob_lstm,
                                   recurrent_dropout=self.keep_prob_lstm)
                               )(concat_drop)
        crf = CRF(units=self.n_entity, learn_mode='join',
                  test_mode='viterbi', sparse_target=False)
        output = crf(bilstm)
        #
        self.model2 = Model(inputs=[char_input, word_input],
                            outputs=output)
        self.model2.compile(optimizer=self.optimizer,
                            loss=crf.loss_function, metrics=[crf.accuracy])

        print(self.model2.summary())

    def build_char_cnn_word_rnn(self):
        # main
        char_input = Input(shape=(self.n_input_char,), name='main_input')
        char_embed = Embedding(input_dim=self.n_vocab_char,
                               output_dim=self.n_embed_char,
                               weights=[self.char_embedding_mat],
                               input_length=self.n_input_char,
                               mask_zero=False,
                               trainable=True)(char_input)
        char_embed_drop = Dropout(self.keep_prob)(char_embed)
        char_conv = Conv1D(self.n_filter, kernel_size=self.kernel_size,
                           strides=1, padding='same',
                           kernel_initializer='he_normal')(char_embed_drop)
        char_conv = BatchNormalization(axis=-1)(char_conv)
        char_conv = LeakyReLU(alpha=1 / 5.5)(char_conv)

        # auxiliary
        word_input = Input(shape=(self.n_input_word,))
        word_embed = Embedding(input_dim=self.n_vocab_word,
                               output_dim=self.n_embed_word,
                               input_length=self.n_input_word,
                               weights=[self.word_embedding_mat],
                               mask_zero=True,
                               trainable=True)(word_input)
        word_embed_drop = Dropout(self.keep_prob)(word_embed)
        bilstm = Bidirectional(GRU(self.n_lstm, return_sequences=True,
                                   dropout=self.keep_prob_lstm,
                                   recurrent_dropout=self.keep_prob_lstm)
                               )(word_embed_drop)
        # concatenation
        concat = Concatenate(axis=-1)([char_conv, bilstm])
        concat_drop = TimeDistributed(Dropout(self.keep_prob))(concat)

        crf = CRF(units=self.n_entity, learn_mode='join',
                  test_mode='viterbi', sparse_target=False)
        output = crf(concat_drop)
        self.model_char_cnn_word_rnn = Model(inputs=[char_input, word_input],
                                             outputs=output)
        self.model_char_cnn_word_rnn.compile(optimizer=self.optimizer,
                                             loss=crf.loss_function,
                                             metrics=[crf.accuracy])
        print(self.model_char_cnn_word_rnn.summary())

    def build3(self):
        # main
        char_input = Input(shape=(self.n_input_char,), name='main_input')
        char_embed = Embedding(input_dim=self.n_vocab_char,
                               output_dim=self.n_embed_char,
                               weights=[self.char_embedding_mat],
                               input_length=self.n_input_char,
                               mask_zero=True,
                               trainable=True)(char_input)
        char_embed_drop = Dropout(self.keep_prob)(char_embed)
        bilstm = Bidirectional(GRU(self.n_lstm, return_sequences=True,
                                   dropout=self.keep_prob_lstm,
                                   recurrent_dropout=self.keep_prob_lstm)
                               )(char_embed_drop)

        # auxiliary
        word_input = Input(shape=(self.n_input_word,))
        word_embed = Embedding(input_dim=self.n_vocab_word,
                               output_dim=self.n_embed_word,
                               input_length=self.n_input_word,
                               weights=[self.word_embedding_mat],
                               mask_zero=False,
                               trainable=True)(word_input)
        word_embed_drop = Dropout(self.keep_prob)(word_embed)
        # 使用CNN提取word的n_gram特征
        word_conv = Conv1D(self.n_filter, kernel_size=self.kernel_size,
                           strides=1, padding='same',
                           kernel_initializer='he_normal')(word_embed_drop)
        word_conv = BatchNormalization(axis=-1)(word_conv)
        word_conv = LeakyReLU(alpha=1 / 5.5)(word_conv)
        # concatenation
        concat = Concatenate(axis=-1)([bilstm, word_conv])
        concat_drop = TimeDistributed(Dropout(self.keep_prob))(concat)

        crf = CRF(units=self.n_entity, learn_mode='join',
                  test_mode='viterbi', sparse_target=False)
        output = crf(concat_drop)
        self.model3 = Model(inputs=[char_input, word_input],
                            outputs=output)
        self.model3.compile(optimizer=self.optimizer,
                            loss=crf.loss_function,
                            metrics=[crf.accuracy])

    def build4(self):
        char_input = Input(shape=(self.n_input_char,), name='main_input')
        char_embed = Embedding(input_dim=self.n_vocab_char,
                               output_dim=self.n_embed_char,
                               weights=[self.char_embedding_mat],
                               input_length=self.n_input_char,
                               mask_zero=False,
                               trainable=True)(char_input)
        char_embed_drop = Dropout(self.keep_prob)(char_embed)
        # 使用cnn提取字符级特征
        char_conv = Conv1D(filters=self.n_filter, kernel_size=self.kernel_size, strides=1, padding='same',
                           kernel_initializer='he_normal')(char_embed_drop)
        char_conv = BatchNormalization(axis=-1)(char_conv)
        char_conv = LeakyReLU(alpha=1 / 5.5)(char_conv)
        # char_pool = MaxPooling1D(self.pool_size)(char_conv)
        # char_flaten = Flatten()(char_pool)
        # auxiliary
        word_input = Input(shape=(self.n_input_word,), name='auxiliary_input')
        word_embed = Embedding(input_dim=self.n_vocab_word,
                               output_dim=self.n_embed_word,
                               weights=[self.word_embedding_mat],
                               input_length=self.n_input_word,
                               mask_zero=True,
                               trainable=True)(word_input)
        word_embed_drop = Dropout(self.keep_prob)(word_embed)

        # concatentation
        concat = concatenate([char_conv, word_embed_drop])
        concat_drop = TimeDistributed(Dropout(self.keep_prob))(concat)

        lstm = Bidirectional(GRU(self.n_lstm, return_sequences=True,
                                 dropout=self.keep_prob_lstm,
                                 recurrent_dropout=self.keep_prob_lstm)
                             )(concat_drop)

        crf = CRF(units=self.n_entity, learn_mode='join',
                  test_mode='viterbi', sparse_target=False)
        output = crf(lstm)
        self.model4 = Model(inputs=[char_input, word_input],
                            outputs=output)
        self.model4.compile(optimizer=self.optimizer,
                            loss=crf.loss_function,
                            metrics=[crf.accuracy])

    def build_attention(self):
        # main
        char_input = Input(shape=(self.n_input_char,))

        char_embed = Embedding(input_dim=self.n_vocab_char,
                               output_dim=self.n_embed_char,
                               input_length=self.n_input_char,
                               weights=[self.char_embedding_mat],
                               mask_zero=False,
                               trainable=True)(char_input)
        char_embed_drop = Dropout(self.keep_prob)(char_embed)
        # auxiliary
        word_input = Input(shape=(self.n_input_word,))
        word_embed = Embedding(input_dim=self.n_vocab_word,
                               output_dim=self.n_embed_word,
                               input_length=self.n_input_word,
                               weights=[self.word_embedding_mat],
                               mask_zero=False,
                               trainable=True)(word_input)
        word_embed_drop = Dropout(self.keep_prob)(word_embed)
        # 使用CNN提取word的n_gram特征
        word_conv = Conv1D(self.n_filter, kernel_size=self.kernel_size,
                           strides=1, padding='same',
                           kernel_initializer='he_normal')(word_embed_drop)
        word_conv = BatchNormalization(axis=-1)(word_conv)
        word_conv = LeakyReLU(alpha=1 / 5.5)(word_conv)
        # concatenation
        concat = Concatenate(axis=-1)([char_embed_drop, word_conv])
        concat_drop = TimeDistributed(Dropout(self.keep_prob))(concat)

        # attention = self.attention_3d_block(concat_drop)
        # attention_drop = TimeDistributed(Dropout(self.keep_prob))(attention)

        bilstm = Bidirectional(LSTM(units=self.n_lstm,
                                    return_sequences=True,
                                    dropout=self.keep_prob_lstm,
                                    recurrent_dropout=self.keep_prob_lstm)
                               )(concat_drop)

        crf = CRF(units=self.n_entity, learn_mode='join',
                  test_mode='viterbi', sparse_target=False)
        output = crf(bilstm)

        self.model_attention = Model(inputs=[char_input, word_input],
                                     outputs=output)
        self.model_attention.compile(optimizer=self.optimizer,
                                     loss=crf.loss_function,
                                     metrics=[crf.accuracy])

    def train_simple(self, X_train, y_train, X_dev, y_dev, cb):
        self.model_simple.fit(X_train, y_train, batch_size=self.batch_size,
                              epochs=self.epochs, validation_split=0.3,
                              callbacks=cb)
        self.model_simple.save('checkpoints/model.hdf5')

    def train(self, X_train, y_train, X_dev, y_dev, cb):
        self.model.fit(X_train, y_train, batch_size=self.batch_size,
                       epochs=self.epochs, validation_split=0.3,
                       callbacks=cb)

    def train2(self, X_train, y_train,  cb):
        self.model2.fit(X_train, y_train, batch_size=self.batch_size,
                        epochs=self.epochs, validation_split=0.1,
                        callbacks=cb)

    def train3(self, X_train, y_train, X_dev, y_dev, cb):
        self.model3.fit(X_train, y_train, batch_size=self.batch_size,
                        epochs=self.epochs, validation_data=(X_dev, y_dev),
                        callbacks=cb)

    def train4(self, X_train, y_train, X_dev, y_dev, cb):
        self.model4.fit(X_train, y_train, batch_size=self.batch_size,
                        epochs=self.epochs, validation_data=(X_dev, y_dev),
                        callbacks=cb)

    def train_attention(self, X_train, y_train, X_dev, y_dev, cb):
        self.model_attention.fit(X_train, y_train, batch_size=self.batch_size,
                                 epochs=self.epochs, validation_data=(X_dev, y_dev),
                                 callbacks=cb)

    def train_char_cnn_word_rnn(self, X_train, y_train, cb):
        self.model_char_cnn_word_rnn.fit(X_train, y_train, batch_size=self.batch_size,
                                         epochs=self.epochs, validation_split=0.2,
                                         callbacks=cb)
