import operator
import math

'''
    基于物品的协调过滤
    train数据集格式
        {user_id: {item_id: rating}}
'''

def item_similarity(train):
    # 计算item1与item2相同的user数量
    C = dict() # 存储item与item相同user的个数(分子)
    N = dict() # 一个item的购买用户总数(分母)
    for u, items in train.items():
        for i in items:
            if N.get(i) == None:
                N[i] = 0
            N[i] += 1
            if C.get(i) == None:
                C[i] = dict()
            for j in items:
                # 过滤掉相同物品
                if i == j:
                    continue
                elif C[i].get(j) == None:
                    C[i][j] = 0
                C[i][j] += 1

    # 计算商品的相似度(根据相同的用户数量)
    W = dict()
    for i, related_items in C.items():
        if W.get(i, -1) == -1:
            W[i] = dict()
        for j, cij in related_items.items():
            if W[i].get(j, -1) == -1:
                W[i][j] = 0
            # 相似用户个数 / 两个相似商品各自用户个数的乘积再开方
            W[i][j] += cij / math.sqrt(N[i] * N[j] * 1.0)
    return W

# 相似商品的推荐商品集合
def recommend(train, user, w, k):
    rank = dict()
    ru = train[user]
    for i, pi in ru.items():
        # 对相似商品排序取TOPN
        for j, wj in sorted(w[i].items(), key = operator.itemgetter(1), reverse = True)[0:k]:
            # 过滤相同的商品
            if j in ru:
                continue
            elif rank.get(j, -1) == -1:
                rank[j] = 0
            # 商品的打分 * 商品的相似度
            rank[j] += pi * wj
    return rank
