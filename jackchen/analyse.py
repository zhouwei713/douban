# coding = utf-8
"""
@author: zhou
@time:2019/8/27 17:02
@File: analyse.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']


df = pd.read_csv('jack_data.csv')
df.isnull().sum()  # 查看缺失值情况

df_copy = df.copy()
df_copy.dropna(how='any', inplace=True)  # 去掉缺失值

# 去掉异常值
except_data = df_copy[df_copy['name'].apply(lambda x: x == '喜剧之王')].index
df_copy.drop(except_data, inplace=True)


def scatter_pic():
    # 通过散点图，查看随着年份的不同，电影评分的变化
    plt.scatter(df_copy['year'], df_copy['rate'])
    plt.title("成龙电影得分总概")
    plt.savefig('total.jpg')


def bar_pic_top():
    rate_top5 = df_copy.sort_values(by='rate', ascending=False)[0:5]
    plt.bar(rate_top5['name'], rate_top5['rate'], color=['steelblue', 'indianred'])
    for x, y in enumerate(rate_top5['year']):
        plt.text(x, 4, '%s' % y, ha='center', va='bottom')
    plt.title("成龙电影得分top5")
    plt.savefig('top5.jpg')


def bar_pic_bottom():
    rate_bottom5 = df_copy.sort_values(by='rate', ascending=False)[-6:-1]
    plt.bar(rate_bottom5['name'], rate_bottom5['rate'], color=['steelblue', 'indianred'])
    for x, y in enumerate(rate_bottom5['year']):
        plt.text(x, 4, '%s' % y, ha='center', va='bottom')
    plt.title("成龙电影得分bottom5")
    plt.savefig('bottom5.jpg')


def pie_pic():
    year_count = df_copy['year'].value_counts()
    plt.pie(year_count.values.tolist()[:10], labels=year_count.index.tolist()[:10],
            autopct="%1.1f%%")
    plt.title("成龙电影出产年份top10")
    plt.savefig('year10.jpg')


def year(myyear):
    year = df_copy[df_copy['year'] == myyear]
    plt.xticks(rotation=20)
    plt.bar(year['name'], year['rate'], color=['steelblue', 'indianred'])
    for x, y in enumerate(year['rate']):
        plt.text(x, y, '%s' % y, ha='center', va='bottom')
    plt.title("%s" % myyear)
    plt.savefig(str(myyear) + '.jpg')


if __name__ == '__main__':
    # year(1976)
    pie_pic()
    # bar_pic_top()
    # bar_pic_bottom()



