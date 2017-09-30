import subprocess
from time import sleep

f = open('w1.txt', 'r')
for line in f:
    l = line.strip().split(' ')
    name = l[1]+'.mid'
    url = l[0]
    cmd = 'wget -O %s %s -p %s'% (name, url, '/ddir')
    subprocess.call(cmd, shell=True)
    sleep(3)


wget -c "http://www.bing.com/dict/proxy/proxy?k=HoEjnHmAgU9YYBobJYNDnZzNHkLIQLOxQtS6S5qjGmA3AkSTbgKTudQcMBjmPSpl" -O t.mid -P ~/download/
