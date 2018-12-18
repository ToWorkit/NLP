import recall.config as conf
import math

def rec_func(user_id = '00b4b743cf561e441063edbb5554d14f'):
    '''
        step1 载入特征处理
    '''
    # load user and item category feature
    # one-hot
    with open(conf.user_feat_map_file, 'r', encoding = 'utf-8') as f:
        category_feat_dict = eval(f.read())

    # load cross feature
    # userId_itemId: score
    with open(conf.cross_file, 'r', encoding = 'utf-8') as f:
        cross_feat_dict = eval(f.read())

    '''
        step2 载入模型
    '''
    # load LR Model
    with open(conf.model_file, 'r', encoding = 'utf-8') as f:
        model_dict = eval(f.read())
    W = model_dict['W']
    b = model_dict['b']

    '''
        step3 match(召回，协同过滤，召回候选集)
            3.1 CF
            3.1.1 user base
    '''
    rec_item_all = dict()
    with open(conf.cf_rec_lst_outfile, 'r', encoding = 'utf-8') as f:
        cf_rec_lst = eval(f.read())

    key = 'UCF_' + user_id
    ucf_rec_lst = cf_rec_lst[key]
    for item, score in ucf_rec_lst:
        rec_item_all[item] = {'score': score, 'recall': 'user_base'}

    # 3.1.2 item base
    key = 'ICF_' + user_id
    icf_rec_lst = cf_rec_lst[key]
    for item, score in icf_rec_lst:
        if rec_item_all.get(item, -1) == -1:
            rec_item_all[item] = {'score': score, 'recall': 'item_base'}
        else:
            rec_item_all[item]['score'] += float(score)
            rec_item_all[item]['recall'] = 'both'

    # 3.2 CB
    '''
        step4 调取用户和物品服务
    '''
    # 4.1 用户属性
    user_df = conf.gen_user_profile()
    age, gender, salary, province = '', '', '', ''
    for _, row in user_df.loc[user_df['user_id'] == user_id, :].iterrows():
        age, gender, salary, province = row['age'], row['gender'], row['salary'], row['province']

    (age_idx, gender_idx, salary_idx, province_idx) = (category_feat_dict['age_' + age],
                                                       category_feat_dict['gender_' + gender],
                                                       category_feat_dict['salary_' + salary],
                                                       category_feat_dict['province_' + province])

    print('age: '+age,'gender: ' + gender,'salary: ' + salary,'province:' + province)


rec_func()

