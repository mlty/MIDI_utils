#encoding=utf-8
#处理抽取出来的乐谱，删除太短和单一的部分，进行分段
import os
import shutil

def ext(root, dist, filename):
    f = open(root + filename, 'r')

    c = 0
    b = False
    strr = ''
    n = 0

    for line in f:
        if '-' not in line and b == False:
            fw = open(dist+str(c)+filename, 'w')
            b = True
            strr = ''
            n = 1

        if b:
            if '-' not in line:
                strr += line

            else:

                b = False
                ll = len(strr.split('\n'))

                if ll > 64:
                    fw.write(strr)
                    c += 1

    if n != 0:
        ll = len(strr.split('\n'))
        if ll > 64:
            fw.write(strr)
        fw.write(strr)

'''
root = 'C:\\Users\\v-honzhu\\Desktop\\t1\\'
dist = 'C:\\Users\\v-honzhu\\Desktop\\test2\\'

for p, d, filenames in os.walk(root):
    for filename in filenames:
        ext(root, dist, filename)
        
'''

# 处理数据 抽取合适的乐谱
def norm_data(root, dist, filename):
    f = open(root+filename, 'r')
    c = 0
    s = 0
    strr = ''
    g = 0
    for line in f:
        l = line.split('     ')
        if g == 0:
            s = float(l[1].strip())
            g += 1

        if abs(float(l[1].strip())-s) <= 10:
            s = float(l[1].strip())
            strr += line
        else:
            fw = open(dist + str(c)+ filename, 'w')
            fw.write(strr)
            strr = ''
            s = float(l[1].strip())
            c += 1

    fw = open(dist + str(c) + filename, 'w')
    fw.write(strr)

def ext_by_length(root, dist, filename):

    f = open(root+filename, 'r')
    c = 0
    for i in f:
        c += 1

    if c > 50:
        shutil.copy(root+filename, dist+filename)

def pro_diff(root, dist, filename):
    f = open(root + filename, 'r')
    fw = open(dist + filename, 'w')

    c = 0
    for line in f:
        if c == 0:
            l = float((line.split('     '))[1].strip())
        else:
            break
        c += 1

    f = open(root + filename, 'r')
    for line in f:
        strr = ''
        line = line.split('     ')
        x1 = float(line[1].strip()) - l
        x2 = float(line[2].strip()) - l

        if x1 < 0:
            x1 = 0.0
        if x2 < 0:
            print('err')


        strr += line[0].strip()+' '+str(x1)+' '+str(x2)
        fw.write(strr)
        fw.write('\n')












#root = 'C:\\Users\\v-honzhu\\Desktop\\guitar_txt\\'
root = 'C:\\Users\\v-honzhu\\Desktop\\test2\\'
dist = 'C:\\Users\\v-honzhu\\Desktop\\t1\\'

for p, d, filenames in os.walk(root):
    for filename in filenames:
        pro_diff(root, dist, filename)








