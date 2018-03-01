# 对两个已经排序的列表进行合并，要求合并后的元素不重复，并且排序

list_ = [1, 2, 3, 4, 5, 6, 1, 2]
list_1 = [4, 5, 6, 7, 8, 9, 4, 5]

# 原生函数的方法
def first_sort(a, b):
  st = sorted(set(a) | set(b))
  return st
# print(first_sort(list_, list_1))

# a = list_.copy()
# print(a)

# enumerate -> 枚举 => 获取index
print(list(enumerate(list_)))

print
# 原生敲
def second_sort(a, b):
  res = a.copy()
  for b_item in b:
    # 去除重复元素
    if b_item in res:
      continue
    # enumerate -> 枚举 => 获取index
    for (i, res_item) in enumerate(res[:]):
      if b_item > res_item:
        # 如果是末尾
        if i == len(res) - 1:
          res.append(b_item)
        else:
          continue
      if b_item <= res_item:
        res.insert(i, b_item)
        break
  return res
print(second_sort(list_, list_1))


# 测试
import random
def main():
  # 随机生成两个长度不相等的列表，并且进行排序
  first = sorted(random.sample(range(100), random.randint(3, 6)))
  second = sorted(random.sample(range(100), random.randint(3, 6)))

  first_s = first_sort(first, second)
  print('first:', first)
  print('second:', second)
  print('first_s:', first_s)

  second_s = second_sort(first, second)
  print('second_s:', second_s)
  # 断言，如果不为True则会报出错误
  assert first_s == second_s
if __name__ == '__main__':
  main()
