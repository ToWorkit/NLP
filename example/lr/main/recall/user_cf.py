import operator
import math

'''
    基于用户的协同过滤
    train数据集格式
        {user_id: {item_id: rating}}
'''


def user_similarity(train):
    # 建立item -> users倒排表
    # 商品的所有购买用户
    item_users = dict()
    for u, items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    # 计算相似user共同的物品数量
    C = dict()  # 用户之间的共同物品数量 (交集)
    N = dict()  # 一个用户的所有物品个数 (分母)
    for i, users in item_users.items():
        for u in users:
            if N.get(u) == None:
                N[u] = 0
            N[u] += 1
            if C.get(u) == None:
                C[u] = dict()
            for v in users:
                # 过滤掉相同用户
                if u == v:
                    continue
                elif C[u].get(v) == None:
                    C[u][v] = 0
                C[u][v] += 1

    # 最终的相似度矩阵
    W = dict()
    for u, related_users in C.items():
        if W.get(u) == None:
            W[u] = dict()
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v] * 1.0)

    return W


# 相似用户的推荐物品集合
def recommend(user, train, w, k):
    rank = dict()
    # 获取用户购买过的item集合(item_id)
    iteracted_items = train[user].keys()
    # 对相似用户进行排序取TOPN(相似度)
    sortSimUser = sorted(w[user].items(), key=operator.itemgetter(1), reverse = True)[0:k]
    for v, wuv in sortSimUser:
        # 获取用户购买过的item集合(item_id, rating)[打分]
        for i, rvi in train[v].items():
            # 过滤掉用户已经打过分的商品
            if i in iteracted_items:
                continue
            elif rank.get(i) == None:
                rank[i] = 0
            # 相似度 * 打分
            rank[i] += wuv * rvi

    return rank
