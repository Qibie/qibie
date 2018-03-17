# -*- coding: utf-8 -*-
"""
@author: curry
@software: PyCharm
@file: processtxts.py
@time: 2018/3/10
@description: 处理txt，去除标点 数字 以及到摘要前的文字,暂时就先去掉摘要之前的文本, python2 版本 利用pynlpir,这里只处理分词
"""

import os
import pynlpir
import codecs
import re



class ProcessTxt:
    def __init__(self, input_path,output_path, word_segmentation_path):
        self.word_segmentation_path = word_segmentation_path
        self.output_path = output_path
        self.input_path=input_path
        # 去掉中文数字和标点
        # self.chineseNum = re.compile(r'(１)|(２)|(３)|(４)|(５)|(６)|(７)|(８)|(９)|(０)|(（)|(）)|(\d)|([-]+)')
        # self.chinesePunctuation = re.compile(
        #     r'(，)|(、)|(。)|(：)|(《)|(》)|(\[)|(\])|(；)|(”)|(“)|(\.)|(%)|(——)|(？)|(！)|(『)|(』)|()|(\()|(\))|(≧)|(％)|(～)|(＝)|(\+)|(-)|(\*)|(\/)|(<)|(>)|(＞)|()')
        self.specialpunction=re.compile(r'()')
    def processtxts(self):
        """
        除去摘要之前的文本
        :return:
        """
        # 遍历所有txts
        for file in os.listdir(self.input_path):
            index = file.rfind('.')
            if (os.path.isfile(os.path.join(self.input_path, file)) and file[index:] == '.txt'):
                with open(os.path.join(self.input_path, file)) as finput:
                    with open(os.path.join(self.output_path, file), 'w') as fouput:
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

    def WordSegmentation(self):
        """
        分词
        :return:
        """
        pynlpir.open()
        for file in os.listdir(self.output_path):
            index = file.rfind('.')
            if (os.path.isfile(os.path.join(self.output_path, file)) and file[index:] == '.txt'):
                # os.mknod(os.path.join(self.word_segmentation_path, file))
                pynlpir.nlpir.FileProcess(os.path.join(self.output_path, file),
                                          os.path.join(self.word_segmentation_path, file),False)
        pynlpir.close()

    def mergeallwords(self,daily_standard):
        """
        合并分词的结果
        """
        with open(os.path.join(self.word_segmentation_path,"allwords.txt"),'w') as foutput:
            """
            首先把人民日报和国家标准中的词读合并到allows.txt中
            """
            if (daily_standard):
                with open('/home/curry/NER/patent/dailywords.txt', 'r') as finput:
                    for line in finput.readlines():
                        if not line:
                            break
                        elif len(line.strip()) != 0:
                            foutput.write(line)
                        else:
                            continue

                with open('/home/curry/NER/patent/chunking.txt', 'r') as finput:
                    for line in finput.readlines():
                        if not line:
                            break
                        elif len(line.strip()) != 0:
                            foutput.write(line)
                        else:
                            continue
            for file in os.listdir(self.word_segmentation_path):
                index = file.rfind(".")
                # file_path=unicode(os.path.join(self.word_segmentation_path,file),'utf8')
                file_path=os.path.join(self.word_segmentation_path, file)
                if (os.path.isfile(file_path) and file[index:] == '.txt'):
                    with codecs.open(file_path) as finput:
                        for line in finput.readlines():
                            if not line:
                                break
                            elif len(line.strip()) != 0:
                                foutput.write(line)
                            else:
                                continue