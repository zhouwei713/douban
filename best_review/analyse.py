# coding = utf-8
"""
@author: zhou
@time:2019/2/23 16:50
"""

from pyecharts import Line, Map
import pandas as pd
import jieba
from wordcloud import WordCloud
from collections import Counter

font = r'C:\Windows\Fonts\FZSTK.TTF'
STOPWORDS = set(map(str.strip, open('stopwords.txt', encoding='utf-8').readlines()))
data = pd.read_csv('best_review.csv')


# 折线图
def zhexian(data):
    line = Line("duibi", width=1000, height=400)
    line.add("youyong", data['name'], data['youyong'], xaxis_rotate=45)
    line.add("wuyong", data['name'], data['wuyong'], xaxis_rotate=45)
    line.add("reply", data['name'], data['reply'], xaxis_rotate=45)
    line.render()


# 词云 total
def total_ciyun(data):
    df_list = data['review'].tolist()
    fenci = ' '.join(jieba.cut(str(df_list), cut_all=False))
    wc = WordCloud(width=1800, height=1500, background_color='white', font_path=font, stopwords=STOPWORDS)
    wc.generate(fenci)
    wc.to_file('fenci.png')


# 词云 江户川的哀
def ciyun(data):
    j_list = data.iloc[14]['review']
    j_fenci = ' '.join(jieba.cut(j_list, cut_all=False))
    j_wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font, stopwords=STOPWORDS)
    j_wc.generate(j_fenci)
    j_wc.to_file('j_fenci.png')


# 地图
def ditu(data):
    mylist = ['黑龙江', '云南', '陕西', '浙江', '江苏', '北京', '上海', '重庆']
    data_local = data['local'].tolist()
    count = dict(Counter(data_local))
    value = []
    attr = []
    for k, v in count.items():
        for i in mylist:
            if i in k:
                k = i
                value.append(v*10)
                attr.append(k)
    map = Map("大神区域分布", width=1200, height=600)
    map.add(
        "",
        attr,
        value,
        maptype="china",
        is_visualmap=True,
        visual_text_color="#000",
    )
    map.render()


if __name__ == "__main__":
    data = pd.read_csv('best_review.csv')
    ditu(data)
    # zhexian(data)




