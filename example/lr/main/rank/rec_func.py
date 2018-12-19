import recall.config as conf
import math

def rec_func(user_id = '012457193169d597b9c531cd7842e3c1'):
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

    # 对应有值的index
    (age_idx, gender_idx, salary_idx, province_idx) = (category_feat_dict['age_' + age],
                                                       category_feat_dict['gender_' + gender],
                                                       category_feat_dict['salary_' + salary],
                                                       category_feat_dict['province_' + province])

    print('age: '+age,'gender: ' + gender,'salary: ' + salary,'province:' + province)
    rec_list = []
    for item_id in rec_item_all.keys():
        item_df = conf.gen_music_meta()
        location, item_name = '', ''
        for _, row in item_df.loc[item_df['item_id'] == int(item_id), :].iterrows():
            location,item_name = row['location'], row['item_name']

        location_idx = category_feat_dict['location_' + location]

        ui_key = user_id + '_' + item_id
        # score
        cross_value = float(cross_feat_dict.get(ui_key, 0))

        # 预测 predict y = wx + b
        wx_score = float(b)
        # category feat 获取对应属性值的权重(离散值)
        wx_score += W[age_idx] + W[gender_idx] + W[salary_idx] + W[province_idx] + W[location_idx]
        # continuous feat 连续值(分数)权重[再乘以打分值]
        wx_score += W[-1] * cross_value

        # sigmoid: p(y=1|x) = 1 / (1 + exp(-wx))
        final_rec_score = 1 / (1 + math.exp(-(wx_score)))
        score = rec_item_all[item_id]['score']
        # 最终打分 二次打分
        final_rec_score = 0.3 * final_rec_score + 0.7 * score

        explain = rec_item_all[item_id]['recall']
        rec_list.append((item_id, item_name, final_rec_score, explain))

    # step 5 排序
    rec_sort_list = sorted(rec_list, key = lambda x:x[2], reverse = True)

    # step 6 topN (取5个)
    rec_filter_list = rec_sort_list[:5]

    # step 7 返回
    ret_list = ['->'.join([i_id, name, str(score), explain]) for i_id, name, score, explain in rec_filter_list]
    print('\n'.join(ret_list))
    return ret_list

rec_func()

