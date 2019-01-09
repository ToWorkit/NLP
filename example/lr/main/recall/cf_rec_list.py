'''
    保存推荐列表
'''
import recall.item_cf as ic
import recall.user_cf as uc
import recall.config as conf
import operator

item_item_sim_file = conf.item_item_sim_file
user_user_sim_file = conf.user_user_sim_file

UCF_PREFIX = conf.UCF_PREFIX
ICF_PREFIX = conf.ICF_PREFIX

cf_rec_lst_outfile = conf.cf_rec_lst_outfile

# load CF train data
train = {}
with open(conf.cf_train_data_path, 'r', encoding = 'utf-8') as f:
    train = eval(f.read())
print("CF train loaded, start similarity")

# 要推荐的商品topN
reclst = dict()
'''
    基于用户的协同过滤 user base cf
'''
# 用户相似度矩阵
user_user_sim = uc.user_similarity(train)
with open(user_user_sim_file, 'w', encoding = 'utf-8') as uuf:
    uuf.write(str(user_user_sim))
# 8G内存
print("user base cf similarity saved")
for user_id in train.keys():
    rec_item_list = uc.recommend(user_id, train, user_user_sim, 10)
    user_id = UCF_PREFIX + user_id
    reclst[user_id] = sorted(rec_item_list.items(), key = operator.itemgetter(1), reverse = True)[:20]
print("user base cf done, item base cf starting")

'''
    基于物品的协同过滤 item base cf
'''
# 商品相似度矩阵
item_item_sim = ic.item_similarity(train)
with open(item_item_sim_file, 'w', encoding = 'utf-8') as iif:
    iif.write(str(item_item_sim))
print("item base cf similarity saved")
for user_id in train.keys():
    item_list = ic.recommend(train, user_id, item_item_sim, 10)
    user_id = ICF_PREFIX + user_id
    reclst[user_id] = sorted(item_list.items(), key = operator.itemgetter(1), reverse = True)[:20]

with open(cf_rec_lst_outfile, 'w', encoding = 'utf-8') as rcf:
    rcf.write(str(reclst))
# 5G
print("user topN and item topN saved")
