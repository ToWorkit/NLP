#!/usr/bin/python
# -*- coding: UTF-8 -*-

import recall.gen_cf_data as gcf
import recall.config as conf
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

user_feat_map_file = conf.user_feat_map_file
cross_file = conf.cross_file
model_file = conf.model_file

# 获取处理后的数据集, 添加标签(根据分值的大小区分[作二分类])
data = gcf.user_item_score()
data['label'] = data['score'].apply(lambda x: 1 if x >= 1.0 else 0)

'''
user_id, item_id, label 添加用户和item的信息
'''
# 获取user信息表数据
user_profile = conf.get_user_profile()
# 获取item信息表数据
music_meta = conf.get_music_meta()
'''
print(user_profile[:10])
print("*" * 20)
print(music_meta[:10])
print("*" * 20)
print(data[:10])
'''
'''
user_profile 将用户信息根据user_id添加到data
music_meta 将商品信息添加(一个商品会有很多的共同用户)
'''
data = data.merge(user_profile, how='inner', on='user_id') \
    .merge(music_meta, how='inner', on='item_id')
# print("*" * 20)
# for u in data["user_id"]:
#     if u == "0000066b1be6f28ad5e40d47b8d3e51c":
#         print(u)
# print(data[:10]) === data.head(10)

# print(data[:10])

'''
划分特征种类
user_feat
    性别，年龄，收入，省份
item_feat
    总时长，地区
item_text_feat
    名称，标签(描述)
watch_feat
    用户收听时间，听的时长，打分(听的时长 / 商品总时长)
'''
user_feat = ['gender', 'age', 'salary', 'province']
item_feat = ['total_timelen', 'location']
item_text_feat = ['item_name', 'tags']
watch_feat = ['hours', 'stay_seconds', 'score']

# 离散特征
'''
可分类的任意数据属性都是离散值，这意味着它们属于某一特定的有限类别。在模型预测的属性或者响应变量（ response variables）中，经常被称为类别/标签。这些离散值在自然界中可以是文本或者数字（甚至是诸如图像这样的非结构化数据）
'''
category_feat = user_feat + ['location']
# 连续特征
'''
连续化特征就是一些不可枚举的有理数。 例如资产， 从0到正无穷你枚举不过来。 我们输入给模型算法的除了目标值(y或者说叫label，也叫标签)以外就只能是离散的，或者连续的。 
'''
continous_feat = ['score']

labels = data['label']
del data['label']

'''
特征处理
     比如在泰坦尼克号当中，有一个变量叫做乘客登陆的港口，取值为（C, Q, S）代表三个地方。这是一个典型的无序分类变量，我们在进行数据预处理的时候应该如何进行。 一种很容易想到的方法就是把每个值映射为一个数字，比如C=0, Q=1, S=2。 但是这样容易产生一个问题：我们实际上是把它们当做了有序的数字来进行看待了，2比1大，这就存在了顺序关系。但是我们的数据本来并不存在这样的关系。
  为了解决上面的问题，我们使用独热编码（One-Hot Encoding）对无序的分类变量进行处理。对于取值有m种情况的变量，我们用m维来表示。比如上面的变量可以取值100, 010，001， 仅当样本取值为第i种情况的时候，在第i维上面编码为1，其余维均编码为0。独热编码形成的变量也叫做虚变量或者哑变量（dummpy variable）
'''
# 1、离散特征作one-hot处理(有值或值无值作映射)
df = pd.get_dummies(data[category_feat])
one_hot_columns = df.columns
# 2、暂时不处理连续特征
df[continous_feat] = data[continous_feat].astype(float)

# print(df[:10])

# 保存组合特征
'''
ui-key
    user_id_item_id
'''
data['ui-key'] = data['user_id'].astype(str) + '_' + data['item_id'].astype(str)
cross_feat_map = dict()
for _, row in data[['ui-key', 'score']].iterrows():
    cross_feat_map[row["ui-key"]] = row['score']
# print(cross_feat_map)
with open(cross_file, 'w', encoding='utf-8') as cf:
    cf.write(str(cross_feat_map))

'''
划分数据集
    train 0.7 test 0.3
    x_train 数据 y_train 对应标签
'''
x_train, x_test, y_train, y_test = train_test_split(df.values, labels, test_size = 0.3, random_state = 2018)

'''
训练
    n_jobs=-1
        启动所有线程
    ovr
        二分类
'''
lr = LogisticRegression(penalty='l2', dual=False, tol=1e-4, C=1.0,
                        fit_intercept=True, intercept_scaling=1, class_weight=None,
                        random_state=None, solver='liblinear', max_iter=100,
                        multi_class='ovr', verbose=0, warm_start=False, n_jobs=-1)
model = lr.fit_transform(x_train, y_train)

'''
查看模型
    w 权值
    b 偏置值(截距)
'''
print("w: %s, b: %s" % (lr.coef_, lr.intercept_))
# 评价模型(平方差[保留两个小数点])
# 预测值 - 真实值
print("Residual sum of squatres: %.2f" % np.mean((lr.predict(x_test) - y_test) ** 2))
# 模型本身的评分
print("score: %.2f" % lr.score(x_test, y_test))


# print(lr.coef_.tolist())

'''
保存模型
'''
# 特征属性位置
feat_map = {}
for i in range(len(one_hot_columns)):
    key = one_hot_columns[i]
    feat_map[key] = i

with open(user_feat_map_file, 'w', encoding = 'utf-8') as f:
    f.write(str(feat_map))

# 保存模型
model_dict = {
    'W': lr.coef_.tolist()[0],
    'b': lr.intercept_.tolist()[0]
}

with open(model_file, 'w', encoding = 'utf-8') as m:
    m.write(str(model_dict))