'''
即使 s1,s2 不同，它们都是由完全相同的字符组成的。所以，我们按照字母顺序从 a 到 z 排列每个字符串，如果两个字符串相同，那这两个字符串就是乱序字符串
'''
def anagramSolution(s1, s2):
  alist1 = list(s1)
  alist2 = list(s2)
  # 排序
  alist1.sort()
  alist2.sort()
  pos = 0
  matches = True
  while pos < len(s1) and matches:
    if alist1[pos] == alist2[pos]:
      pos = pos + 1
    else:
      matches = False
  return matches
print(anagramSolution('abcde','edcba'))
print(anagramSolution('abcde','adcba'))
