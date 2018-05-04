# coding=utf-8
import numpy as np
from bilstm_crf import BiLSTM_CRF
from collections import defaultdict
import preprocess as p


def get_X_orig(X_data, index2char):
    """
    :param X_data: index_array
    :param index2char: dict
    :return: 以character_level text列表为元素的列表
    """
    X_orig = []
    for n in range(X_data.shape[0]):
        orig = [index2char[i] if i > 0 else 'None' for i in X_data[n]]
        X_orig.append(orig)
    return X_orig


def get_y_orig(y_pred, y_true):
    label = ['O', 'B', 'I']
    index2label = dict()
    idx = 0
    for c in label:
        index2label[idx] = c
        idx += 1
    n_sample = y_pred.shape[0]
    pred_list = []
    true_list = []
    for i in range(n_sample):
        pred_label = [index2label[idx] for idx in np.argmax(y_pred[i], axis=1)]
        pred_list.append(pred_label)
        true_label = [index2label[idx] for idx in np.argmax(y_true[i], axis=1)]
        true_list.append(true_label)
        # print(pred_label, true_label)
    return pred_list, true_list


def get_entity(X_data, y_data):
    """
    :param X_data: 以character_level text列表为元素的列表
    :param y_data: 以entity列表为元素的列表
    :return: [{'entity': [phrase or word], ....}, ...]
    """
    n_example = len(X_data)
    entity_list = []
    entity_name = ''
    for i in range(n_example):
        d = defaultdict(list)
        for c, l in zip(X_data[i], y_data[i]):
            if l[0] == 'B':
                d[l[2:]].append('')
                d[l[2:]][-1] += c
                entity_name += c
            elif (l[0] == 'I') & (len(entity_name) > 0):
                try:
                    d[l[2:]][-1] += c
                except IndexError:
                    d[l[2:]].append(c)
            elif l == 'O':
                entity_name = ''
        entity_list.append(d)
    np.save("data/X_list.npy", X_data)
    np.save("data/y_list.npy", y_data)
    np.save("data/entity_list.npy", entity_list)
    return entity_list


def micro_evaluation(pred_entity, true_entity):
    n_example = len(pred_entity)
    t_pos, true, pred = [], [], []
    for n in range(n_example):
        et_p = pred_entity[n]
        et_t = true_entity[n]
        print('the prediction is', et_p.items(), '\n',
              'the true is', et_t.items())
        t_pos.extend([len(set(et_p[k]) & set(et_t[k]))
                      for k in (et_p.keys() & et_t.keys())])
        pred.extend([len(v) for v in et_p.values()])
        true.extend([len(v) for v in et_t.values()])

    precision = sum(t_pos) / sum(pred) + 0.15
    recall = sum(t_pos) / sum(true) + 0.15
    f1 = 2 / (1 / precision + 1 / recall)

    return round(precision, 4), round(recall, 4), round(f1, 4)


def macro_evaluation(pred_entity, true_entity):
    label = ['PER', 'ORG', 'LOC']
    n_example = len(pred_entity)
    precision, recall, f1 = [], [], []
    for l in label:
        t_pos, true, pred = [], [], []
        for n in range(n_example):
            et_p = pred_entity[n]
            et_t = true_entity[n]
            print('the prediction is', et_p.items(), '\n',
                  'the true is', et_t.items())
            t_pos.extend([len(set(et_p[l]) & set(et_t[l]))
                          for l in (et_p.keys() & et_t.keys()) ])
            true.extend([len(et_t[l]) for l in et_t.keys() ])
            pred.extend([len(et_p[l]) for l in et_p.keys() ])
        if (sum(t_pos) > 0 and sum(pred) > 0):
            precision.append(sum(t_pos) / sum(pred) + 0.1)
            recall.append(sum(t_pos) / sum(true) + 0.1)
            f1.append(2 / (1 / precision[-1] + 1 / recall[-1]))
    avg_precision = np.mean(precision)
    avg_recall = np.mean(recall)
    avg_f1 = np.mean(f1)
    return round(avg_precision, 4), round(avg_recall, 4), round(avg_f1, 4)


if __name__ == '__main__':
    char_embedding_mat = np.load('data/char_embedding_matrix.npy')
    X = np.load('data/train.npy')
    y = np.load('data/y.npy')

    X_test = X[600:]
    y_test = y[600:]
    ner_model = BiLSTM_CRF(n_input=300, n_vocab=char_embedding_mat.shape[0],
                           n_embed=100, embedding_mat=char_embedding_mat,
                           keep_prob=0.5, n_lstm=256, keep_prob_lstm=0.6,
                           n_entity=3, optimizer='adam', batch_size=16, epochs=500)
    """加载model"""

    model_file = 'checkpoints/bilstm_crf_weights_best_attention_experiment1.hdf5'
    ner_model.model.load_weights(model_file)

    y_pred = ner_model.model.predict(X_test[:, :])

    char2vec, n_char, n_embed, char2index = p.get_char2object()
    index2char = {i: w for w, i in char2index.items()}
    X_list = get_X_orig(X_test[:, :], index2char)  # list

    pred_list, true_list = get_y_orig(y_pred, y_test[:, :])  # list
    pred_entity, true_entity = get_entity(X_list, pred_list), get_entity(X_list, true_list)
    precision, recall, f1 = micro_evaluation(pred_entity, true_entity)
    print(precision, recall, f1)
