# -*- coding: utf-8 -*-

"""
@author: curry
@software: Pycharm
@file: word2vec.py
@time: 2018/3/14
@description: 训练词向量
"""

import gensim,logging
from Word2Vec import Iterator


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences=Iterator.Iterator(r'/home/curry/NER/patent/Word_Segmentation_pynlpir/allwords.txt')
model=gensim.models.Word2Vec(sentences=sentences,sg=1,window=8,min_count=1,size=100,iter=10,hs=1,negative=10)
model.save('./model_py2/model_hs_neg')
