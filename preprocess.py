# coding = utf-8
import numpy as np
import os
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
import random
from utils import *

embedding_file = 'data/char_embedding_matrix.npy'


def get_char_tag_data(file_path):
    """
    获取字符 和对应的标签
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as f:
        list_all = f.readlines()  # type: list
    # print(list_all, len(list_all))
    # ['本 O\n', '性 O\n', '的 O\n', '差 O\n', '别 O\n', '。 O\n', '\n'] 112188
    i = 0
    char_str = str()
    char_list = []  # 列表中每个元素为每句话组成的字符串
    tag_str = str()
    tag_list = []  # 列表中的每个元素为每句话对应的tag所组成的字符串
    while i < len(list_all) - 1:
        str_all = list_all[i]
        # print(str_all)
        tep_list = str_all.split(' ')
        if (len(tep_list) > 1) & (tep_list[0] not in '!。?；'):
            char_str += (tep_list[0] + ' ')
            tag_str += tep_list[1]
        else:
            if tep_list[0] in '!。?；':
                char_str += (tep_list[0] + ' ')
                tag_str += tep_list[1]
            char_list.append(char_str)
            tag_list.append(tag_str)
            char_str = str()
            tag_str = str()
        i += 1
    # print(char_list[:3], tag_list[:3])

    char_data = [sent.split() for sent in char_list if len(sent) > 0]  # 将每句话转化为由单字符字符串构成的列表
    tag_data = [tags.split('\n')[:-1] for tags in tag_list if len(tags) > 0]  # 同上, 专门去掉''
    # 'O\nLOC\nO\n'.split('\n') : ['O', 'LOC', 'O', '']    !!!!
    return char_data, tag_data


def get_char2object():
    """
    获取预先训练好的字向量
    :return:
    """
    char2vec = {}
    f = open('Word2Vec/character_model/word_vec')  # load pre-trained word embedding
    i = 0
    for line in f:
        tep_list = line.split()
        if i == 0:  # 第一行的两个数字
            n_char = int(tep_list[0])
            n_embed = int(tep_list[1])
        else:  # 其他行
            char = tep_list[0]
            vec = np.asarray(tep_list[1:], dtype='float32')
            char2vec[char] = vec
        i += 1
    f.close()
    char2index = {k: i for i, k in enumerate(sorted(char2vec.keys()), 1)}
    return char2vec, n_char, n_embed, char2index  # char2vec 指的是每个字符对应的向量，char2index 指的是每个字符所在未知的索引，n_embed，每个字向量的维度，n_char


def get_embedding_matrix(char2vec, n_vocab, n_embed, char2index):
    """
    将加载的字向量放入到矩阵中
    :param char2vec:
    :param n_vocab:
    :param n_embed:
    :param char2index:
    :return:
    """
    embedding_mat = np.zeros([n_vocab, n_embed])
    for w, i in char2index.items():
        vec = char2vec.get(w)
        if vec is not None:
            embedding_mat[i] = vec
    if not os.path.exists(embedding_file):
        np.save(embedding_file, embedding_mat)
    return embedding_mat


def get_X_data(char_data, char2index, max_length):
    """
    准备输入的数据，不足的填充0
    :param char_data:
    :param char2index:
    :param max_length:
    :return:
    """
    index_data = []
    for l in char_data:
        index_data.append([char2index[s] if char2index.get(s) is not None else 0
                           for s in l])
    index_array = pad_sequences(index_data, maxlen=max_length, dtype='int32',
                                padding='post', truncating='post', value=0)
    return index_array


def get_y_data(tag_data, label2index, max_length):
    """
    准备输入的标签集合
    :param tag_data:
    :param label2index:
    :param max_length:
    :return:
    """
    index_data = []
    for l in tag_data:
        index_data.append([label2index[s] for s in l])
    index_array = pad_sequences(index_data, maxlen=max_length, dtype='int32',
                                padding='post', truncating='post', value=0)
    index_array = to_categorical(index_array, num_classes=3)  # (20863, 574, 7)

    # return np.expand_dims(index_array, -1)
    return index_array


if __name__ == '__main__':

    train, tag = get_char_tag_data('data/allwords.txt')  # 字符组成的列表
    word_train = get_word_data(train)  # 词组成的列表
    assert len(train) == len(tag)
    assert len(word_train) == len(train)
    i = 0
    while (i < len(train)):
        if (len(train[i]) > 300):
            del (train[i])
            del (tag[i])
            del (word_train[i])
        else:
            i = i + 1

    # 字转索引

    char2vec, n_char, n_embed, char2index = get_char2object()  # 加载字向量
    n_vocab = n_char + 1

    if os.path.exists(embedding_file):
        embedding_mat = np.load(embedding_file)
    else:
        embedding_mat = get_embedding_matrix(char2vec, n_vocab, n_embed, char2index)

    X_train = get_X_data(train, char2index, 300)

    # 词转索引
    word2vec, n_word, n_embed, word2index = get_word2object()
    n_word_vocab = len(word2vec.keys()) + 1

    if os.path.exists(word_embedding_file):
        word_embedding_matrix = np.load(word_embedding_file)
    else:
        word_embedding_matrix = get_word_embedding_matrix(word2vec, n_word_vocab,
                                                          n_embed, word2index)

    word_index_train = add_word_data(word_train, word2index, 300)

    label2index = dict()
    idx = 0
    for c in ['O', 'B', 'I']:
        label2index[c] = idx
        idx += 1
    # print(label2index)
    y = get_y_data(tag, label2index, 300)

    # 打乱索引
    index = [i for i in range(len(train))]
    random.shuffle(index)

    train=np.array(train)
    tag=np.array(tag)
    X_train=np.array(X_train)
    y=np.array(y)
    word_train=np.array(word_train)
    word_index_train=np.array(word_index_train)
    train = train[index]
    tag = tag[index]
    X_train = X_train[index]
    y = y[index]
    word_train=word_train[index]
    word_index_train = word_index_train[index]

    np.save("data/tt.npy", train)
    np.save("data/tag.npy", tag)
    np.save("data/train.npy", X_train)
    np.save("data/y.npy", y)
    np.save("data/word.npy",word_index_train)
    np.save("data/word_char.npy",word_train)
