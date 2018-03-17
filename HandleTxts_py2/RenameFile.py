# -*- coding: utf-8 -*-
"""
@author: curry
@software: PyCharm
@file: RenameFile.py
@time: 2018/3/15
@description: 重命名文件
"""

import os

dirname=r'/home/curry/NER/patent/processed_txts_englishname'
i=0

for file in os.listdir(dirname):
    os.rename(os.path.join(dirname,file),os.path.join(dirname,str(i)+'.txt'))
    i=i+1
