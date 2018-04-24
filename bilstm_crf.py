# coding=utf-8
from keras.models import Sequential
from keras.layers import Masking, Embedding, Bidirectional, LSTM, Dropout,\
                         TimeDistributed, GRU
from crf_layer import CRF
from keras.models import *
from keras.layers.core import *
from keras.layers import merge
from keras.utils.vis_utils import plot_model

class BiLSTM_CRF():
    def __init__(self, n_input, n_vocab, n_embed, embedding_mat, keep_prob,
                 n_lstm, keep_prob_lstm, n_entity, optimizer, batch_size,
                 epochs):
        self.n_input = n_input
        self.n_vocab = n_vocab
        self.n_embed = n_embed
        self.embedding_mat = embedding_mat
        self.keep_prob = keep_prob
        self.n_lstm = n_lstm
        self.keep_prob_lstm = keep_prob_lstm
        self.n_entity = n_entity
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.epochs = epochs
        self.build()



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

    def build(self):
        self.model = Sequential()

        self.model.add(Embedding(input_dim=self.n_vocab,
                                 output_dim=self.n_embed,
                                 input_length=self.n_input,
                                 weights=[self.embedding_mat],
                                 mask_zero=True,
                                 trainable=True))
        self.model.add(Dropout(self.keep_prob))

        self.model.add(Bidirectional( GRU(self.n_lstm, return_sequences=True,
                                           dropout=self.keep_prob_lstm,
                                           recurrent_dropout=self.keep_prob_lstm)
                                     ))
        self.model.add(TimeDistributed(Dropout(self.keep_prob)))

        # crf = CRF(units=self.n_entity, learn_mode='join',
        #           test_mode='viterbi', sparse_target=False)
        crf=CRF(units=self.n_entity,learn_mode='join',
                    test_mode='viterbi',sparse_target=False)
        self.model.add(crf)

        self.model.compile(optimizer=self.optimizer,
                           loss=crf.loss_function,
                           metrics=[crf.accuracy])
        print((self.model.summary()))
        plot_model(self.model,to_file="model_png/character_model.png",show_shapes=False)


    def build_attention(self):
        char_input = Input(shape=(self.n_input,), name='main_input')
        char_embed = Embedding(input_dim=self.n_vocab,
                                 output_dim=self.n_embed,
                                 input_length=self.n_input,
                                 weights=[self.embedding_mat],
                                 mask_zero=False,
                                 trainable=True)(char_input)
        char_drop=Dropout(self.keep_prob)(char_embed)
        # attention
        attention_probs = Dense(int(char_drop.shape[2]), activation='softmax', name='attention_vec')(char_drop)
        attention_mul = merge([char_drop, attention_probs], output_shape=32, name='attention_mul', mode='mul')
        blstm=Bidirectional(LSTM(self.n_lstm, return_sequences=True,
                                           dropout=self.keep_prob_lstm,
                                           recurrent_dropout=self.keep_prob_lstm))(attention_mul)

        crf = CRF(units=self.n_entity, learn_mode='join',
                  test_mode='viterbi', sparse_target=False)

        output=crf(blstm)

        self.model_attention = Model(inputs=[char_input],
                            outputs=output)

        self.model_attention.compile(optimizer=self.optimizer,
                           loss=crf.loss_function,
                           metrics=[crf.accuracy])
        print(self.model_attention.summary())
        print((self.model_attention.summary()))
        plot_model(self.model_attention, to_file="model_png/character_model_attention.png", show_shapes=False)

    def train(self, X_train, y_train, cb):
        self.model.fit(X_train, y_train, batch_size=self.batch_size,
                       epochs=self.epochs,validation_split=0.1,
                       callbacks=cb)

    def train_attention(self, X_train, y_train,  cb):
        self.model_attention.fit(X_train, y_train, batch_size=self.batch_size,
                       epochs=self.epochs, validation_split=0.1,
                       callbacks=cb)