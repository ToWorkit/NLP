# 使用封闭方程的方法计算求和，而不是迭代来计算前n个数的和
# https://facert.gitbooks.io/python-data-structure-cn/2.%E7%AE%97%E6%B3%95%E5%88%86%E6%9E%90/2.2.%E4%BB%80%E4%B9%88%E6%98%AF%E7%AE%97%E6%B3%95%E5%88%86%E6%9E%90/
# https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF
def sum(n):
  return (n * (n + 1)) / 2
print(sum(100))

# 甩开传统求和近千倍
# sum += i

l = []
l += [2]
l += [3]
print(l)
_list = list(range(1000))
print(_list)

_li = [1, 2, 4]
print(_li.pop())
print(_li.pop(0))
