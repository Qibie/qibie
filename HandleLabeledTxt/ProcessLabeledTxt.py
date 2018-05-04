# coding = utf-8

import os

# file_path = '/home/curry/NER/patent/labeled/CN106994283A-一种新能源汽车用空气过滤器.txt'
# file_out_path='/home/curry/NER/patent/labeled_complete/CN106994283A-一种新能源汽车用空气过滤器.txt'
#
#
#
#
# with open(file_out_path,'w') as fileoutput:
#     with  open(file_path,'r') as fileinput:
#         for line in fileinput.readlines():
#             if not line:
#                 break
#             elif (len(line.strip()) > 2):
#                 line=line.strip()
#                 str_temp=line[0]+' '
#                 i=1
#                 while i<len(line):
#                     if line[i]!=' ':
#                         str_temp=str_temp+line[i]
#                         break
#                     i=i+1
#                 fileoutput.write(str_temp+'\n')
#
#             else:
#                 continue


INPUT_DIR = '/home/curry/NER/patent/labeled'
OUTPUT_DIR = '/home/curry/NER/patent/labeled_complete'
#
# for file in os.listdir(INPUT_DIR):
#     index=file.rfind(".")
#     if (os.path.isfile(os.path.join(INPUT_DIR,file)) and file[index:]=='.txt'):
#         with open(os.path.join(INPUT_DIR,file),'r') as fileinput:
#             with open(os.path.join(OUTPUT_DIR,file),'w') as fileoutput:
#                 for line in fileinput.readlines():
#                     if not line:
#                         break
#                     elif (len(line.strip()) > 2):
#                         line = line.strip()
#                         str_temp = line[0] + ' '
#                         i = 1
#                         while i < len(line):
#                             if line[i] != ' ':
#                                 str_temp = str_temp + line[i]
#                                 break
#                             i = i + 1
#                         fileoutput.write(str_temp + '\n')
#
#                     else:
#                         continue
#
# with open(os.path.join(OUTPUT_DIR, "allwords.txt"), 'w') as fout:
#     for file in os.listdir(OUTPUT_DIR):
#         index = file.rfind(".")
#         if (os.path.isfile(os.path.join(OUTPUT_DIR, file)) and file[index:] == '.txt'):
#             with open(os.path.join(OUTPUT_DIR, file), 'r') as finput:
#                 for line in finput.readlines():
#                     if not line:
#                         break
#                     elif (len(line.strip()) > 0):
#                         fout.write(line)
#                     else:
#                         continue
#
# with open('../data/allwords.txt', 'r') as finput:
#     with open("../data/allwords1.txt", 'w') as foutput:
#         for line in finput.readlines():
#             if not line:
#                 break
#             elif (len(line.strip()) > 0):
#                 if(line[2]!='0'):
#                     foutput.write(line)
#                 else:
#                     line[2]='O'
#                     foutput.write(line)
#             else:
#                 continue


# import numpy as np
# train=np.load("../data/train.npy")
# i=0
# for line in train:
#     if(len(line)>300):
#         print(len(line))
#         print(line)
#         i=i+1

#
# import numpy as np
# X_train=np.load("../data/train.npy")
# train_char=np.load('../data/tt.npy')
# tag=np.load("../data/tag.npy")
# y=np.load("../data/y.npy")
#
#
# i=0
# while(i<len(train_char)):
#     # print(X_train[i])
#     print(train_char[i])
#     print(tag[i])
#     # print(y[i])
#     print("#########################")
#     i=i+1
#
#
import os

DIR_NAME='/home/curry/NER/patent/character_segmentation_column'

i=0
for file in os.listdir(DIR_NAME):
    index=file.rfind('.')
    if(os.path.isfile(os.path.join(DIR_NAME,file)) and file[index:]=='.txt'):
        with open(os.path.join(DIR_NAME,file),'r') as finput:
            for line in finput.readlines():
                i=i+1
print(i)