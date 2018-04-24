# coding = utf-8
"""
@author: curry
@software: PyCharm
@file: processtxts.py
@time: 2018/4/10
@description: 拿到一篇专利中最值得标注的句子 ，思路是：
    将该专利中所有的句子进行余弦相似度匹配，找到同本专利相似度最高的
    1、首先将专利中的所有的句子放到矩阵中
    2、依次计算每一个句子同矩阵的匹配度
    3、依据相似度排序
"""

from keras.preprocessing.sequence import pad_sequences
from activelearning import preprocess as pt
import numpy as np


class Findtopsentences:
    def __init__(self):
        self.filename = ''  # 文件位置
        self.char_embedding, self.n_char, self.n_embed, self.index2char, self.char2index = self.get_char_embedding()

    def set_filename(self, filename):
        """
        设置文件路径
        :param filename:
        :return:
        """
        self.filename = filename

    def get_char_data(self):
        """
        返回由单字符字符串构成的列表
        :return:
        """
        # 获取所有的行数

        with open(self.filename) as finput:
            list_all = finput.readlines()
        i = 0
        char_str = str()
        char_list = []  # 列表中每个元素为每句话组成的字符串
        while i < (len(list_all) - 1):
            str_all = list_all[i]
            if (str_all[0] not in '!。?;；！'):
                char_str += (str_all[0] + ' ')
            else:
                if str_all[0] in '!。?;；！':
                    char_str += (str_all[0] + ' ')
                    char_list.append(char_str)
                    char_str = str()
            i += 1
        char_data = [sent.split() for sent in char_list if len(sent) > 0]  # 将每句话转化为由单字符字符串构成的列表
        return char_data

    def get_index_data(self, char_data, max_length):
        """
        准备输入的数据，不足的填充0
        :param char_data:
        :param char2index:
        :param max_length:
        :return:
        """
        index_data = []
        for l in char_data:
            index_data.append([self.char2index[s] if self.char2index.get(s) is not None else 0
                               for s in l])
        index_array = pad_sequences(index_data, maxlen=max_length, dtype='int32',
                                    padding='post', truncating='post', value=0)
        return index_array

    def get_sentences_embedding(self, index_array):
        """
        整篇文档的所有的句子的向量
        :param index_array:
        :return:
        """
        embedding_data = []
        for l in index_array:
            sentences_embedding = np.zeros(self.n_embed)
            for index in l:
                if (index in self.index2char.keys()):
                    sentences_embedding = sentences_embedding + self.char_embedding[self.index2char[index]]
            embedding_data.append(sentences_embedding)
        return embedding_data

    def get_char_embedding(self):
        """
        加载训练好的字向量
        :return:
        """
        char2vec, n_char, n_embed, char2index = pt.get_char2object()  # 加载训练好的向量
        index2char = {i: w for w, i in char2index.items()}  # 字典： index:char
        char_embedding = {w: v for w, v in char2vec.items()}  # 字典：char:embeding
        return char_embedding, n_char, n_embed, index2char, char2index

    def gettopsentences(self, length):
        char_data = self.get_char_data()  # 文章句子
        index_array = self.get_index_data(char_data, 500)  # 索引构成的句子
        sentences_embedding = self.get_sentences_embedding(index_array)  # 文章句子向量
        sentence_rank = np.zeros(len(char_data))  # 记录每个句子的相似度
        i = 0
        while i < (len(index_array) - 1):
            index_data = index_array[i]
            """
            获取当前句子的向量
            """
            sentence_embedding = np.zeros(self.n_embed)
            for index in index_data:
                if (index in self.index2char.keys()):
                    sentence_embedding = sentence_embedding + self.char_embedding[self.index2char[index]]

            """
            计算余弦相似度
            """
            cos = 0
            j = 0
            while j < (len(sentences_embedding)-1):
                cos += self.sim(sentence_embedding, sentences_embedding[j])
                j = j + 1
            sentence_rank[i] = cos

            # 累加
            i = i + 1
        # 对sentence_rank 进行排序 拿到索引
        top_index = np.argsort(sentence_rank)[-length:]
        sentences=[]
        for index in top_index:
            sentences.append(char_data[index])
        return sentences

    def sim(self, vector1, vector2):
        """
        计算余弦 相似度
        :param v1:
        :param v2:
        :return:
        """

        dot_product = 0.0
        normA = 0.0
        normB = 0.0
        for a, b in zip(vector1, vector2):
            dot_product += a * b
            normA += a ** 2
            normB += b ** 2
        if normA == 0.0 or normB == 0.0:
            return None
        else:
            return dot_product / ((normA * normB) ** 0.5)
