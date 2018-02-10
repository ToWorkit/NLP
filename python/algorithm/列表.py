from timeit import Timer
# concat  0.07136099214578559 milliseconds
def test_0():
  list_ = []
  '''
    l = []
    l += [2]
    l += [3]
    print(l)
    >>> [2, 3]
  '''
  for i in range(1000):
    list_ += [i]

# append  0.0794551471521817 milliseconds
def test_1():
  list_ = []
  for i in range(1000):
    list_.append(i)

# comprehension  0.02942634062962049 milliseconds
def test_2():
  list_ = [i for i in range(1000)]

# list range  0.01282333956336959 milliseconds
def test_3():
  list_ = list(range(1000))
  
# https://facert.gitbooks.io/python-data-structure-cn/2.%E7%AE%97%E6%B3%95%E5%88%86%E6%9E%90/2.6.%E5%88%97%E8%A1%A8/
t1 = Timer("test_0()", "from __main__ import test_0")
print("concat ",t1.timeit(number=1000), "milliseconds")

t2 = Timer("test_1()", "from __main__ import test_1")
print("append ",t2.timeit(number=1000), "milliseconds")

t3 = Timer("test_2()", "from __main__ import test_2")
print("comprehension ",t3.timeit(number=1000), "milliseconds")

t4 = Timer("test_3()", "from __main__ import test_3")
print("list range ",t4.timeit(number=1000), "milliseconds")
