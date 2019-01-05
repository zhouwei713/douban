# coding = utf-8
"""
@author: zhou
@time:2019/1/4 17:41
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymongo

# 处理webp格式到jpg格式
# url = 'https://img3.doubanio.com/view/photo/photo/public/p611791976.webp'
# url1 = url.split('webp')
# url2 = url1[0] + 'jpg'
# print(url2)
# content = requests.get(url2)
# print(content.content)
# f = open('wangzuxian.jpg', 'wb')
# f.write(content.content)
# f.close()


def get_posters():
    comment_url_list = []
    picture_list = []
    for i in range(0, 40000, 30):
        url = 'https://movie.douban.com/celebrity/1166896/photos/?type=C&start=%s&sortby=like&size=a&subtype=a' % str(i)
        req = requests.get(url).text
        content = BeautifulSoup(req, "html.parser")
        chekc_point = content.find('span', attrs={'class': 'next'}).find('a')
        if chekc_point != None:
            data = content.find_all('div', attrs={'class': 'cover'})
            for k in data:
                ulist = k.find('a')['href']
                plist = k.find('img')['src']
                comment_url_list.append(ulist)
                picture_list.append(plist)
        else:
            break
    return comment_url_list, picture_list


def get_comment(comment_l):
    client = pymongo.MongoClient('mongodb://douban:douban1989@ds149744.mlab.com:49744/douban')
    db = client.douban
    mongo_collection = db.comment
    comment_list = []
    comment = []
    print("Save to MongoDB")
    for i in comment_l:
        response = requests.get(i).text
        content = BeautifulSoup(response, "html.parser")
        tmp_list = content.find_all('div', attrs={'class': 'comment-item'})
        comment_list = comment_list + tmp_list
        for k in comment_list:
            tmp_comment = k.find('p').text
            mongo_collection.insert_one({'comment': tmp_comment})
            comment.append(tmp_comment)
    print("Save Finish!")


def download_picture(pic_l):
    for i in pic_l:
        pic = requests.get(i)
        p_name = i.split('/')[7]
        with open('picture\\' + p_name, 'wb') as f:
            f.write(pic.content)


if __name__ == "__main__":
    print("Get URL list")
    comment_url_list, picture_list = get_posters()
    # list = ['https://movie.douban.com/celebrity/1166896/photo/2232707438/',
    #         'https://movie.douban.com/celebrity/1166896/photo/1524663203/']
    p_list = ['https://img1.doubanio.com/view/photo/l/public/p2232707438.jpg',
              'https://img3.doubanio.com/view/photo/l/public/p2232705511.jpg']
    print("Get Comment")
    get_comment(comment_url_list)
    print("Download picture")
    download_picture(p_list)
    print("END ALL!")
