# encoding=utf-8
# 处理数据：连音 划分成 24 拍
import os

fw = open('guitar_train_data.txt', 'w')
count = 0

def get_batch(root, filename):

    f = open(root+filename, 'r')
    global count
    record = {}
    c = 0
    import re

    for line in f:
        line = line.replace('\n', '').strip().split(' ')

        if c == 0:
            t = []
            note = []
            t.append(line[1].strip())
            t.append(line[2].strip())
            note.append(line[0])
            record[str(t)] = note

        else:

            t = []
            note = []
            t.append(line[1].strip())
            t.append(line[2].strip())
            note.append(line[0])

            if str(t) in record:
                record[str(t)].append(line[0])
            else:
                record[str(t)] = note

        c += 1

    records = []
    for i in record:
        line = i
        g = re.findall('\'(.+?)\'', line)
        #print(float(g[0]), float(g[1]))

        t = []
        t.append(float(g[0]))
        t.append(float(g[1]))
        t.append(float(g[1])-float(g[0]))
        record[i].sort()
        t.append(record[i])

        records.append(t)

    import operator

    records.sort(key=lambda l:(l[0],l[1]),reverse=False)

    start = 0.0
    for i in range(len(records)):
        t = records[i][0] - start
        records[i].append(t)
        start = records[i][1]


    #for i in range(len(records)):
        #print(records[i])

    count_time = 0

    strr = ''
    for i in range(len(records)):

        if records[i][4] >= 0.0:
            if records[i][4] != 0.0:
                strr += '0-'+str(records[i][4])+' '
                count_time += records[i][4]
            note = records[i][3]
            t = ''
            for j in range(len(note)):
                t += str(note[j])
                if j != len(note)-1:
                    t += '-'

            strr += t + '-' + str(records[i][2]) + ' '
            count_time += records[i][2]

            if count_time >= 24:
                #print(strr)
                l = len(strr.split(' '))
                if l > 48:
                    fw.write(strr)
                    fw.write('\n')
                #print(l, count_time)
                strr = ''
                count_time = 0

    l = len(strr.split(' '))
    #print(l,  count_time)
    if l > 48:
        fw.write(strr)
        fw.write('\n')
        #print(strr)

    print(count)
    count += 1



root = 'C:\\Users\\v-honzhu\\Desktop\\test\\'
#dist = 'C:\\Users\\v-honzhu\\Desktop\\test\\'

for p, d, filenames in os.walk(root):
    for filename in filenames:
        get_batch(root, filename)


















'''

    if c == 0:
        s = line[1]
        e = line[2]
        note.append(line[0])

    else:
        if line[1] == s and line[2] == e:
            note.append(line[0])

        if line[1] != s or line[2] != e:

            t = []
            t.append(note)
            t.append(s)
            t.append(e)

            records.append(t)

            note = []
            s = line[1]
            e = line[2]
            note.append(line[0])



    c += 1

for i in range(len(records)):
    print(records[i])
'''












