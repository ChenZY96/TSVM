#coding=utf-8
import TSVM
import numpy as np
import pandas as pd
from collections import Counter
import joblib

X1 = np.loadtxt('train_data.csv',usecols=(1,2,3,4),skiprows=1,delimiter=',')
#print(X1[:10])
print('train_data feature shape:',X1.shape)
Y1 = np.loadtxt('train_data.csv',usecols=(5),skiprows=1,delimiter=',')
Y1 = np.expand_dims(Y1, 1)
#print(Y1[:10])
print('train_data label shape:',Y1.shape)
X2 = np.loadtxt('combine_data.csv',usecols=(1,2,3,4),skiprows=1,delimiter=',')
#print(X2[:10])
print('rest_data feature shape:',X2.shape)

model = TSVM.TSVM()
model.initial(kernel='linear')
model.train(X1,Y1,X2)
Y_hat = model.predict(X2)
#print(len(Y_hat))
print('predict result:',Counter(Y_hat))

data = pd.read_csv('combine_data.csv')
data['label'] = Y_hat
data.to_csv('result.csv',index=None)
#print(data.head())

# validate
data = pd.read_csv('result.csv')
abnormal_user = joblib.load('abnormal_user.pkl')
res = []
for each in abnormal_user:
    #print(each)
    tmp = data[data['_id'] == str(each)]['label'].values[0]
    res.append(tmp)
#print(res)
# -1 presents normal user and 1 presents abnormal user
print('abnormal result count:',Counter(res))
        

