# coding=utf-8
import numpy as np
from bilstm_crf import BiLSTM_CRF
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau,\
                            TensorBoard
import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

char_embedding_mat = np.load('data/char_embedding_matrix.npy')

X=np.load('data/train.npy')
y=np.load('data/y.npy')

X_train=X[:600]
y_train=y[:600]






# ner_model = BiLSTM_CRF(n_input=200, n_vocab=char_embedding_mat.shape[0],
#                        n_embed=100, embedding_mat=char_embedding_mat,
#                        keep_prob=0.5, n_lstm=100, keep_prob_lstm=0.8,
#                        n_entity=7, optimizer='adam', batch_size=64, epochs=500)
ner_model = BiLSTM_CRF(n_input=300, n_vocab=char_embedding_mat.shape[0],
                       n_embed=100, embedding_mat=char_embedding_mat,
                       keep_prob=0.5, n_lstm=256, keep_prob_lstm=0.6,
                       n_entity=3, optimizer='adam', batch_size=16, epochs=500)

cp_folder, cp_file = 'checkpoints', 'bilstm_crf_weights_best_attention.hdf5'
log_filepath = 'logs/bilstm_crf_summaries'

cb = [ModelCheckpoint(os.path.join(cp_folder, cp_file), monitor='val_loss',
                      verbose=1, save_best_only=True, save_weights_only=True, mode='min'),
      EarlyStopping(min_delta=1e-8, patience=10, mode='min'),
      ReduceLROnPlateau(factor=0.2, patience=6, verbose=0, mode='min',
                        epsilon=1e-6, cooldown=4, min_lr=1e-8),
      TensorBoard(log_dir=log_filepath, write_graph=True, write_images=True,
                  histogram_freq=1)]





ner_model.train_attention(X_train, y_train,  cb)
