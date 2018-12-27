# -*- coding:utf-8 -*-

import intermediate.svm.atestmodle_method1  as modle1
import intermediate.svm.atestmodle_method2  as modle2
from intermediate.svm.Extraction1Feature import *
from intermediate.svm.Extraction2Feature import *
def mainFuction():
    '''
    一张图片经过处理之后变成 92 * 47 大小的像素
    '''
    extraction1feature()  # 提取图片中每一行(92,47)每一列的白点个数 ，因此一张图片共有 行加列个特征  92+47 = 139 个特征
    extractionFeature()   # 提取一定区域内的白点个数 ，区域的大小为  8 * 8   大约 47/8 * 92/8 = 6*12 = 72  个特征
    #extraction3feature() #为字符左右上下与边界的距离
    #extraction4feature() # 为每一行和每一列的线段数目
    #extraction5feature() #为区域密度，区域大小为4*4
    #extraction6feature() #为区域密度，区域大小为6*6
    modle1.model()
    modle2.model()
    pass


if __name__=="__main__":
    mainFuction()