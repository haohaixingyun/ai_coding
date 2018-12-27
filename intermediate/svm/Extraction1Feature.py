# -*- coding: utf-8 -*-

'''
提取每行 每列上的白点个数  并且每个行和列都算是一个特征数据 ，因为计算的是有白点的数据 所以 这个 Y标签就都是 1  fuck clver

'''

from skimage import io,filters
import numpy as np
def extraction1feature():

    inputpic = []
    with open('../txt/Char_Index.txt','r') as fp:
        for line in fp:
            if line[0] != '#':
                picname = line.strip().split('\t')
                inputpic.append(picname[2])

    lens = len(inputpic)
    with open('../txt/feature_1.txt','w+') as fp :
        for k in range(lens):
            rd = io.imread('../aftImage/' + inputpic[k],as_grey= True)
            th = filters.threshold_otsu(rd)
            md = (rd > th) * 1

            rw = md.shape[0]
            cl = md.shape[1]
            print('rw',rw, 'cl',cl)
            C  = np.zeros(rw + cl , dtype=np.int)  # 这里是共行程了行 + 列个特征值 ，并计算这一行列上白点的个数 ，真fuck聪明

            for i in  range(rw):
                for j in range(cl):
                    if md[i,j] == 1 :
                        C[i] += 1

            for j in range(cl):
                for i in range(rw):
                    if md[i,j] ==1:
                        C[j+rw] +=1

            fp.write(str(k+1)+'\t')  # 写入一个编号
            for x in range(rw + cl -1):
                fp.write(str(C[x]) + ',')
            if k < 999:
                fp.write(str(C[cl + rw -1]) + '\n')
            else:
                fp.write(str(C[cl + rw - 1]) )
    pass


if __name__ =='__main__':
    extraction1feature()

