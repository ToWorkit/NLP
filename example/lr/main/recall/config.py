'''
    配置文件和方法
'''
import os
import pandas as pd

data_path = "../raw_data/"

# data file
music_data = os.path.join(data_path, 'music_meta')
user_profile = os.path.join(data_path, 'user_profile.data')
user_watch_pref = os.path.join(data_path, 'user_watch_pref.sml')

# 相似度矩阵存储
sim_mid_data_path = '../data/sim_m_data/'
item_item_sim_file = os.path.join(sim_mid_data_path, 'item_sim.data')
user_user_sim_file = os.path.join(sim_mid_data_path, 'user_sim.data')

# cf train out file path
cf_train_data_path = '../data/cf_train.data'

# 区分前缀 prefix for user_id in recommend list
UCF_PREFIX = 'UCF_'
ICF_PREFIX = 'ICF_'

# recommend list out file
cf_rec_lst_outfile = '../data/cf_reclst.data'

# 特征数据和模型以及交叉验证数据集
user_feat_map_file = '../data/map/user_feat_map'
model_file = '../data/map/model_file'
cross_file = '../data/map/cross_file'

# item description data
def gen_music_meta(nrows=None):
    df_music_meta = pd.read_csv(music_data,
                                sep='\001',
                                nrows=nrows,
                                names=['item_id', 'item_name', 'desc', 'total_timelen', 'location', 'tags'])
    del df_music_meta['desc']
    # 空值替换为 -
    return df_music_meta.fillna('-')


# user profile data
def gen_user_profile(nrows=None):
    return pd.read_csv(user_profile,
                       sep=',',
                       nrows=nrows,
                       names=['user_id', 'gender', 'age', 'salary', 'province'])

# user action data
def gen_user_watch(nrows = None):
    return pd.read_csv(user_watch_pref,
                       sep = '\001',
                       nrows = nrows,
                       names = ['user_id', 'item_id', 'stay_seconds', 'hour'])