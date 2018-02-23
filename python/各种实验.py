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
