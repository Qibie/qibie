# -*- coding: utf-8 -*-
# CN107658182A-一种低压直流控制交流接触器的电路和方法

"""
@author:curry
@software:PyCharm
@file:parsePdf.py
@time:2018/3/10
"""

import sys
import importlib

importlib.reload(sys)

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import os


input_path=r'/home/curry/NER/20180309054447078/files'
output_path=r'/home/curry/NER/txts_20180309054447078'



'''
转换成txt
'''
def converter():
    for file in os.listdir(input_path):
        file_path=os.path.join(input_path,file)
        index=file.rfind('.')
        file_out_path=os.path.join(output_path,file[:index]+'.txt')
        print('loadding '+file)
        with open(file_path,'rb') as input:
            with open(file_out_path,'w') as output:
                # 创建一个PDF资源管理器对象来存储共享资源
                # caching = False不缓存
                rsrcmgr = PDFResourceManager(caching=False)
                # 创建一个PDF设备对象
                laparams = LAParams()
                device = TextConverter(rsrcmgr, output,laparams=laparams)
                # 创建一个PDF解析器对象
                process_pdf(rsrcmgr, device, input)
                # 关闭输入流
                input.close()
                # 关闭输出流
                device.close()
                output.flush()
                output.close()
        print('done')


if __name__ == '__main__':
    converter()