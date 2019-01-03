# coding = utf-8
"""
@author: zhou
@time:2019/1/3 18:58
"""

import jieba
import pandas as pd
from wordcloud import WordCloud
import numpy as np
from PIL import Image

font = r'C:\Windows\Fonts\FZSTK.TTF'
STOPWORDS = set(map(str.strip, open('stopwords.txt').readlines()))


def wordcloud_praise():
    df = pd.read_csv('praise.csv', usecols=[1])
    df_list = df.values.tolist()
    comment_after = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment_after)
    img = Image.open('haiwang8.jpg')
    img_array = np.array(img)
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font, mask=img_array, stopwords=STOPWORDS)
    wc.generate(words)
    wc.to_file('praise.png')


def wordcloud_ordinary():
    df = pd.read_csv('ordinary.csv', usecols=[1])
    df_list = df.values.tolist()
    comment_after = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment_after)
    img = Image.open('haiwang8.jpg')
    img_array = np.array(img)
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font, mask=img_array, stopwords=STOPWORDS)
    wc.generate(words)
    wc.to_file('ordinary.png')


def wordcloud_lowest():
    df = pd.read_csv('lowest.csv', usecols=[1])
    df_list = df.values.tolist()
    comment_after = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment_after)
    img = Image.open('haiwang7.jpg')
    img_array = np.array(img)
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font, mask=img_array, stopwords=STOPWORDS)
    wc.generate(words)
    wc.to_file('lowest.png')


if __name__ == "__main__":
    print("Save praise wordcloud")
    wordcloud_praise()
    print("Save ordinary wordcloud")
    wordcloud_ordinary()
    print("Save lowest wordcloud")
    wordcloud_lowest()
    print("THE END!!!")

