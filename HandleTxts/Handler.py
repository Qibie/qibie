# -*- coding: utf-8 -*-
"""
@author: curry
@software: PyCharm
@file: Handler.py
@time: 2018/3/11
@description: 数据集处理,使用
"""

from HandleTxts.processtxts import ProcessTxt


if __name__=="__main__":
    input_path=r'/home/curry/NER/patent/txts/'
    output_path=r'/home/curry/NER/patent/processed_txts'
    word_segmentation_path=r'/home/curry/NER/patent/Word_Segmentation/'
    character_segmentation_path=r'/home/curry/NER/patent/character_segmentation/'
    pt=ProcessTxt(input_path,output_path)
    #pt.processtxts()
    #pt.wordSegmentation(word_segmentation_path)
    #pt.mergeallwords(word_segmentation_path,True)
    pt.characterSegmentation(character_segmentation_path)
