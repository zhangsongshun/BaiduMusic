import re
import urllib.request
import urllib
from urllib.request import urlretrieve
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


def get_music():
    """解析网页，获取歌单列表"""
    page = 0
    music_list = []
    for i in range(2):
        url = 'http://music.baidu.com/tag/%E7%B2%A4%E8%AF%AD?start=' + str(page) + '&size=20&third_type=0'
        page += 20
        result = get_html(url)
        music_items = re.findall(r'data-info=.*?>(.*?)</a>', result, re.S)
        singer_items = re.findall(r'<span class="author_list" title="(.*?)">', result, re.S)
        songID_items = re.findall(r'<a href="/song/(.*?)" target=_blank', result, re.S)
        for i in range(len(music_items)):
            dic = {'music_name': music_items[i], 'singer': singer_items[i], 'songID': songID_items[i]}
            music_list.append(dic)
    for i in range(len(music_list)):
        print(str(i+1), '.', music_list[i])
    return music_list


def download(music_list):
    """下载爬取歌单里的歌曲"""
    # 获取下载地址有多种方法
    # 1.post  range中下载歌曲数不要超过爬取歌单总数。可设置range(len(music_list))
    for i in range(20):
        url = 'http://play.baidu.com/data/music/songlink'
        data = {'songIds': music_list[i]['songID']}
        r = requests.post(url, data=data)
        result = r.content.decode('UTF-8')
        # print(json.loads(result)['data']['songList'][0]['songName'])
        # print(json.loads(result)['data']['songList'][0]['songLink'])
        # print(json.loads(result)['data']['songList'][0]['lrcLink'])

        print('《'+json.loads(result)['data']['songList'][0]['songName']+'》' + ' 正在下载...')
        urlretrieve(json.loads(result)['data']['songList'][0]['songLink'],
                    'music\\' + music_list[i]['songID'] + '_' + music_list[i]['music_name'] + '.mp3')
        print('下载完成！')
        # 下载歌词
        print('《'+json.loads(result)['data']['songList'][0]['songName']+'》' + ' 正在下载歌词...')
        urlretrieve(json.loads(result)['data']['songList'][0]['lrcLink'],
                    'lyric\\' + music_list[i]['songID'] + '_' + music_list[i]['music_name'] + '.txt')
        print('歌词下载完成！')
    # 2.get  range中下载歌曲数不要超过爬取歌单总数。可设置range(len(music_list))
    # for i in range(1):
    #     url = 'http://ting.baidu.com/data/music/links?songIds=' + music_list[i]['songID']
    #     result = get_html(url)
    #     print(json.loads(result)['data']['songList'][0]['songName'])
    #     print(json.loads(result)['data']['songList'][0]['songLink'])
    #     urlretrieve(json.loads(result)['data']['songList'][0]['songLink'],
    #                 'music\\' + music_list[i]['music_name'] + '.mp3')

    # 打开歌词
    # f = open('lyric\\922583_单恋高校.txt', 'r', encoding="utf-8")
    # with open('lyric\\922583_单恋高校.txt', 'r', encoding="utf-8") as f:
    #     print(f.read())


if __name__ == '__main__':
    music_list = get_music()
    download(music_list)
