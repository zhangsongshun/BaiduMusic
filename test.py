import re
import urllib.request
import urllib
from urllib.request import urlretrieve

import eyed3
import requests
import json


def get_html(url):
    """爬取网页"""
    header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', }
    req = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    response.close()
    return content


# url = 'http://ting.baidu.com/data/music/links?songIds=7279415'
# result = get_html(url)
# print(json.loads(result)['data']['songList'][0])

xx = eyed3.load(u'music\\996730_半点.mp3')
print(xx)
# print(u'时长为：{}秒'.format(xx.info.time_secs))