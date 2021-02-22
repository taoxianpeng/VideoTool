import requests
import pyperclip
from bs4 import BeautifulSoup as bs
from functools import wraps

def get_html(url):
    with requests.get(url) as req:
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
    urls = {}
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

if __name__ == '__main__':
    # get_html('https://v.qq.com/x/cover/mzc00200lmp89ps.html')
    #令人心动的offer
    tencent_video_zongyi('https://v.qq.com/x/cover/mzc00200lmp89ps.html')
    #tencent_video_zongyi('https://v.qq.com/x/cover/mzc0020049ijejf/b0035j0tgo0.html?')
    # tencent_tv('https://v.qq.com/x/cover/mzc00200x9fxrc9.html')