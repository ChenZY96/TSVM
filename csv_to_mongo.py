#coding=utf-8
from pymongo import MongoClient
from csv import DictReader
import pandas as pd
from bson import ObjectId

# 连接数据库
client = MongoClient(host='192.168.58.59', port=27017)
db = client.single_community_dataset
blog = db.TSVM_res


with open('result.csv',mode='r',encoding='utf-8') as f:
    data = DictReader(f)
    #tmp = {}
    for each in data:
        tmp = {}
       # each['uid'] = each.pop('_id')
        tmp['uid'] = ObjectId(each['_id'])
        tmp['label'] = int(eval(each['label']))
        tmp['user_community'] = int(eval(each['user_community']))
        tmp['tweet_community'] = int(eval(each['tweet_community']))
        tmp['blog_community'] = int(eval(each['blog_community']))
        tmp['ecommerce_community'] = int(eval(each['ecommerce_community']))
        #print(tmp)
        blog.insert_one(tmp)
print('Import to Mongo successfully')


    

