import numpy as np
import pandas as pd

data = [1, 2, 3, 4]
data = [i for i in data if i > 2 and i < 4]
print(data)
# 小数点向右移两位，并保留四位小数
print(format(2.12345618, '.4%'))

x = np.random.randn(10)
# 各项加1
print(x + 1)

D = pd.DataFrame([x, x + 1])
print(D)

D_t = pd.DataFrame([x, x + 1]).T
print(D_t)

print(np.arange(10))

d = [i for i in range(5)]
print(d)


import pandas as pd
data=[[1,2,3],[4,5,6], [7, 8, 9]]
index=['a','b','f']#行号
columns=['c','d','e']#列号
df=pd.DataFrame(data,index=index,columns=columns)#生成一个数据框
print(df)
# 取下标为 2 的数据
print(df.iloc[:, 2])

# 各项乘积 
print(pd.Series([1, 2, 3, 4]).prod())
