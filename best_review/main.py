# coding = utf-8
"""
@author: zhou
@time:2019/2/23 14:37
"""

import requests
from bs4 import BeautifulSoup


def get_detial(start):
    print('start get details')
    start = start
    base = 'https://movie.douban.com/review/best/?start='
    details = []
    for i in start:
        url = base + i
        response = requests.get(url).text
        content = BeautifulSoup(response, "html.parser")
        tmpid = content.find_all('div', attrs={'class': 'main review-item'})
        for k in tmpid:
            div_id = content.find('div', attrs={'id': k['id']})
            name = div_id.find('a', attrs={'class': 'name'}).text
            youyong = div_id.find('span', attrs={'id': 'r-useful_count-' + k['id']}).text.split('\n')[1].strip(' ')
            wuyong = div_id.find('span', attrs={'id': 'r-useless_count-' + k['id']}).text.split('\n')[1].strip(' ')
            reply = div_id.find('a', attrs={'class': 'reply'}).text.replace('回应', '')
            user = div_id.find('header', attrs={'class': 'main-hd'}).find('a', attrs={'class': 'avator'})['href']
            details.append([name, k['id'], youyong, wuyong, reply, user])
    print('finish get details')
    return details


def get_review(details):
    print('start get review')
    for i in details:
        res = requests.get('https://movie.douban.com/review/' + i[1]).text
        content = BeautifulSoup(res, "html.parser")
        review = content.find('div', attrs={'id': 'link-report'}).text.strip('\n').replace(',', '，').replace('\n', ' ')
        res2 = requests.get(i[5]).text
        content2 = BeautifulSoup(res2, "html.parser")
        try:
            user_local = content2.find('div', attrs={'class': 'user-info'}).find('a').text.replace(',', '，')
            i.append(user_local)
            i.append(review)
        except:
            user_local = "未知"
            i.append(user_local)
            i.append(review)
            continue
    print('finish get review')
    return details


def save_csv(review):
    print('start save to csv')
    with open('best_review.csv', 'w', encoding='utf-8') as f:
        f.write('name,id,youyong,wuyong,reply,user,local,review\n')
        for i in review:
            try:
                rowcsv = '{},{},{},{},{},{},{},{}'.format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                f.write(rowcsv)
                f.write('\n')
            except:
                continue
    print('finish save to csv')


def run():
    print('START')
    details = get_detial(['0', '20', '40'])
    review = get_review(details)
    save_csv(review)
    print('FINISH')


if __name__ == "__main__":
    run()
