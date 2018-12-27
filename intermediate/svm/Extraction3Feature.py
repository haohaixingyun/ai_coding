# -*- coding:utf-8 -*-
from skimage import  io, filters
import  numpy as np
import matplotlib.pyplot as plt
'''
Some mention:
当从各个方向计算到最外围的白点距离 ，因此特征讲有  行 + 列 + 行 + 列个 特征  ,如果此行没有白点 ，那么长度将是整列的长度
'''
def extraction3feature():

    input_pics = [] #获取所有的图片的名称 并放入一个list 里面
    with open("../txt/Char_Index.txt") as fp:
        for line in fp:
            if line[0]!="#":
                va = line.strip().split("\t")[0]   # 记录样本的序列号
                pc = line.strip().split("\t")[2]
                input_pics.append(pc)
    with open("../txt/feature3.txt",'w+') as fp :
        ls = len(input_pics)
        for x in range(1):
            pis = io.imread("../aftImage/"+input_pics[x],as_grey=True )  #pis is a ndarray
            thd = filters.threshold_otsu(pis)  # 获取图片的阈值
            bia = (pis > thd) * 1.0  # 0 1 组成的二维数组
            rw = bia.shape[0]  #数组的行数  must shape
            cl = bia.shape[1]  #数组的列数  must shape

            C = np.zeros((rw+cl)*2,dtype=np.int)
            #计算从左边数
            for i in range(rw):
                for j in range(cl):
                    if bia[i,j] ==1:
                        C[i] = j
                        break
                    if bia[i,cl-1] ==0 and j ==cl -1 :  # cause [0,cl)
                        C[i]= cl
                pass

            #计算从右边数
            for i in range(rw):
                for j in range(cl):
                    if bia[i,cl-1-j]==1:
                        C[rw+i] = cl-j-1
                        break
                    if [i,0] ==0 and j == 0:
                        C[rw + i] = cl - 1

            #计算从上面数
            for j in range(cl):
                for i in range(rw):
                    if bia[i,j] ==1:
                        C[rw+rw+j] =i
                        break
                    if bia[rw-1,j] ==0 and i ==rw -1:
                        C[rw + rw + j] = rw -1

            #计算从下面数
            for j in range(cl):
                for i in range(rw):
                    if bia[rw-1-i,j] ==1:
                        C[rw+rw+cl+j] = i
                        break
                    if bia[i,j] ==0 and i ==0:
                        C[rw + rw + cl + j] = rw

            fp.write(str(x +1)+"\t")
            for z in range(len(C)-1):
                fp.write(str(C[z])+",")
            if x < 999:
                fp.write(str(C[len(C)-1])+"\n")
            else:
                fp.write(str(C[len(C)-1]))

        pass


if __name__ =="__main__":
    extraction3feature()