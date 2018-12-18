# -*- coding: utf-8 -*-

from  skimage import io,filters

def correctProcess():
    inputpci =[]
    with open('../txt/error.txt') as tf:
        for line in tf:
            inputpci.append(line.strip())
    lens = len(inputpci)
    for i in range(lens):
        pics = io.imread('../aftImage/'+inputpci[i])
        t = filters.threshold_otsu(pics)
        binary = (pics> t) * 1.0
        rw = binary.shape[0]
        cl = binary.shape[1]
        for x in range(rw):
            for j in range(cl):
                binary[x,j] = 1 - binary[x,j]
        io.imsave('../aftImage/'+inputpci[i],binary)
    pass

if  __name__ =='__main__':
    correctProcess()