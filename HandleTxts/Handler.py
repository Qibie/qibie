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
    input_path=r'/home/curry/NER/patent/txts/origin_txts'
    output_path=r'/home/curry/NER/patent/txts/processed_txts'
    word_segmentation_path=r'/home/curry/NER/patent/txts/Word_Segmentation'
    pt=ProcessTxt(input_path,output_path)
    # pt.processtxts()
    pt.wordSegmentation(word_segmentation_path)