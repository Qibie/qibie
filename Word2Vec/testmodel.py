# -*- coding: utf-8 -*-

"""
@author: curry
@software: Pycharm
@file: testmodel.py
@time: 2018/3/14
@description: 测试训练出来的词向量
"""

import gensim

model=gensim.models.Word2Vec.load('./model_py2/model_hs_neg')
# 计算某个词的相关词列表
similar_list=model.most_similar(u'电池')

for item in similar_list:
    print(item[0],item[1])