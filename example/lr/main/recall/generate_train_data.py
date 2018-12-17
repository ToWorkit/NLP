import pandas as pd
import recall.user_cf
import operator
import recall.item_cf


data_path = '../raw_data/u.data'

udata = pd.read_csv(data_path,
                    sep='\t',
                    header=None,
                    names=['user_id', 'item_id', 'rating', 'timestamp'])

train = dict()
# for _,row in udata.iloc[:2,:].iterrows():
for _, row in udata.iterrows():
    user_id = str(row['user_id'])
    item_id = str(row['item_id'])
    rating = row['rating']
    if train.get(user_id, -1) == -1:
        train[user_id] = dict()
    train[user_id][item_id] = rating

# print(train)
W = user_cf.user_similarity(train)
# print(sorted(W.get('1').items(), key=operator.itemgetter(1), reverse=True)[:10])
rec_item_list = user_cf.recommend('1', train, W, 10)
print(sorted(rec_item_list.items(), key=operator.itemgetter(1), reverse=True)[:20])


# ###################item_cf test###################
W2 = item_cf.item_similarity(train)
item_list = item_cf.recommend(train,'1',W2,10)
print(sorted(item_list.items(), key=operator.itemgetter(1), reverse=True)[:20])