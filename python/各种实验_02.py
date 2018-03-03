import pandas as pd
print(pd.Series(1, [4, 5, 2, 7]))

list_ = ['a', 'b', 'c', None, 'd', None, 'e', None]

# l_ = [i for i in list_ if i != None]
# print(l_)

pd_li = pd.Series([1, 2, 3, 4, None, None, 5, None, 6])
print(pd_li)
# 取非空的值
print(pd_li[pd.notnull(pd_li)])
# 乘积
print(pd_li[pd.notnull(pd_li)].prod(), '----')



str_l = ['a', 'b', 'c', 'd', 'e']
x = list(map(lambda i: i.split('-->'), str_l))
print(x)
print(type('a'.split('--')))

a_ = pd.Series(['a', 'b', 'c', 'e'])
b_ = pd.Series(['a-->b', 'a-->c', 'a-->e', 'b-->c', 'c-->e'])
a_ = a_.append(b_)
print(a_)
