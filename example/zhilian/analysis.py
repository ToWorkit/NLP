import csv
import matplotlib.pyplot as plt

filename_csv = '北京地区python工程师岗位招聘详情.csv'

def read_csv_column(path, column):
  '''
    读取列
  '''
  with open(path, 'r', encoding='utf8', newline='') as f:
    reader = csv.reader(f)
    return [row[column] for row in reader]

# 薪资
salaries = []
# 读取
sal = read_csv_column(filename_csv, 3)
# 将表头去掉并转为整型
for i in range(len(sal) - 1):
  # 为0的是面议不做处理
  if not sal[i] == '0':
    salaries.append(int(sal[i + 1]))
print(salaries)
plt.hist(salaries, bins=10 ,)
plt.show()
