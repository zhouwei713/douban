# coding = utf-8
"""
@author: zhou
@time:2019/8/27 16:13
@File: main.py
"""

import requests
from bs4 import BeautifulSoup


def get_data():
    data = []
    for i in range(0, 150, 25):
        url = 'https://movie.douban.com/celebrity/1054531/movies?start=%s&format=text&sortby=time&role=A1' % i
        res = requests.get(url).text
        content = BeautifulSoup(res, "html.parser")
        tbody_tag = content.find_all('tbody')
        tr_tag = tbody_tag[1].find_all('tr')
        for tr in tr_tag:
            tmp = []
            name = tr.find('a').text
            year = tr.find('td', attrs={'headers': 'mc_date'}).text
            rate = tr.find('td', attrs={'headers': 'mc_rating'}).text
            tmp.append(name)
            tmp.append(year)
            tmp.append(rate.replace('\n', '').strip().replace('-', ''))
            data.append(tmp)
    return data


if __name__ == '__main__':
    data = get_data()
    print(data)
    with open('jack_data.csv', 'w', encoding='utf-8') as f:
        f.write('name,year,rate\n')
        for d in data:
            try:
                rowcsv = '{},{},{}'.format(d[0], d[1], d[2])
                f.write(rowcsv)
                f.write('\n')
            except:
                continue
