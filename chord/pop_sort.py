#pop数据二次处理
import os
import re

'''
root = 'C:\\Users\\v-honzhu\\Desktop\\dd\\'
dist = 'C:\\Users\\v-honzhu\\Desktop\\d5\\'
wdist = 'C:\\Users\\v-honzhu\\Desktop\\d7\\'

def pop_sort(wdist, dist, filename):

    f = open(dist+filename, 'r')

    fw = open(wdist + filename, 'w')

    time = 16
    ss = ''
    end = 0

    for line in f:
        strr = ''
        line = line.replace('\n', '').strip().split(' ')

        s = float(line[len(line) - 2])
        diff = float(line[len(line) - 1]) - float(line[len(line) - 2])

        if float(line[1]) > end:
            ss += '0-' + str(float(line[1])-end)+' '


        if s >= time:
            fw.write(ss)
            fw.write('\n')
            ss = ''
            time += 16

        ss += line[0] + '-' + str(diff) + ' '
        end = float(line[2])

    fw.write(ss)
    fw.write('\n')





'''

'''
root = 'C:\\Users\\v-honzhu\\Desktop\\data\\'
cc = 0
def count_beat(root, filename):
    global cc
    f = open(root+filename, 'r')
    c = 0
    all = 0
    for line in f:
        line = line.replace('\n', '').strip().split(' ')
        all += len(line)

        avg = 0
        keys = []

        for i in range(len(line)):
            n = int((line[i].split('-'))[0])
            keys.append(n)
            avg += n

            if n < 60:
                c += 1

    if c*2 >= all:
        cc += 1
        print(filename)


for p, d, filenames in os.walk(root):
    for filename in filenames:
        try:
            count_beat(root, filename)
        except:
            #print(filename)
            pass

print(cc)
'''


'''
fw = open('pop_data.txt', 'w')
def datapro(root, filename):

    f = open(root+filename, 'r')
    count = 0
    for line in f:

        line = line.replace('\n', '').strip().split(' ')

        strr = ''

        for i in range(len(line))[::-1]:

            if i == len(line)-1 and str((line[i].split('-'))[0]) == '0':
                strr = ''
            else:
                strr += line[i] + ' '

        strr = strr.strip()

        stl = strr.split(' ')
        chord = str(stl[0])
        if count == 0:
            pre = ''

        str_line = pre+' '+chord+'|'+strr

        fw.write(str_line.strip())
        fw.write('\n')

        pre = strr

        count += 1


#datapro('', 'C:\\Users\\v-honzhu\\Desktop\\data\\王菲-雪中莲.mid_8.txt0.txt')
'''

# pop music 数据处理 从一首歌中抽出2个小节信息 [节奏, 和弦, 旋律]

fw = open('rm_data.txt', 'w')

def popext(root, filename):

    f = open(root+filename, 'r')
    dealine = 8
    notes = ''
    rhythm = ''
    chord = ''
    end = 0
    pre = ''

    for line in f:

        ll = line.replace('\n', '').strip().split(' ')
        start = float(ll[1])


        if start < dealine:

            if start > end:
                if start-end > 2:
                    rhythm += '0-' + str(float(2)) + ' '
                else:
                    rhythm += '0-' + str(start-end) + ' '

            notes += ll[0] + ' '
            if float(ll[2]) - float(ll[1]) > 2:
                rhythm += str(float(2)) + ' '
            else:
                rhythm += str(float(ll[2]) - float(ll[1])) + ' '
        else:

            n = notes.strip().split(' ')[::-1]
            #print(n[0])
            nn = ''
            for i in range(len(n)):
                nn += n[i] + ' '

            strr = rhythm + '|' + str(pre) + ' ' + str(n[0]) + '|' + str(n[0]) + '|' + nn.strip()
            pre = nn.strip()

            fw.write(strr)
            fw.write('\n')

            #print(strr)

            dealine += 8

            notes = ll[0] + ' '
            rhythm = str(float(ll[2]) - float(ll[1])) + ' '

        end = float(ll[2])



#popext('C:\\Users\\v-honzhu\\Desktop\\C_music _data\\c6\\', '9.mid_1.txt0.txt')



root = 'C:\\Users\\v-honzhu\\Desktop\\t4\\'

for p, d, filenames in os.walk(root):
    for filename in filenames:
        try:
            popext(root, filename)
        except:
            print(filename)