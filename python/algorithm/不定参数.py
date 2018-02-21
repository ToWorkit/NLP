def foo(x, y, *pas):
  # 储存不展开
  print(x, y, pas)

foo(1, 2)

foo(1, 2, 3, 4, 5)


def foo_2(x, y, *pas):
  # 解构展开
  print(x, y, *pas)

foo_2(1, 2)

foo_2(1, 2, 3, 4, 5)

# 默认值
def foo_3(x, y = 1, **pas):
  # 解构展开
  print(x, y, pas)

# 依旧以传入的值为主
foo_3(1, 2)
dic = {'name': 'ml', 'age': 20}
foo_3(1, 2, **dic)
foo_3(1, 2, name = 'ml', age = 20)


def multiple(arg, *args, **dictargs):
    print("arg: ", arg)
    # 打印args
    for value in args:
      print("other args:", value)
    # 打印dict类型的不定长参数 args
    for key in dictargs:
      print("dictargs:" + str(dictargs[key]) + '_' + key)
 
if __name__ == '__main__':
    multiple(1,'a',True, name='Amy',age=12)
