import operator
a = [1, 2, 3, 1]
b = [4, 5, 6]
print(operator.eq(a, b))
'''
lt(a,b) 相当于 a<b     从第一个数字或字母（ASCII）比大小 

le(a,b)相当于a<=b

eq(a,b)相当于a==b     字母完全一样，返回True,

ne(a,b)相当于a!=b

gt(a,b)相当于a>b

ge(a,b)相当于 a>=b
'''

# 统计次数
print(a.count(1))
