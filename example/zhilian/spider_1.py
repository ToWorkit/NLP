# -*- coding: utf-8 -*-
import re
import csv # csv 操作
import requests
from tqdm import tqdm # 进度条
from requests.exceptions import RequestException # 错误处理
from bs4 import BeautifulSoup # 解析html
# 模拟浏览器headers
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
  'Host': 'sou.zhaopin.com',
  'Referer': 'https://www.zhaopin.com/',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'zh-CN,zh;q=0.9'
}

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
  # 地址
  # 准换参数
  url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?'
  try:
    # 获取网页内容
    response = requests.get(url, params=params, headers=headers)
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
  # 匹配职位详情地址和职位名称
  # 匹配公司名称 
  # 匹配月薪 
  # 字符串换行，连写也可以
  pattern = re.compile('<td class="zwmc".*?href="(.*?)" target="_blank">(.*?)</a>.*?' 
        '<td class="gsmc">.*? target="_blank">(.*?)</a>.*?'
        '<td class="zwyx">(.*?)</td>', re.S)
  # 匹配所有符合条件的内容
  items = re.findall(pattern, html)
  # 将薪资处理为平均值
  for item in items:
    job_name = item[1]
    job_name = job_name.replace('<b>', '')
    job_name = job_name.replace('</b>', '')
    salary_avarge = 0
    temp = item[3]
    if temp != '面议':
      # 找到-下标
      _index = temp.find('-')
      # 平均工资
      salary_avarge = (int(temp[0:_index]) + int(temp[_index + 1:])) // 2
    yield {
      'job': job_name,
      'job_url': item[0],
      'company': item[2],
      'salary': salary_avarge,
    }

def get_detail_page(url):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Host': 'jobs.zhaopin.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
  }
  try:
    # 获取网页内容
    response = requests.get(url, headers=headers)
    # 通过返回的状态码判断是否获取成功
    if response.status_code == 200:
      return response.text
    return None
  except RequestException as err:
    return err


def get_job_detail(html):
  '''
    工作详情
  '''
  requirement = ''
  # 构建BeautifulSoup对象解析HTML
  soup = BeautifulSoup(html, 'html.parser')
  # 容器标签
  for ul in soup.find_all('ul', class_='terminal-ul clearfix'):
    # 8个子标签
    # 职位月薪|工作地点|发布日期|工作性质|工作经验|最低学历|招聘人数|职位类别
    lis = ul.find_all('strong')
    # 工作经验
    years = lis[4].get_text()
    # 最低学历
    education = lis[5].get_text()
  # 筛选任职要求
  for terminalpage in soup.find_all('div', class_='terminalpage-main clearfix'):
    for box in terminalpage.find_all('div', class_='tab-cont-box'):
      cont = box.find_all('div', class_='tab-inner-cont')[0]
      ps = cont.find_all('p')
      # 舍弃最后一个p标签
      for i in range(len(ps) - 1):
        # 去除换行符和空格
        requirement += ps[i].get_text().replace('\n', '').strip()
  # 筛选公司规模，取第一个li标签
  scale = soup.find(class_='terminal-ul clearfix terminal-company mt20').find_all('li')[0].strong.get_text()
  return {
    'years': years,
    'education': education,
    'requirement': requirement,
    'scale': scale
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
    # 如果写入数据为字典则写入一行，否则写入多行
    if type(rows) == type({}):
      # 一行一行的写
      f_csv.writerow(rows)
    else:
      f_csv.writerows(rows)

def write_txt_file(path, txt):
  '''
    写入txt文本
  '''
  with open(path, 'a', encoding='utf8', newline='') as f:
    f.write(txt)

def read_csv_column(path, column):
  '''
    读取列
  '''
  with open(path, 'r', encoding='utf8', newline='') as f:
    reader = csv.reader(f)
    return [row[column] for row in reader]

def main(city, keyword, region, pages):
  filename_csv = '{}地区{}岗位招聘详情.csv'.format(city, keyword)
  filename_txt = '{}地区{}岗位招聘详情.txt'.format(city, keyword)
  headers = ['job', 'years', 'education', 'salary', 'company', 'scale', 'job_url']
  # 写入csv文件头部
  # write_csv_headers(filename_csv, headers)

  # 进度条
  for i in tqdm(range(pages)):
    '''
      获取数据并写入csv
    '''
    job_dict = {}
    html = get_page(city, keyword, region, i)
    items = parse_page(html)
    for item in items:
      '''
        详情页
      '''
      html = get_detail_page(item.get('job_url'))
      job_detail = get_job_detail(html)

      job_dict['job'] = item.get('job')
      job_dict['years'] = job_detail.get('years')
      job_dict['education'] = job_detail.get('education')
      job_dict['salary'] = item.get('salary')
      job_dict['company'] = item.get('company')
      job_dict['scale'] = job_detail.get('scale')
      job_dict['job_url'] = item.get('job_url')

      # 清洗数据，将特殊字符等影响词频统计的因素剔除
      pattern = re.compile(r'[\u4e00-\u9fa5]+')
      filterdata = re.findall(pattern, job_detail.get('requirement'))
      '''
      write_txt_file(filename_txt, ''.join(filterdata))
      write_csv_rows(filename_csv, headers, job_dict)
      '''


if __name__ == '__main__':
  main('北京', 'python工程师', 2006, 10)
