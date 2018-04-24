# coding = utf-8
"""
@author: curry
@software: PyCharm
@file: processtxts.py
@time: 2018/4/10
@description: 主动学习
"""

from activelearning.findtopsentences import Findtopsentences
import numpy as np
import os

FILE_SOURCE_DIRNAME = '/home/curry/NER/patent/character_segmentation_column'
FILE_TARGET_DIRNAME = '/home/curry/NER/patent/character_segmentation_column_simple'
LABEL_LEGTH = 20

ft = Findtopsentences()

for file in os.listdir(FILE_SOURCE_DIRNAME):
    index = file.rfind('.')
    if (os.path.isfile(os.path.join(FILE_SOURCE_DIRNAME, file)) and file[index:] == '.txt'):
        ft.set_filename(os.path.join(FILE_SOURCE_DIRNAME, file))
        sentences = ft.gettopsentences(LABEL_LEGTH)
        with open(os.path.join(FILE_TARGET_DIRNAME, file), 'w') as foutput:
            for l in sentences:
                for c in l:
                    foutput.write(c + '\n')


