# -*- coding: utf-8 -*-

"""
@author: curry
@software: Pycharm
@file: word2vec.py
@time: 2018/3/14
@description: 训练词向量
"""

import gensim, logging
import preprocess as pt
from utils import get_word_data
from Word2Vec import Iterator
import jieba

import os

# char_train, tag_train = pt.get_char_tag_data('../data/allwords.txt')
# word_train = get_word_data(char_train)
# with open('../data/words.txt', 'w') as fout:
#     for word_list in word_train:
#         for word in word_list:
#             fout.write(word + " ")
#         fout.write('\n')

FILE_INPUT_DIR = '/home/curry/NER/patent/character_segmentation_column_simple_copy'
FILE_OUTPUT = '/home/curry/NER/patent/all_words.txt'

#
#
#
#
#
# def get_sentences(file_path):
#     """
#     获取分好词的句子
#     :param file_path:
#     :return:
#     """
#     with open(file_path, 'r') as f:
#         list_all = f.readlines()
#     i = 0
#     char_str = str()
#     char_list = []  # 列表中每个元素为每句话组成的字符串
#     while (i < len(list_all) - 1):
#         str_all = list_all[i]
#         if (str_all[0] not in '!。?；'):
#             char_str += (str_all[0])
#         else:
#             if (str_all[0] in '!。?；'):
#                 char_str += (str_all[0])
#             char_list.append(char_str)
#             char_str = str()
#         i += 1
#     return char_list
#
#
#
# if __name__=="__main__":
#     jieba.initialize()
#     with open(FILE_OUTPUT,'w') as fout:
#         for file in os.listdir(FILE_INPUT_DIR):
#             index = file.rfind(".")
#             if (os.path.isfile(os.path.join(FILE_INPUT_DIR, file)) and file[index:] == ".txt"):
#                 sentences=get_sentences(os.path.join(FILE_INPUT_DIR,file))
#                 for sentence in sentences:
#                     seq_cut=jieba.cut(sentence,cut_all=False)
#                     for word in seq_cut:
#                         fout.write(word+' ')
#                     fout.write('\n')




logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences=Iterator.Iterator(FILE_OUTPUT)
model=gensim.models.Word2Vec(sentences=sentences,sg=1,window=8,min_count=1,size=200,iter=15,hs=1,negative=10)
model.save('./model/model_hs_neg')
model.wv.save_word2vec_format("./model/word_vec_word")
