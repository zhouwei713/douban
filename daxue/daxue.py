# coding = utf-8
"""
@author: zhou
@time:2019/6/14 13:50
"""


import requests
from bs4 import BeautifulSoup


def get_data():
    url = 'http://college.gaokao.com/schlist'
    res = requests.get(url).text
    content = BeautifulSoup(res, "html.parser")
    data = content.find_all('dl')
    print(data)


if __name__ == '__main__':
    get_data()