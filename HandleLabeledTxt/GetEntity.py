#encoding=utf-8
import os

# DIR_NAME='/home/curry/NER/patent/labeled'
#
# with open('entity.txt','w') as fentity:
#         with open('../data/allwords.txt','r') as f:
#             entity=''
#             for line in f.readlines():
#                 if not line:
#                     break
#                 elif len(line)>0:
#                     if(line[2]=='B' or line[2]=='I'):
#                         entity=entity+line[0]
#                     elif line[2]=='O':
#                         if len(entity)>0:
#                             fentity.write(entity+"\n")
#                             entity=''
#
#                 else:
#                     continue
# #
# import gensim
# from Word2Vec.Iterator import Iterator
#
# sentences=Iterator('entity.txt')
# model=gensim.models.Word2Vec(sentences=sentences,iter=1)
#
# model.wv.save_word2vec_format('entity_vec.txt')

with open("entity_vec.txt",'r') as f:
    with open('entity_labeld.txt','w') as fout:
        for line in f.readlines():
            if not line:
                break
            elif len(line)>0:
                lines=line.strip().split(' ')
                fout.write(lines[0]+'\n')
            else:
                continue