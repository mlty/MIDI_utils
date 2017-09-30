#encoding=utf-8
import urllib.request
import re
import wget

url = 'https://freemidi.org/genre-hip-hop-rap'

def download(durl):
    url = 'https://freemidi.org/'+durl

    request = urllib.request.Request(url)

    # 爬取结果
    response = urllib.request.urlopen(request)

    data = response.read()

    # 设置解码方式
    data = data.decode('utf-8', 'ignore')

    relink = 'href="(.+?)" download>Download MIDI</a>'
    cinfo = re.findall(relink, data)

    for j in range(len(cinfo)):
        wget.download('https://freemidi.org/'+cinfo[j])



if __name__ == '__main__':

    request = urllib.request.Request(url)

    # 爬取结果
    response = urllib.request.urlopen(request)

    data = response.read()

    # 设置解码方式
    data = data.decode('utf-8')

    relink = '<div class="genre-link-text"><a href="(.+?)">.*</a></div>'
    cinfo = re.findall(relink, data)

    for j in range(len(cinfo)):
        suburl = 'https://freemidi.org/'+cinfo[j]

        request = urllib.request.Request(suburl)

        # 爬取结果
        response = urllib.request.urlopen(request)

        data = response.read()

        # 设置解码方式
        data = data.decode('utf-8', 'ignore')

        relink = '<span itemprop="name"> <a href="(.+?)" itemprop="url">'
        subinfo = re.findall(relink, data)

        for i in range(len(subinfo)):
            download(subinfo[i])


