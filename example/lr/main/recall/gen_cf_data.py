import recall.config as conf
import pandas as pd

train_file = conf.cf_train_data_path

# 数据集
def user_item_score():
    # 读取10000条
    user_watch = conf.get_user_watch(10000)
    # 取music_meta中商品总共的时长
    music_meta = conf.get_music_meta()
    # print(user_watch)
    # print(music_meta)

    # 将用户记录和商品信息关联起来
    data = user_watch.merge(music_meta, how = 'inner', on = 'item_id')
    del user_watch
    del music_meta

    # 添加score列(横轴 axis = 1) 听的时间 / 商品总时长
    data['score'] = data.apply(lambda x: float(x['stay_seconds']) / float(x['total_timelen']), axis = 1)
    # 通过key取值
    data = data[['user_id', 'item_id', 'score']]
    # 对相同user_id和item_id的打分求和(用户可能在不同时间段听了不同的时长) 9999 => 8361
    data = data.groupby(['user_id', 'item_id']).score.sum().reset_index()
    return data

# 处理为 {user_id: {item_id: rating}}
def train_from_df(df, col_name = ['user_id', 'item_id', 'score']):
    train = dict()
    for _, row in data.iterrows():
        user_id = str(row[col_name[0]])
        item_id = str(row[col_name[1]])
        rating = row[col_name[2]]
        if train.get(user_id, -1) == -1:
            train[user_id] = dict()
        train[user_id][item_id] = rating
    return train

data = user_item_score()
train = train_from_df(data)

# 写出
with open(train_file, 'w', encoding = 'utf-8') as f:
    f.write(str(train))