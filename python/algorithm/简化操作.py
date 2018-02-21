# 原始
a = [1, 2, 3]
b = []
for i in a:
  b.append(i)
print(b)

# 简化
a = [3, 4, 5]
b = [ i + 1 for i in a]
print(b)

# set 简写 -> 自动去重
sl = {1, 2, 3, 1, 2, 4}
print(sl)
