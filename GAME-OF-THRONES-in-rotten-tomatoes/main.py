# coding = utf-8
"""
@author: zhou
@time:2019/6/5 14:18
"""


import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Line
import pyecharts.options as opts
from wordcloud import WordCloud
import jieba


baseurl = 'https://www.rottentomatoes.com'


def get_total_season_content():
    url = 'https://www.rottentomatoes.com/tv/game_of_thrones'
    response = requests.get(url).text
    content = BeautifulSoup(response, "html.parser")
    season_list = []
    div_list = content.find_all('div', attrs={'class': 'bottom_divider media seasonItem '})
    for i in div_list:
        suburl = i.find('a')['href']
        season = i.find('a').text
        rotten = i.find('span', attrs={'class': 'meter-value'}).text
        consensus = i.find('div', attrs={'class': 'consensus'}).text.strip()
        season_list.append([season, suburl, rotten, consensus])
    return season_list


def get_season_content(url):
    # url = 'https://www.rottentomatoes.com/tv/game_of_thrones/s08#audience_reviews'
    response = requests.get(url).text
    content = BeautifulSoup(response, "html.parser")
    episode_list = []
    div_list = content.find_all('div', attrs={'class': 'bottom_divider'})
    for i in div_list:
        suburl = i.find('a')['href']
        fresh = i.find('span', attrs={'class': 'tMeterScore'}).text.strip()
        episode_list.append([suburl, fresh])
    return episode_list[:5]


mylist = [['/tv/game_of_thrones/s08/e01', '92%'],
          ['/tv/game_of_thrones/s08/e02', '88%'],
          ['/tv/game_of_thrones/s08/e03', '74%'],
          ['/tv/game_of_thrones/s08/e04', '58%'],
          ['/tv/game_of_thrones/s08/e05', '48%'],
          ['/tv/game_of_thrones/s08/e06', '49%']]


def get_episode_detail(episode):
    # episode = mylist
    e_list = []
    for i in episode:
        url = baseurl + i[0]
        # print(url)
        response = requests.get(url).text
        content = BeautifulSoup(response, "html.parser")
        critic_consensus = content.find('p', attrs={'class': 'critic_consensus superPageFontColor'}).text.strip().replace(' ', '').replace('\n', '')
        review_list_left = content.find_all('div', attrs={'class': 'quote_bubble top_critic pull-left cl '})
        review_list_right = content.find_all('div', attrs={'class': 'quote_bubble top_critic pull-right  '})
        review_list = []
        for i_left in review_list_left:
            left_review = i_left.find('div', attrs={'class': 'media-body'}).find('p').text.strip()
            review_list.append(left_review)
        for i_right in review_list_right:
            right_review = i_right.find('div', attrs={'class': 'media-body'}).find('p').text.strip()
            review_list.append(right_review)
        e_list.append([critic_consensus, review_list])
    print(e_list)


def line_season(data) -> Line:
    season_list = data.sort()
    c = (
        Line()
        .add_xaxis([i[0][-8:] for i in season_list])
        .add_yaxis("Rate of Fresh", [i[2][:2] for i in season_list], is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-fresh"))
    )
    return c


def ciyun(data):
    STOPWORDS = ['episode', 'the', 'it', 'is', 'of', 'and', 'but',
                 'for', 'this', 'But', 'that', 'there', 'There', 'Were', 'in', 'was']
    datastr = ''.join([i[1][0] for i in data])
    fenci = ' '.join(jieba.cut(datastr, cut_all=False))
    wc = WordCloud(width=1800, height=1500, background_color='white', stopwords=STOPWORDS)
    wc.generate(fenci)
    wc.to_file('fenci.png')


def line_season_04(data) -> Line:
    c = (
        Line()
        .add_xaxis([i[0][-3:] for i in data])
        .add_yaxis("Rate of Fresh", [i[1][:-1] for i in data], is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="season04-fresh"))
    )
    return c


if __name__ == '__main__':
    total_season_content = get_total_season_content()
    # get_season_content('hehe')
    # get_episode_detail()
    line = line_season(total_season_content)
    line.render()


