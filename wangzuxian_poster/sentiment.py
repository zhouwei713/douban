# coding = utf-8
"""
@author: zhou
@time:2019/1/23 15:05
"""


from snownlp import SnowNLP
import pymongo
import jieba
import pandas as pd
from jieba import analyse
from wordcloud import WordCloud
from PIL import Image
import numpy as np
font = r'C:\Windows\Fonts\FZSTK.TTF'


# 情感分析
def mysentiment(content):
    s = SnowNLP(content)
    return s.sentiments


# 连接MongoDB
client = pymongo.MongoClient('mongodb://douban:douban1989@ds149744.mlab.com:49744/douban')
db = client.douban
mongo_collection = db.comment

# 获取前5万条数据
limit_comment = mongo_collection.find().limit(50000)


# 将数据做情感分析并保存到本地
def localsave():
    with open('new_comment.csv', 'w', encoding='utf-8') as f:
        f.write('comment,sentiment\n')
        for i in limit_comment:
            try:
                comment = i["comment"].strip().replace('\n', '').replace('\r', '')  # 处理掉评论中的空格和换行符
                comment_doc = comment.replace(',', '，')  # 把评论中的英文半角逗号改为中文半角逗号，来保证CSV文件是两列
                sentiment = mysentiment(comment_doc)
                rowcsv = '{},{}'.format(comment_doc, sentiment)
                f.write(rowcsv)
                f.write('\n')
            except:
                continue
    print("Local save finish!")


def g_dealdata():
    data = pd.read_csv('new_comment.csv', encoding='utf-8')
    # 正面评价
    first_sort = data.sort_values(['sentiment'], ascending=False)  # 获取高评价，没有负面评价
    first_sort_100 = first_sort[:100]  # 前100的高评价
    print(first_sort_100)
    first_sort_string = " ".join(first_sort_100.comment.tolist())
    first_cut = " ".join(jieba.cut(first_sort_string))
    keyword = analyse.extract_tags(first_cut, topK=500, withWeight=True, allowPOS=('a', 'e', 'n', 'o', 'v', 'y'))
    print(keyword[:10])
    g_s = pd.DataFrame(keyword, columns=['words', 'weight'])  # 用于后面其他处理
    dict_keywords = dict(keyword)
    img = Image.open('g1.jpg')
    img_array = np.array(img)
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font,
                   mask=img_array)
    wc.generate_from_frequencies(dict_keywords)
    wc.to_file('goodcomment.png')


if __name__ == "__main__":
    localsave()
    g_dealdata()

