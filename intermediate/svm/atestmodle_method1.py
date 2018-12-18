# -*- coding :utf-8 -*-

import sys

PATH ='D:\sthself\ml\AI Academy aiacademy\模块一\FeatureExtraction\FeatureExtraction\libsvm-3.22\python'
sys.path.append(PATH)
from svmutil import *
import  numpy as np
from skimage import io
import matplotlib.pyplot as plt

def model():

    feature_1 = []
    with open('../txt/feature_1.txt','r') as fp:
        for line in fp :
            row=[]
            value = line.strip().split('\t')
            c1    = value[0]
            c2    = value[1].strip().split(',')
            lens  = len(c2)
            row.append(int(c1))
            for x in range(lens):
                row.append(int(c2[x]))
            feature_1.append(row)
            # fecature_1 的模式大概是 [[row1],[row2],[row3],[row4]]
    feature_1 = np.array(feature_1)
    feature_1 = feature_1[:,1:]    ### 这个地方fuck
    """
    The best way to know the fuck place is try to do some trial
    we define a fucntion :
    s = [[1,2,3],[4,5,6],[7,8,9]]
    x = np.array(s)
    x will be:
    array[[1,2,3],
          [4,5,6],
          [7,8,9]]
    x.shape will be (3,3) which meaning this is a 3 rows 3 columns data set
    will s.shape tell us list object has no attribute shape
    x[:,1:] which tell us keep all rows ,but the column wills start from the 1 index ,not from index 0 ,very funny
    """
    feature = feature_1.tolist()  #after remove the first column set it back to list not array

    classification_num  =13
    allclass = [10, 11, 12, 20, 22, 25, 26, 28, 30, 31, 32, 33, 34]
    indexInfo = ['京', '渝', '鄂', '0',  '2', '5', '6', '8', 'A', 'B', 'C', 'D', 'Q']

    train_num = 800
    selected_sample = []
    with open('../txt/selected_sample.txt','r') as fp:
        line = fp.readline()
        lineattr = line.strip().split(' ')
        for  i in range(len(lineattr)):
            selected_sample.append(int(lineattr[i]))

    rwno  = 0
    classtrain   = []   # define Y for train
    classtest    = []   # define Y for test

    featuretrain = []
    featuretest  = []

    nametrain    = []
    nametest     = []

    with open('../txt/Char_Index.txt','r') as fp:
        for line in fp :
            if line[0] !='#':
                lineattr = line.strip().split('\t')
                if selected_sample[rwno] ==1:     # 在 sample select 里面定义了 800 个 1  200 个 0
                    classtrain.append(int(lineattr[1]))
                    nametrain.append(lineattr[2])
                    featuretrain.append(feature[rwno])
                else:
                    classtest.append(int(lineattr[1]))
                    nametest.append(lineattr[2])
                    featuretest.append(feature[rwno])
                rwno +=1
    model = svm_train(classtrain, featuretrain, '-t 1 -d 1 -g 0.1 -r 0')
    """
    参数说明：
    -t  kernel_type : set type of kernel function (default 2)          here  1 -- polynomial: (gamma*u'*v + coef0)^degree 
    -d  degree : set degree in kernel function (default 3)             here  1 
    -g  gamma : set gamma in kernel function (default 1/num_features)  here 0.1 
    -r  coef0 : set coef0 in kernel function (default 0)               here 0
    
    """
    """
    model 保存和加载
    """
    svm_save_model("../txt/model_file",model)
    road_model = svm_load_model("../txt/model_file")
    pred_labels, (ACC, MSE, SCC), pred_values = svm_predict(classtest, featuretest, road_model)

    print('ACC = ' + str(ACC))
    print(pred_labels)
    print(pred_values)

    lens = len(classtest)
    err_index = []
    for  x  in range(lens):
        if int(pred_labels[x]) != classtest[x]:
            err_index.append(x)
    #print(err_index)
    for i in  range(len(err_index)):
        true_value = allclass.index(classtest[err_index[i]]) # 根据值 定义index  的位置
        errr_value = allclass.index(pred_labels[err_index[i]])
        print(indexInfo[true_value] +" 被识别成了 "+ indexInfo[errr_value])
        """
        the below section also very confused 
        """
        imgpath = '../preImage/' + nametest[err_index[i]]
        #io.imread(imgpath)
        io.imshow(imgpath)
        plt.show()

if __name__=="__main__":
    model()