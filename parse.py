import requests
import pyperclip
from bs4 import BeautifulSoup as bs
from functools import wraps
import logging
import re
from collections import OrderedDict
import time
import json

logging.basicConfig(level=logging.INFO)

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    with requests.get(url, headers=headers) as req:
        # print(req.headers['content-type'])
        req.encoding = 'utf-8'
        return req.text

def parse(get_video_urls_func):
    @wraps(get_video_urls_func)
    def decorated(*args, **kwargs):
        urls_dict = get_video_urls_func(*args, **kwargs) #urls is dict
        print('该栏目所有节目选项：')
        urls_list = []
        for i,name in enumerate(urls_dict):
            print("{}. {}".format(i,name))
            urls_list.append(urls_dict[name])
        while True:
            n = int(input('输入对应的数值 按下回车(输入小于0的数-退出):'))

            if n<0: break

            try:
                url_ = urls_list[n]
                pyperclip.copy(url_)
                print('已经复制到粘贴板上！')
            except Exception as f:
                print('error: ',f)
        
    return decorated


# @parse
def tencent_tv(url):
    host='https://v.qq.com'
    urls={}
    html=get_html(url)
    soup=bs(html,'lxml')
    episode=soup.find('div',class_='mod_episode')
    a_items = episode.find_all('a')
    for a_item in a_items:
        url_=host+a_item['href']
        #去除字符串的空格和换行符
        title =a_item.string.replace('\n','').replace(' ','')
        # print(title)
        if url_ != '':
            urls[title]=url_
        else:
            print('[error]: ',title," url为空！")
    return urls

# @parse
def tencent_video_zongyi(url):
    host = 'https://v.qq.com'
    urls = OrderedDict()
    html = get_html(url)
    soup = bs(html, 'lxml')

    list_items = soup.find('ul', class_='figure_list')
    a_items = list_items.find_all('a',class_='figure')

    for a_item in a_items:
        url_ = host + a_item['href']
        title = a_item['title']
        if url_ != '':
            urls[title]=url_
        else:
            print('[error]: ',title," url为空！")
    return urls

def iqiyi_zongyi(url):
    
    html = get_html(url)
    soup = bs(html,'lxml')
    a = soup.find('div',id='rightPlayList')
    b = a.find_all('li',class_='play-list-item')
    
    
    items = OrderedDict()
    for item in b:
        idn = item['data-td']
        title = item.find('a')['title']
        items[idn]=title
    
    play_url_host = 'https://pcw-api.iqiyi.com/video/video/baseinfo/'

    urls = OrderedDict()
    for idn in items:
        title = items[idn]
        text = get_html(play_url_host+idn)
        play_url = re.search(r'"playUrl":"(.+)","issueTime":', text).group(1)
        urls[title] = play_url
    
    return urls

def iqiyi_tv(url):
    html = get_html(url)
    aid_num = re.search(r'"albumId":(.+),"albumName"',html).group(1)
    
    play_url='https://pcw-api.iqiyi.com/albums/album/avlistinfo?aid={}&page=1&size=1000'.format(aid_num)

    json_ = json.loads(get_html(play_url))

    items = OrderedDict()
    for a in json_['data']['epsodelist']:
        items[a['name']] = a['playUrl']
    
    return items

if __name__ == '__main__':
    url = 'https://www.iqiyi.com/v_19vub7y9ztk.html'
    # print(iqiyi_tv(url))
    print(iqiyi_tv(url))