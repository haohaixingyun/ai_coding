# -*- coding :utf-8 -*-

from skimage import io,filters
import  numpy as np
import math
def extractionFeature():

#step 1 get the picture name
    with open('../txt/Char_Index.txt','r') as  fp:
        picnamearray = []
        for line in fp:
            if line[0] !='#':
                picname = line.strip().split('\t')[2]
                picnamearray.append(picname)
        pass
    #print(picnamearray)
    lens = len(picnamearray)
    # 定义特征值
    bfnum = 6*12

#step 2 try to 一枝花 二值化 一张图片 也就是 白字黑底  （1,0）

    with open("../txt/feature2.txt",'w+') as fp:

        for x in range(lens):
            rd = io.imread('../aftImage/' + picnamearray[x])
            th = filters.threshold_otsu(rd)
            md = (rd > th )* 1.0
            rw = md.shape[0]
            cl = md.shape[1]

            C = np.zeros(bfnum, dtype=np.int)  # 为每张图片定义特征向量 ，采用区域密度方式 ，也就是每张图片特征向量的个数是 72 个
            crw = np.ceil(rw/8.0)
            ccl = math.ceil(cl/8.0)   # here we should use math not numpy  ,you are very cute

            for  i  in range(rw):
                irw = math.floor(i/8)    # one more here we use floor not float  have no idea
                for j in range(cl):
                    jcl = math.floor(j/8)
                    if md[i,j] ==1:
                        l = irw*ccl +jcl
                        C[l] +=1

            fp.write(str(x + 1) + '\t')
            for z in range(len(C)):
                fp.write(str(C[z]) + ',')
            if x <999:
                fp.write( str(C[z]) +'\n')
            else:
                fp.write(str(C[z]))
            pass

    pass


if __name__=="__main__":
    extractionFeature()