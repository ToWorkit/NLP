'''
利用两个乱序字符串具有相同数目的 a, b, c 等字符的事实。我们首先计算的是每个字母出现的次数。由于有 26 个可能的字符，我们就用 一个长度为 26 的列表，每个可能的字符占一个位置。每次看到一个特定的字符，就增加该位置的计数器。最后如果两个列表的计数器一样，则字符串为乱序字符串
'''
def anagramSolution(s1, s2):
  c1 = [0] * 26
  c2 = [0] * 26
  for i in range(len(s1)):
    '''
    >>> ord('a')
    对应的ASCII数值
    97
    '''
    pos = ord(s1[i]) - ord('a')
    c1[pos] += 1
  for i in range(len(s2)):
    pos = ord(s2[i]) - ord('a')
    c2[pos] += 1

  j = 0
  stillOk = True
  while j < 26 and stillOk:
    if c1[j] == c2[j]:
      j += 1
    else:
      stillOk = False
  return stillOk

print(anagramSolution('apple','pleap'))
