'''
我们对乱序问题的第一个解法是检查第一个字符串是不是出现在第二个字符串中。如果可以检验到每一个字符，那这两个字符串一定是乱序。可以通过用 None 替换字符来了解一个字符是否完成检查。但是，由于 Python 字符串是不可变的，所以第一步是将第二个字符串转换为列表。检查第一个字符串中的每个字符是否存在于第二个列表中，如果存在，替换成 None
'''
# https://facert.gitbooks.io/python-data-structure-cn/2.%E7%AE%97%E6%B3%95%E5%88%86%E6%9E%90/2.4.%E4%B8%80%E4%B8%AA%E4%B9%B1%E5%BA%8F%E5%AD%97%E7%AC%A6%E4%B8%B2%E6%A3%80%E6%9F%A5%E7%9A%84%E4%BE%8B%E5%AD%90/
def anagramSolution(s1, s2):
  # 由于python的字符串不可变行，所以先将第二个字符串转为列表
  alist = list(s2)
  # 次数
  pos1 = 0
  # 结果
  stillOk = True
  # 第一个字符串
  while pos1 < len(s1) and stillOk:
    pos2 = 0
    found = False
    # 第二个转为列表的字符串
    while pos2 < len(alist) and not found:
      # 检查第一个字符串中的每个字符是否存在于第二个列表中
      if s1[pos1] == alist[pos2]:
        found = True
      else:
        pos2 += 1
    # 如果存在，替换成 None
    if found:
      alist[pos2] = None
    else:
      print(1)
      stillOk = False
    pos1 += 1
  return stillOk, alist

print(anagramSolution('abcd','dcba'))
print(anagramSolution('abcd','acba'))
