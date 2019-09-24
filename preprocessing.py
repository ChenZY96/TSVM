#coding=utf-8
import numpy as np
import pandas as pd
from pymongo import MongoClient
import joblib
import os
import re
from bson import ObjectId
client = MongoClient(host='192.168.58.59',port=27017)
db = client.dataset_release
collection = db.users

# all users' uid
user_path = 'all_users.pkl'
if os.path.exists(user_path):
    all_users = joblib.load(user_path)
else:
    all_users = set()
    all_users_id = collection.find({},{'_id':1})
    for each in all_users_id:
        user = each['_id']
        #print(user)
        all_users.add(user)
    joblib.dump(all_users,user_path)
print('all users:',len(all_users))

# all abnormal users's uid
abnormal_user_path = 'abnormal_user.pkl'
if os.path.exists(abnormal_user_path):
    abnormal_users = joblib.load(abnormal_user_path)
else:
    abnormal_users = set()
    ab_u = collection.find({'generated':True},{'_id':1})
    for each in ab_u:
        user = each['_id']
        abnormal_users.add(user)
    joblib.dump(abnormal_users,abnormal_user_path)
print('all abnormal users:',len(abnormal_users))

# all normal users' uid
normal_user_path = 'normal_user.pkl'
if os.path.exists(normal_user_path):
    normal_users = joblib.load(normal_user_path)
else:
    normal_users = all_users - abnormal_users
    joblib.dump(normal_users,normal_user_path)
print('all normal users:',len(normal_users))
    
# all users' feature array
my_array = np.loadtxt('combine_data.csv',usecols=(1,2,3,4),skiprows=1,delimiter=',')
#print(my_array[:10])

# train data  for semi-supervised learning
normal_sample = 5780
ab_sample = 20

data = pd.read_csv('combine_data.csv')
#print(data.head())
normal_list = list(normal_users)[:normal_sample]
#print(len(normal_list))
abnormal_list = list(abnormal_users)[:ab_sample]


# 5780 normal users for training
tmp1 = []
for each in normal_list:
    tmp1.append(str(each))
normal_data = data[data._id.isin(tmp1)]
print('normal user for training:',len(normal_data))
normal_data['label'] = -1
normal_data.to_csv('train_normal.csv',index=None)
# 20 abnormal users for training
tmp2 = []
for each in abnormal_list:
    tmp2.append(str(each))
abnormal_data = data[data._id.isin(tmp2)]
print('abnormal users for training',len(abnormal_data))
abnormal_data['label'] = 1
abnormal_data.to_csv('train_abnormal.csv',index=None)

## rest users
#tmp3 = []
#for each in all_users:
#    tmp3.append(str(each))
#a = list(set(tmp3).difference(set(tmp1)))
#test_users = list(set(a).difference(set(tmp2)))
#test_data = data[data._id.isin(test_users)]
##print('test_data:',len(test_data))
#test_data.to_csv('test_data.csv',index=None)

# final training_data for SSL
df1 = pd.read_csv('train_normal.csv')
df2 = pd.read_csv('train_abnormal.csv')

train_data = pd.concat([df1,df2],axis=0,ignore_index=True)
print('final training data:',len(train_data))
train_data.to_csv('train_data.csv',index=None)


