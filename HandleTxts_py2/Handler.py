# -*- coding: utf-8 -*-
"""
@author: curry
@software: PyCharm
@file: Handler.py
@time: 2018/3/14
@description: 数据集处理,使用python2 pynldir
"""
from HandleTxts_py2 import processtxts

if __name__=='__main__':
    input_path = r'/home/curry/NER/patent/txts/'
    output_path = r'/home/curry/NER/patent/processed_txts_englishname'
    word_segmentation_path=r'/home/curry/NER/patent/Word_Segmentation_pynlpir'
    pt=processtxts.ProcessTxt(input_path,output_path,word_segmentation_path)
    # pt.processtxts() #处理文本
    pt.WordSegmentation() #分词
    pt.mergeallwords(True) #合并分词结果