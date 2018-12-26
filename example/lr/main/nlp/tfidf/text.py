import numpy as np
import jieba
import math
s1 = "我吃饱了，不饿了"
s1_cut = [i for i in jieba.cut(s1, cut_all = True) if i != '']
s2 = "我没有吃饱，好饿啊"
s2_cut = [i for i in jieba.cut(s2, cut_all = True) if i != '']
print(s1_cut)
print(s2_cut)
# 词库
word_set = set(s1_cut).union(set(s2_cut))
print(word_set)

word_dict = dict()
i = 0
for word in word_set:
    word_dict[word] = i
    i += 1
print(word_dict)

# [0, 0, 0, 0, 0, 0, 0, 0]
s1_cut_code = [0] * len(word_dict)
for word in s1_cut:
    s1_cut_code[word_dict[word]] += 1
print(s1_cut_code)

s2_cut_code = [0] * len(word_dict)
for word in s2_cut:
    s2_cut_code[word_dict[word]] += 1
print(s2_cut_code)

s2_np = np.array([i * i for i in s2_cut_code])
s2_np_sum = np.sum(s2_np)

s2_e = [i / math.sqrt(s2_np_sum) for i in s2_cut_code]
s2_e_sum = np.sum([i * i for i in s2_e])
print(s2_e)
print(s2_e_sum)

