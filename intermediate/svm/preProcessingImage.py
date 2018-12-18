# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from skimage import filters,io,morphology,color
import numpy as np
def preProcess():
    inputpic = []
    with open('../txt/Char_Index.txt','r') as file:
        for f in file:
            if f[0] !='#':
                lineattr = f.strip().split('\t')
                inputpic.append(lineattr[2])
    lenth=len(inputpic)
    print(lenth)

    for k in range(lenth):
        rd = io.imread('../preImage/'+inputpic[k] , as_grey = True)  # why I need to use this method ,sorry
        #rd = color.rgb2gray(rd)
        th = filters.threshold_otsu(rd)                              # need to check this method use to do what

        binary = (rd > th) * 1.0
        rw = binary.shape[0]
        cl = binary.shape[1]


        #io.imshow(binary)
        #plt.show()
        #print(type(binary))
        #print(binary.shape)
        #print("图片高度:",binary.shape[0])  #图片高度
        #print("图片宽段:",binary.shape[1])  #图片宽段
        width  = binary.shape[1]             # 记录图片的宽度
        binary = np.zeros((rw ,cl))      #生成 np.zeros((2, 1))#生成2行1列的零矩阵

        for i in range(0,rw,width):
            for j in range(0,cl,width):
                md = rd[i:min(i+width,rw),j:min(j+width,cl)]
                th = filters.threshold_otsu(md)
                md_th = (md > th) * 1.0
                binary[i:min(i+width,rw),j:min(j+width,cl)] = md_th
        binary=morphology.opening(binary,morphology.disk(1))

        if binary[0,0] + binary[0,cl-1]+ binary[rw-1,0]+binary[rw-1,cl-1] >= 2:
            for i in range(rw):
                for j in range(cl):
                    binary[i,j] = 1 - binary[i,j]

        io.imsave('../aftImage/' + inputpic[k], binary)

        #print(binary.shape[2])
        #print(binary.size)      #显示总像素个数
        #print(binary.max())     #显示最大像素值
        #print(binary.min())     #显示最小像素值
        #print(binary.mean())    #显示平均像素值
    pass

if __name__ == '__main__':
    print("process start")
    preProcess()
    print("process end")
