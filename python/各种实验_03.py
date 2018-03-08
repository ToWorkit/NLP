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
print(len(str_l))

print(train[:, :3].reshape(2, 9))


# 切片
li_ = [1, 2, 3, 4, 5, 6, 7, 8 ,9]

# 含头不含尾
print(li_[2:])
print(li_[:2])

import time

# dt = "2016-05-05 20:28:54"
dt = "2014/03/31"
# http://blog.csdn.net/google19890102/article/details/51355282
# 转换成时间数组
# timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
timeArray = time.strptime(dt, "%Y/%m/%d")
# 转换为时间戳
dt_new = time.mktime(timeArray)

print(dt_new)


def test(ti_1, ti_2):
    # strptime -> 转换为时间数组
    # mktime -> 转换为时间戳
    return time.mktime(time.strptime(ti_1, '%Y/%m/%d')) - time.mktime(time.strptime(ti_2, '%Y/%m/%d'))

print(test('2014/03/31', '2006/11/02') / 60 / 60 / 24 / 30)


data = np.array([[1, 2, 3, 4, 5], [6, 4, 3, 2, 1], [6, 4, 3, 2, 8], [8, 7, 6, 4, 2], [0, 0, 2, 3, 1]])
print(type(data))
# 从 下标为 2 的位置开始截取，一直取到结尾(含头)
print(data[:, 2:])
# 尾部只能取 负值
print(data[:, 2:-1])
print('-' * 30)
# 取索引为 0 列的数据
print(data[:, 0])
