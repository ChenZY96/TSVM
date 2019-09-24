# TSVM半监督分类
combine data.csv:原始数据，一共11596条（包括115596正常数据以及400个异常数据），每一行为该用户在四个域上的聚类结果

preprocessing.py:数据预处理，拆分数据集，5780个正常数据和20个异常数据用于半监督训练，生成train_data.csv，剩余数据在test_data.csv中(可以不生成)

TSVM.py:半监督SVM的实现

semi_svm.py:训练并预测，将结果存入result.csv

csv_to_mongo.py:将结果存入数据库
# 中间生成数据说明
abnormal_user.pkl：数据库中所有异常用户的uid,元组形式,一共115596个

normal_user.pkl：数据库中所有正常用户的uid,元组形式，一共400个

all_user.pkl：数据库中所有用户的uid,元组形式，一共115996个

train_normal.csv：用于训练的正常用户特征

train_abnormal.csv：用于训练的异常用户特征

train_data.csv：最终用于训练的5800个用户特征


