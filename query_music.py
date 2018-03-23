import re
import urllib.request
import urllib
from urllib.request import urlretrieve
import requests
import json

from bs4 import BeautifulSoup


def get_html(url):
    """爬取网页"""
    header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', }
    req = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    response.close()
    return content


def get_music(name):
    for i in range(1):
        url = 'http://musicmini.baidu.com/app/search/searchList.php?qword=' + name
        result = get_html(url)
        soup = BeautifulSoup(result, 'html.parser')
        soup_songs = soup.findAll('td', attrs={'class': 'sName linkTitle linkMV linkCT'})
        soup_singer = soup.findAll('td', attrs={'class': 'uName linkArtist'})
        soup_albums = soup.findAll('td', attrs={'class': 'aName'})
        soup_id = soup.findAll('i', attrs={'class': 'checkboxI'})
        songs = []
        singers = []
        albums = []
        song_ids = []
        music_list = []
        for singer in soup_songs:
            if singer.div.em is None:
                songs.append(singer.div.string)
            else:
                songs.append(singer.div.em.string)
        for singer in soup_singer:
            singers.append(singer.string)
        for album in soup_albums:
            albums.append(album.string)
        for song_id in soup_id:
            song_ids.append(song_id.input.get('id'))
        for num in range(len(songs)):
            dic = {'song': songs[num], 'singer': singers[num], 'album': albums[num], 'song_id': song_ids[num+1]}
            music_list.append(dic)
        return music_list


def run_enter():
    return get_music(urllib.parse.quote(input('输入查询歌曲名：')))


if __name__ == '__main__':
    a = run_enter()
    for music in a:
        print(music['song'], music['singer'], music['album'], music['song_id'],)