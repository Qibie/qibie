# -*- coding: utf-8 -*-

"""
@author: curry
@software: Pycharm
@file: word2vec.py
@time: 2018/3/17
@description: 训练字向量
"""

import gensim,logging
from Word2Vec import Iterator

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# sentences=Iterator.Iterator(r'/home/curry/NER/patent/character_segmentation/allwords.txt')
# model=gensim.models.Word2Vec(sentences=sentences,sg=1,window=8,min_count=1,size=100,iter=10,hs=1,negative=10)
# model.save('./character_model/model')
model =gensim.models.Word2Vec.load('./character_model/model')
model.wv.save_word2vec_format('./character_model/word_vec')

