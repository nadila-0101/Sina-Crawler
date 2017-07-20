#-*-coding:utf8-*-

import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
import shutil
import time
import csv
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

user_id = 2068548863
cookie = {"Cookie": "_T_WM=c0facfb77d67ef134b79f79ba020504b; WEIBOCN_WM=3333_2001; SCF=AkwFYA0S2oimMZt7R7pfg5DcMsCwA5f70SoDiHkmI7iAr8SXJhiN-ogbJme3w5k3qBNxHA2DR2KPTNzfjjcR_Rw.; SUB=_2A250YZQEDeThGedM4lAT8irFwziIHXVXrTxMrDV6PUJbkdANLW3ikW1Lwde8szKYyT3AAa9twAj5Rft_Zg..; SUHB=0KAgZPJxcKR5Bq; SSOLoginState=1499849812; M_WEIBOCN_PARAMS=uicode%3D20000174; H5_INDEX=0_all; H5_INDEX_TITLE=%E5%91%BC%E5%91%BC%E5%91%BC%E4%B8%801"}
url = 'https://weibo.cn/u/%d'%user_id
info_url = 'https://weibo.cn/%d/info'%user_id

content = requests.get(url, cookies = cookie).content
info_content = requests.get(info_url, cookies = cookie).content

print u'user_id和cookie读入成功'

soup = BeautifulSoup(content, 'lxml')
info_soup = BeautifulSoup(info_content, 'lxml')
weibo_content = soup.find_all('div', class_="c")

expression_list = []
topic_list = []
call_list =[]
weibo_list = ''

for weibo in weibo_content:
    try:
        weibo_text = weibo.find("span", class_="ctt").get_text()
        re.sub(" +", " ", weibo_text)
        weibo_list += weibo_text

        topic = re.findall("#.*?#", weibo_text)
        for topic_text in topic:
            topic_list.append(topic_text)

        expression = re.findall("\[.*?]", weibo_text)
        for expression_text in expression:
            expression_list.append(expression_text)

        call = re.findall("@{1}", weibo_text)
        for call_text in call:
            call_list.append(call_text)

    except AttributeError:
        print 'weibo is empty'

print '话题个数', len(topic_list)
print '表情个数', len(expression_list)
print '@个数', len(call_list)
print '###########',weibo_list

topic_num = len(topic_list)
expression_num = len(expression_list)
call_num = len(call_list)


# 保留数字
def trans2numbers(string):
    return int(''.join(a for a in string.strip() if a.isdigit()))

weibo_num_tag = soup.find("span", class_="tc").get_text()
follow_tag = soup.find("a", href="/%d/follow"%user_id).get_text()
fans_tag = soup.find("a", href="/%d/fans"%user_id).get_text()

weibo_num = trans2numbers(weibo_num_tag)
follow_num = trans2numbers(follow_tag)
fans_num = trans2numbers(fans_tag)

print '微博数量', weibo_num, '关注数量', follow_num, '粉丝数量', fans_num

user_info_list = info_soup.select('body > div:nth-of-type(7)')
user_info = user_info_list[0] if len(user_info_list) > 0 else 'null'
user_info_text = user_info.get_text()


print '用户信息',user_info_text

# csv文件的写入
# headers = ['id', 'weibo_num', 'follow_num', 'fans_num', 'expression_num', 'topic_num', 'call_num']
# rows = [{'id': user_id, 'weibo_num': weibo_num, 'follow_num': follow_num, 'fans_num': fans_num, 'expression_num': expression_num, 'topic_num': topic_num, 'call_num':call_num}]
#
# with open('data.csv', 'a+') as f:
#     f_csv = csv.DictWriter(f, headers)
#     # f_csv.writeheader()
#     f_csv.writerows(rows)

