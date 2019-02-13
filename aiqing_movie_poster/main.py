# coding = utf-8
"""
@author: zhou
@time:2019/2/13 9:20
"""

import requests
import json


def deal_pic(url, name):
    pic = requests.get(url)
    with open(name + '.jpg', 'wb') as f:
        f.write(pic.content)


def get_poster():
    for i in range(0, 10000, 20):
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电影&start=%s&genres=爱情' % i
        req = requests.get(url).text
        req_dict = json.loads(req)
        for j in req_dict['data']:
            name = j['title']
            poster_url = j['cover']
            print(name, poster_url)
            deal_pic(poster_url, name)


if __name__ == "__main__":
    get_poster()
