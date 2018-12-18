# -*- coding :utf-8 -*-


"""
we already have know that the sklearn has svm ML lib , so it's confuse used the libsvm in method 1

in this method we will use this lib to re-realization the svm process

I think must of steps will same ,just copy them from method 1 only different the svm modle

"""

from sklearn import svm

import  numpy as np
from skimage import io
import matplotlib.pyplot as plt

# scikit-learn已经有了模型持久化的操作，导入joblib即可
from sklearn.externals import joblib

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
    with open('../txt/ethan_sample.txt','r') as fp:
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
    model = svm.SVC(kernel='poly',gamma = 0.1,degree = 1 )

    """
    very fuck  ,kernel='poly' 影响特别重大  下面分析下这个到底是猫东西  ，没找到相关的资料 NND 
    
    """

    model.fit(featuretrain,classtrain)
    joblib.dump(model , '../txt/svm_job_modle.m')   #  模型的持久化
    model = joblib.load( '../txt/svm_job_modle.m')  #  模型的重载
    class_predict = model.predict(featuretest)
    print(class_predict)
    print(classtest)
    #print(y_predict.tolist())
    def_error_list = []
    lens = len(class_predict)
    for x  in range(lens):
        if class_predict[x] != classtest[x]:
            def_error_list.append(x)
    print("错误list 的长度为 ： " , len(def_error_list))
    for x in range(len(def_error_list)):
        err_index = allclass.index(class_predict[def_error_list[x]])
        true_index = allclass.index(classtest[def_error_list[x]])
        #print(err_index,true_index)
        err_value = indexInfo[err_index]
        tru_value = indexInfo[true_index]
        filename = nametest[def_error_list[x]]
        err_data = io.imread('../aftImage/'+filename)
        io.imshow(err_data)
        plt.show()

        #print(err_value,tru_value)
        print(tru_value + " 被识别成了 "+err_value)



if __name__=="__main__":
    model()