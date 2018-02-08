# -*- coding: utf-8 -*-
import re
import csv # csv 操作
import requests
from tqdm import tqdm # 进度条
from urllib.parse import urlencode
from requests.exceptions import RequestException # 错误处理
 
def get_page(city, keyword, region, page):
  '''
    获取网页内容信息
  '''
  # 所需参数
  params = {
    'jl': city,     # 搜索城市
    'kw': keyword,  # 关键字
    'isadv': 0,     # 更详细搜索选项参数
    'isfilter': 1,  # 过滤结果参数
    'p': page,      # 
    're': region    # 地区，朝阳 -> 2006
  }

  # 模拟浏览器headers
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Host': 'sou.zhaopin.com',
    'Referer': 'https://www.zhaopin.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
  }
  # 地址
  # 准换参数
  url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?' + urlencode(params)
  try:
    # 获取网页内容
    response = requests.get(url, headers = headers)
    # 通过返回的状态码判断是否获取成功
    if response.status_code == 200:
      return response.text
    return None
  except RequestException as err:
    return err

def parse_page(html):
  '''
    解析页面获取数据
  '''
  # 正则
  # 匹配职位信息
  # 匹配公司网址和公司名称 
  # 匹配月薪 
  # 字符串换行，连写也可以
  pattern = re.compile('<a style=.*? target="_blank">(.*?)</a>.*?'
        '<td class="gsmc"><a href="(.*?)" target="_blank">(.*?)</a>.*?'
        '<td class="zwyx">(.*?)</td>', re.S)
  # 匹配所有符合条件的内容
  items = re.findall(pattern, html)
  # 处理结果中的标签
  for item in items:
    job_name = item[0]
    job_name = job_name.replace('<b>', '')
    job_name = job_name.replace('</b>', '')
    yield {
      'job': job_name,
      'website': item[1],
      'company': item[2],
      'salary': item[3]
    }

def write_csv_headers(path, headers):
  '''
    写入表头
  '''
  # newline -> 防止每写一行都会多一个空行
  with open(path, 'a', encoding='utf8', newline='') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()

def write_csv_rows(path, headers, rows):
  '''
    写入行
  '''
  with open(path, 'a', encoding='utf8', newline='') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writerows(rows)

def main(city, keyword, region, pages):
  filename = '{}地区{}岗位招聘详情.csv'.format(city, keyword)
  headers = ['job', 'website', 'company', 'salary']
  write_csv_headers(filename, headers)
  # 进度条
  for i in tqdm(range(pages)):
    '''
      获取数据并写入csv
    '''
    jobs = []
    html = get_page(city, keyword, region, i)
    items = parse_page(html)
    for item in items:
      jobs.append(item)
    # 当页数据写入
    write_csv_rows(filename, headers, jobs)

if __name__ == '__main__':
  main('北京', 'python工程师', 2006, 10)
