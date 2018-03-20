# -*- coding: utf-8 -*-

"""
@author: curry
@software: Pycharm
@file: Bi_LSTM_CRF_Character.py
@time: 2018/3/14
@description: 只有词的lstm
"""
from keras.models import Model
from keras.layers import Input, Embedding, Bidirectional, LSTM, Dropout, \
    TimeDistributed, Concatenate, Dense, GRU, Conv1D, \
    LeakyReLU
from keras.layers.normalization import BatchNormalization
from  LSTM.crf_layer import CRF


class BiLSTM_CRF():
    """
    两输入：main_input(字序列), auxiliary_input(对应的相同timestep的词序列)
    单输出：char_wise IOB label
    """

    def __init__(self, n_input_char, char_embedding_mat, n_input_word,
                 keep_prob, n_lstm, keep_prob_lstm, n_entity,
                 optimizer, batch_size, epochs, word_embedding_mat=None,
                 n_filter=None, kernel_size=None, ):
        self.n_input_word = n_input_word
        self.word_embedding_mat = word_embedding_mat
        self.n_vocab_word = word_embedding_mat.shape[0]
        self.n_embed_word = word_embedding_mat.shape[1]
        self.keep_prob = keep_prob
        self.n_lstm = n_lstm
        self.keep_prob_lstm = keep_prob_lstm

        self.n_entity = n_entity
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.epochs = epochs

        self.build()

    def build(self):
        word_input = Input(shape=(self.n_input_word,), name='auxiliary_input')
        word_embed = Embedding(input_dim=self.n_vocab_word,
                               output_dim=self.n_embed_word,
                               weights=[self.word_embedding_mat],
                               input_length=self.n_input_word,
                               mask_zero=True,
                               trainable=True)(word_input)
        word_embed_drop = Dropout(self.keep_prob)(word_embed)
        blstm = Bidirectional(GRU(self.n_lstm, return_sequences=True,
                                  dropout=self.keep_prob_lstm,
                                  recurrent_dropout=self.keep_prob_lstm)
                              )(word_embed_drop)
        time_drop = TimeDistributed(Dropout(self.keep_prob))(blstm)

        crf = CRF(units=self.n_entity, learn_mode='join',
                  test_mode='viterbi', sparse_target=False)
        output = crf(time_drop)
        self.model = Model(inputs=word_input, outputs=output, )

        self.model.compile(optimizer=self.optimizer,
                           loss=crf.loss_function,
                           metrics=[crf.accuracy])

    def train(self, X_train, y_train, X_dev, y_dev, cb):
        self.model.fit(X_train, y_train, batch_size=self.batch_size,
                       epochs=self.epochs, validation_data=(X_dev, y_dev),
                       callbacks=cb)
