# -*- coding :utf-8 -*-

"""
为了在测试程序的时候我们能够准确的把握数据的正确率调整参数 ，我们需要固定我们的参数  确定哪些是测试数据 哪些是训练数据

否则出来的数据每次都是不同的 fuck 难以接受 毛线

"""
import random
import  numpy as np
def generator():

    linenum = 0
    train_sample = []
    rand_num = set()
    with open('../txt/Char_Index.txt','r') as fp :
        for line  in fp :
            if line[0] != "#" :
                linenum +=1
    print(linenum)
    # 生成 0 ，1 的随机 数据
    L = [random.randint(0,1) for _ in range(10)]

    w1000 = np.zeros(linenum)
    for x in range(linenum):
        train_sample.append(int(w1000[x]))

    while len(rand_num) < 800:
        v = random.randint(0, 999)
        rand_num.add(v)
    for x in range(len(rand_num)):
        w1000[list(rand_num)[x]] = 1
    with open('../txt/ethan_sample.txt','w+') as fp:
        for x in range(1000):
            if x < 999:
                fp.write(str(int(w1000[x])))
                fp.write(' ')
            else:
                fp.write(str(int(w1000[x])))
        pass

if __name__ == "__main__":
    generator()