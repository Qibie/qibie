# -*- coding: utf-8 -*-
"""
@author: curry
@software: PyCharm
@file: processtxts.py
@time: 2018/3/10
@description: 处理txt，去除标点 数字 以及到摘要前的文字,暂时就先去掉摘要之前的文本,并利用
"""

import re
import os
import jieba

class ProcessTxt:
    def __init__(self, input_path, output_path):
        # 去掉中文数字和标点
        # self.chineseNum = re.compile(r'(１)|(２)|(３)|(４)|(５)|(６)|(７)|(８)|(９)|(０)|(（)|(）)|(\d)|([-]+)')
        # self.chinesePunctuation = re.compile(
        #     r'(，)|(、)|(。)|(：)|(《)|(》)|(\[)|(\])|(；)|(”)|(“)|(\.)|(%)|(——)|(？)|(！)|(『)|(』)|()|(\()|(\))|(≧)|(％)|(～)|(＝)|(\+)|(-)|(\*)|(\/)|(<)|(>)|(＞)|()')
        # self.pattern=re.compile(r'()')
        # 指定输入文件夹
        self.INPUT_PATH = input_path
        # 指定输出文件夹
        self.OUTPUT_PATH = output_path

    def processtxts(self):
        """
        除去摘要之前的文本
        :return:
        """
        # 遍历所有txts
        for file in os.listdir(self.INPUT_PATH):
            index = file.rfind('.')
            if (os.path.isfile(os.path.join(self.INPUT_PATH, file)) and file[index:] == '.txt'):
                with open(os.path.join(self.INPUT_PATH, file)) as finput:
                    with open(os.path.join(self.OUTPUT_PATH, file), 'w') as fouput:
                        for line in finput.readlines():
                            if not line:
                                break
                            else:
                                # line=self.chineseNum.sub("",line)
                                # line=self.chinesePunctuation.sub("",line)
                                index = line.find("摘要")
                                line = line[index + 2:]
                                print(line)
                                fouput.write(line)

    def wordSegmentation(self, word_segmentation_path):
        """
        分词
        :return:
        """
        for file in os.listdir(self.OUTPUT_PATH):
            index = file.rfind('.')
            if (os.path.isfile(os.path.join(self.OUTPUT_PATH, file)) and file[index:] == '.txt'):
                with open(os.path.join(self.OUTPUT_PATH, file)) as finput:
                    with open(os.path.join(word_segmentation_path, file), 'w') as foutput:
                        for line in finput.readlines():
                            if not line:
                                break
                            else:
                                seg_list = jieba.cut(line.strip(), cut_all=False)
                                seg = ' '.join(seg_list)
                                foutput.write(seg)

    def mergeallwords(self, word_segmentation_path,daily_standard):
        """
        合并分词的结果
        :param word_segmentation_path:
        :return:
        """
        with open(os.path.join(word_segmentation_path,"allwords.txt"),'w') as foutput:
            """
            首先把人民日报和国家标准中的词读合并到allows.txt中
            """
            if(daily_standard):
                with open('/home/curry/NER/patent/dailywords.txt','r') as finput:
                    for line in finput.readlines():
                        if not line:
                            break
                        elif len(line.strip())!=0:
                            foutput.write(line)
                        else:
                            continue


                with open('/home/curry/NER/patent/chunking.txt','r') as finput:
                    for line in finput.readlines():
                        if not line:
                            break
                        elif len(line.strip())!=0:
                            foutput.write(line)
                        else:
                            continue



            for file in os.listdir(word_segmentation_path):
                index = file.rfind(".")
                if (os.path.isfile(os.path.join(word_segmentation_path, file)) and file[index:] == '.txt'):
                    with open(os.path.join(word_segmentation_path,file)) as finput:
                        for line in finput.readlines():
                            if not line:
                                break
                            elif len(line.strip()) != 0:
                                foutput.write(line)
                            else:
                                continue