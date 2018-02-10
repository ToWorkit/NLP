import jieba
import numpy as np
import pandas as pd
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

# 设置词云属性
color_mask = imread('timg.jpg')
wordcloud = WordCloud(
  font_path="simhei.ttf",   # 设置字体显示中文
  background_color = 'white', # 背景颜色
  max_words = 100,  # 词云最大显示的次数
  mask = color_mask,  # 设置背景图片
  max_font_size = 100,  # 字体最大值
  random_state = 42,
  width = 1000,
  height = 888,
  margin = 2, # 使用背景图片时设置默认大小
  )

filename_txt = '北京地区python工程师岗位招聘详情.txt'

def read_txt_file(path):
  '''
    读取txt文本
  '''
  with open(path, 'r', encoding='utf8', newline='') as f:
    return f.read()

content = read_txt_file(filename_txt)
# 返回列表形式
statistics = jieba.lcut(content)
# DataFrame 形式处理，名称 表头
words_df = pd.DataFrame({'statistics': statistics})

# 停用词处理
stopwords = pd.read_csv('StopWords.txt', index_col=False, quoting=3, sep=" ", names=['stopword'], encoding='utf8')
# ~ 取反向结果(停用词之外)
words_df = words_df[~words_df.statistics.isin(stopwords.stopword)]
# print(words_df)

# 获取数据并计数
words_stat = words_df.groupby(by=['statistics'])['statistics'].agg({'计数': np.size})
# 将计数列插入
words_stat = words_stat.reset_index().sort_values(by=['计数'], ascending=False)
# print(words_stat)

# 生成词云
# generate
word_frequence = {x[0]: x[1] for x in words_stat.head(6000).values}
word_frequence_dict = {}
# 取出generate格式数据
for key in word_frequence:
  word_frequence_dict[key] = word_frequence[key]

# generate_from_frequencies函数
wordcloud.generate_from_frequencies(word_frequence_dict)

# 从背景图片中生成颜色值
image_colors = ImageColorGenerator(color_mask)
# 重新对文字上色
wordcloud.recolor(color_func=image_colors)
# 保存图片
wordcloud.to_file('test.png')
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
