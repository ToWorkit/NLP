import recall.gen_cf_data as gcf
import recall.config as conf

# 获取用户特征
user_feat_map_file = '../data/map/user_feat_map'

def gen_user_item_vector(user_id, vector_len = 55):
    user_feat_map = dict()
    with open(user_feat_map_file, 'r', encoding = 'utf-8') as f:
        user_feat_map = eval(f.read())

    print(user_feat_map)
    # 用户数据
    user_profile = conf.gen_user_profile()
    user_one_row = user_profile.loc[user_profile['user_id'] == user_id]
    print(user_one_row)
    user_feat_cols = user_one_row.columns[1:]
    print(user_feat_cols)
    feat_vector = [0.0 for i in range(vector_len)]
    print(feat_vector)
    for _, row in user_one_row.iterrows():
        for col_name in user_feat_cols:
            key = col_name + '_' + row[col_name]
            index = user_feat_map[key]
            feat_vector[index] += 1

    return feat_vector

user_profile = conf.gen_user_profile()
print(user_profile.loc[user_profile['user_id'] == '01a0ae50fd4b9ef6ed04c22a7e421000'])
print(gen_user_item_vector('01a0ae50fd4b9ef6ed04c22a7e421000'))