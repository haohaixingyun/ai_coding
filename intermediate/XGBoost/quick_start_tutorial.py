import xgboost as xgb
import numpy as np
data = np.random.rand(5,10)
label = np.random.randint(2,size=5)
dtrain = xgb.DMatrix(data,label=label)
dtest = dtrain
param = {'bst:max_depth':2 ,'bst:eta':1,'silent':1,'objective':'binary:logistic'}
param['nthread'] = 4
param['eval_metric']='auc'
evallist = [(dtest,'eval'),(dtrain,'train')]
num_round = 100
bst = xgb.train(param,dtrain,num_round,evallist)

