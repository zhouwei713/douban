# coding = utf-8
"""
@author: zhou
@time:2019/1/3 11:10
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_praise():
    praise_list = []
    for i in range(0, 2000, 20):
        url = 'https://movie.douban.com/subject/3878007/comments?start=%s&limit=20&sort=new_score&status=P&percent_type=h' % str(i)
        req = requests.get(url).text
        content = BeautifulSoup(req, "html.parser")
        check_point = content.title.string
        if check_point != r"没有访问权限":
            comment = content.find_all("span", attrs={"class": "short"})
            for k in comment:
                praise_list.append(k.string)
        else:
            break
    return praise_list


def get_ordinary():
    ordinary_list = []
    for i in range(0, 2000, 20):
        url = 'https://movie.douban.com/subject/3878007/comments?start=%s&limit=20&sort=new_score&status=P&percent_type=m' % str(i)
        req = requests.get(url).text
        content = BeautifulSoup(req, "html.parser")
        check_point = content.title.string
        if check_point != r"没有访问权限":
            comment = content.find_all("span", attrs={"class": "short"})
            for k in comment:
                ordinary_list.append(k.string)
        else:
            break
    return ordinary_list


def get_lowest():
    lowest_list = []
    for i in range(0, 2000, 20):
        url = 'https://movie.douban.com/subject/3878007/comments?start=%s&limit=20&sort=new_score&status=P&percent_type=l' % str(i)
        req = requests.get(url).text
        content = BeautifulSoup(req, "html.parser")
        check_point = content.title.string
        if check_point != r"没有访问权限":
            comment = content.find_all("span", attrs={"class": "short"})
            for k in comment:
                lowest_list.append(k.string)
        else:
            break
    return lowest_list


if __name__ == "__main__":
    print("Get Praise Comment")
    praise_data = get_praise()
    print("Get Ordinary Comment")
    ordinary_data = get_ordinary()
    print("Get Lowest Comment")
    lowest_data = get_lowest()
    print("Save Praise Comment")
    praise_pd = pd.DataFrame(columns=['praise_comment'], data=praise_data)
    praise_pd.to_csv('praise.csv', encoding='utf-8')
    print("Save Ordinary Comment")
    ordinary_pd = pd.DataFrame(columns=['ordinary_comment'], data=ordinary_data)
    ordinary_pd.to_csv('ordinary.csv', encoding='utf-8')
    print("Save Lowest Comment")
    lowest_pd = pd.DataFrame(columns=['lowest_comment'], data=lowest_data)
    lowest_pd.to_csv('lowest.csv', encoding='utf-8')
    print("THE END!!!")


