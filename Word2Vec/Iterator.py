# -*- coding: utf-8 -*-

"""
@author: curry
@software: Pycharm
@file: Iterator.py
@time: 2018/3/14
@description: 文本迭代器
"""

import codecs


class Iterator(object):
    def __init__(self,filename):
        self.filename=filename

    def __iter__(self):
        with  codecs.open(self.filename,'r') as file:
            for line in file.readlines():
                if not line:
                    break
                elif len(line.strip())!=0:
                    yield line.strip().split()
                else:
                    continue

