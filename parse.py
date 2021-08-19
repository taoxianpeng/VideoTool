import requests
import pyperclip
from bs4 import BeautifulSoup as bs
from functools import wraps
import logging
import re
from collections import OrderedDict
import time
import json

from requests.api import post

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
    cid = re.split(r'/|\.',url)[7]
    host='https://v.qq.com'
    urls={}
    #获取lists的json数据
    #获取数据的url是通用的
    post_url = 'https://pbaccess.video.qq.com/trpc.universal_backend_service.page_server_rpc.PageServer/GetPageData?video_appid=3000010&vplatform=2'
    headers = {
        'referer':'https://v.qq.com/',
        'cookie':'tvfe_boss_uuid=421d9ae056149d9b; pgv_pvid=9157042206; vversion_name=8.2.95; video_omgid=; video_guid=75c15f79deb327d0; video_platform=2; pgv_info=ssid=s837149268',
        'content-type':'application/json'
    }

    request_payload = '{"page_params":{"req_from":"web","page_type":"detail_operation","page_id":"vsite_episode_list","id_type":"1","cid":"'+cid+'","page_num":"","page_size":"100","page_context":""},"has_cache":1}'
    try:
        return_json = requests.post(url=post_url,data=request_payload,headers=headers)
        items_json = return_json.json()["data"]["module_list_datas"][0]["module_datas"][0]["item_data_lists"]["item_datas"]   
 
        urls = OrderedDict()
        for item in items_json:
            item = item["item_params"]
            title = item["union_title"]
            # https://v.qq.com/x/cover/mzc00200lxzhhqz/[vid].html
            play_url = host+'/x/cover/'+cid+'/'+item['vid']+'.html'
            urls[title] = play_url
        
        return urls
    except Exception as e:
        print(e)
    

    return urls

#@parse
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
def youku_tv(url):
    #anthology-content
    html = get_html(url)
    soup = bs(html,'lxml')
    a = soup.find('div',class_='anthology-content')
    b = a.find_all('a')
    
    items=OrderedDict()
    for item in b:
        play_url = item['href']
        title  = item['title']
        items[title] = play_url

    return items
def youku_zongyi(url):
    html = get_html(url)
    soup = bs(html,'lxml')
    a = soup.find('div',class_='anthology-content')
    b = a.find_all('div',class_='pic-text-item')
    
    items = OrderedDict()
    for item in b:
        title = item['title']
        play_url = item.find('a')['href']
        items[title] = play_url
    
    return items
def mgtv_zongyi(url):
    vid = url.split('/')[-1].split('.')[0]
    videolist_json_url = 'https://pcweb.api.mgtv.com/list/master?vid='+vid
    videolist_json_str = get_html(videolist_json_url)
    videolist_json = json.loads(videolist_json_str)

    videolists = videolist_json['data']['list']

    items = OrderedDict()
    for item in videolists:
        title = item['t1']
        clip_id = item['clip_id']
        video_id=item['video_id']
        play_url = 'https://www.mgtv.com/b/'+clip_id+'/'+video_id+'.html'
        items[title] = play_url
    return items
    
if __name__ == '__main__':
    url = 'https://v.qq.com/x/cover/mzc00200lxzhhqz.html'
    # print(iqiyi_tv(url))
    print(tencent_tv(url))
    # mgtv_zongyi(url)