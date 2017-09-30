import urllib.request
import re
import wget
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url = 'http://www.download-midi.com/files/genre/Rap/page/'
f = open('record2.txt', 'w', encoding='utf-8')

if __name__ == '__main__':
    total_num = 2
    for i in range(1, total_num+1):
        t_url = url+str(i)
        request = urllib.request.Request(t_url)

        # 爬取结果
        response = urllib.request.urlopen(request)

        data = response.read()

        # 设置解码方式
        data = data.decode('utf-8')

        relink = '<a href="(.+?)" target="_blank">download</a>'
        cinfo = re.findall(relink, data)

        for j in range(len(cinfo)):
            try:
                wget.download(cinfo[j])
            except:
                print(cinfo[j])

















