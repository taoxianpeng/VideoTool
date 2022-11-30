import html.parse as parse
from bs4 import BeautifulSoup as bs
import re
'''
将传入的url自动分析是那个网站的什么类型视频，
然后调用对应的解析函数进行抓取栏目
'''

class Controller():
    def __init__(self,url):
        self.url = url
    
    def getInfo(self,):
        return self.__parse_url()

    def __parse_url(self,):
        '''
        判断url前缀属于那个视频网站，
        然后转跳到对应的函数进行解析
        '''
        tencent_host = 'https://v.qq.com'
        iqiyi_host = 'https://www.iqiyi.com'
        youku_host = 'https://v.youku.com'
        mgtv_host= 'https://www.mgtv.com'

        if tencent_host in self.url:
            return self.__tencent_video()
        elif iqiyi_host in self.url:
            return self.__iqiyi_video()
        elif youku_host in self.url:
            return self.__youku_video()
        elif mgtv_host in self.url:
            return self.__mgtv_video()
        else:
            return 
    def __tencent_video(self,):
        '''
        腾讯视频综艺和电视剧之类有区别
        '''
        html = parse.get_html(self.url)
        a = re.search(r'"category_map":(.+),"stars_name"',html).group()

        if '综艺' in a:
            return parse.tencent_video_zongyi(self.url)
        if '动漫' in a:
            return parse.tencent_tv(self.url)
        if '电视剧' in a:
            return parse.tencent_tv(self.url)

    def __iqiyi_video(self,):
        # categoryName
        html = parse.get_html(self.url)
        a = re.search(r'"categoryName":"(.+)","categoryMainTitle"',html).group(1)
        if '综艺' in a:
            return parse.iqiyi_zongyi(self.url)
        if '电视剧' in a:
            return parse.iqiyi_tv(self.url)
        if '动漫' in a:
            return parse.iqiyi_tv(self.url)

    def __youku_video(self,):
        html = parse.get_html(self.url)
        a = re.search(r'catName:(.+),\s+seconds',html).group(1)
        if '综艺' in a:
            return parse.youku_zongyi(self.url)
        if '电视剧' in a:
            return parse.youku_tv(self.url)
        if '动漫' in a:
            return parse.youku_tv(self.url)
    def __mgtv_video(self,):
        #解析综艺
        return parse.mgtv_zongyi(self.url)
if __name__ == '__main__':
    url = r'https://v.qq.com/x/cover/mzc00200pl9jhvr.html'
    controller = Controller(url)
    print(controller.getInfo())