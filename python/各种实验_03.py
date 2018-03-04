import numpy as np
import pandas as pd

str_l = [
  [1, 2, 3, 4],
  [2, 3, 4, 5],
  [5, 6, 7, 8],
  [9, 3, 1, 5],
  [2, 4, 1, 5],
  [5, 6, 2, 8],
  [0, 9, 8, 1],
  [4, 5, 2, 1]
]
# 转为矩阵
str_l = np.array(str_l)
print(type(str_l))
# 80% 训练集，20% 测试集
train = str_l[:int(len(str_l) * 0.8), :]
test = str_l[int(len(str_l) * 0.8):, :]

print(train)
print('-' * 20)
print(test)


# 切片
li_ = [1, 2, 3, 4, 5, 6, 7, 8 ,9]

# 含头不含尾
print(li_[2:])
print(li_[:2])
