import urllib.request
import re
import wget
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://www.midishow.com/midi/browse/pop-music?page='
f = open('record3.txt', 'w', encoding='utf-8')

def download():
    print(1)

if __name__ == '__main__':
    total_num = 601
    for i in range(65, total_num):
        t_url = url+str(i+1)
        request = urllib.request.Request(t_url)

        # 爬取结果
        response = urllib.request.urlopen(request)

        data = response.read()

        # 设置解码方式
        data = data.decode('utf-8')

        relink = '<strong class(.+?)</strong>'
        cinfo = re.findall(relink, data)

        for j in range(len(cinfo)):
            strll = cinfo[j]
            reid = 'href="/midi/(.+?).html">'
            id = re.findall(reid, strll)
            rename = '<a .*>(.+?)</a>'
            name = re.findall(rename, strll)

            purl = 'http://www.midishow.com/midi/' + str(id[0]) + '.html'
            request = urllib.request.Request(purl)
            response = urllib.request.urlopen(request)
            data = response.read()
            data = data.decode('utf-8').replace('\n', '').replace('\t', '')
            relink = '<div id="file_info"><ul>(.+?)</ul>'

            try:
                t = re.findall(relink, data)
                relink = '<li>(.+?)</li>'
                t = re.findall(relink, str(t[0]))
                f.write(id[0]+' '+name[0]+' '+str(t[0])+' '+str(t[1])+' '+str(t[2])+' '+str(t[3])+' '+str(t[4]))
                f.write('\n')
            except:
                print('!')

        print(i+1)