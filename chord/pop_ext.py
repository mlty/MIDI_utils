import os
import re

##
#pop 音乐数据处理：先是归一化开始时间为0
#然后处理重音以及音符排序 最后处理重复率过高(伴奏)
#
#Return '[ note ]  start_time    end_time'
##

def pop_ext(root, dist, filename):

    f = open(root + filename, 'r')
    c = 0
    diff = 0
    for line in f:
        if c == 0:
            line = line.strip().split(' ')
            diff = float(line[1])
        else:
            break
        c += 1

    global count
    record = {}
    c = 0
    import re

    f = open(root + filename, 'r')

    for line in f:
        if '-' in line:
            continue
        line = line.replace('\n', '').strip().split(' ')

        if c == 0:
            t = []
            note = []
            t.append(str(float(line[1].strip())-diff))
            t.append(str(float(line[2].strip())-diff))
            note.append(line[0])
            record[str(t)] = note

        else:

            t = []
            note = []
            t.append(str(float(line[1].strip())-diff))
            t.append(str(float(line[2].strip())-diff))
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
        # print(float(g[0]), float(g[1]))

        t = []
        t.append(float(g[0]))
        t.append(float(g[1]))
        t.append(float(g[1]) - float(g[0]))
        record[i].sort()
        t.append(record[i])

        records.append(t)

    import operator

    records.sort(key=lambda l: (l[0], l[1]), reverse=False)

    start = 0.0

    notes = []
    for i in range(len(records)):
        notes.append(records[i][3][0])

    num_list = get_repeat_num_seq(notes)


    if int(num_list) < 10:
        fw = open(dist+filename, 'w')
        for i in range(len(records)):
            strr = ''
            strr += str(records[i][3]) + ' ' + str(records[i][0]) + ' ' + str(records[i][1])
            fw.write(strr)
            fw.write('\n')

def slice(num_str, w):
    '''
    对输入的字符串滑窗切片返回结果列表
    '''
    result_list = []
    for i in range(len(num_str) - w + 1):
        result_list.append(num_str[i:i + w])
    return result_list

def get_repeat_num_seq(num_str):
    '''
    统计重复模式串数量
    '''
    result_dict = {}
    result_list = []
    for i in range(5, int(len(num_str)/2)):
        one_list = slice(num_str, i)
        result_list += one_list
    for i in range(len(result_list)):
        if str(result_list[i]) in result_dict:
            result_dict[str(result_list[i])] += 1
        else:
            result_dict[str(result_list[i])] = 1
    sorted_result_dict = sorted(result_dict.items(), key=lambda e: e[1], reverse=True)
    return sorted_result_dict[0:10][0][1]


# 进行二次抽取
# 对整首音乐进行切片
#
#
#
#
#
def detection_duplicate(root, dist, filename):
    f = open(root+filename, 'r')
    count = 0
    notes = []
    for line in f:
        g = re.findall('\'(.+?)\'', line)
        t = ''
        for i in range(len(g)):
            t += g[i]
            if i != len(g)-1:
                t += '-'

        notes.append(t)
        count += 1
    sample = notes[:5]

    f = open(root + filename, 'r')
    s = 0
    c = 0
    cc = 0
    strr = ''
    last_time = 0
    for line in f:
        ss = line
        strr += line
        line = line.replace('\n', '').strip().split(' ')

        last_time += float(line[len(line)-1]) - float(line[len(line)-2])

        diff = float(line[len(line)-2]) - s

        if diff > 8:

            if sample == notes[c:c+5] or last_time > 16:

                if len(strr.split('\n')) > 64 or last_time > 16:
                    fw = open(dist + filename + str(cc) + '.txt', 'w')
                    fw.write(strr)
                    cc += 1
                    last_time = 0

            strr = ss

        c += 1
        s = float(line[len(line)-1])

    if len(strr.split('\n')) > 64 or last_time > 16:
        fw = open(dist + filename + str(cc) + '.txt', 'w')
        fw.write(strr)


#detection_duplicate('', '', '9.mid_1.txt')

# 2.5
def ext2_5(root, dist, filename):

    f = open(root + filename, 'r')

    n = 0
    pre = ''
    count = 0
    st = ''

    for line in f:
        st += line
        strr = ''
        g = re.findall('\'(.+?)\'', line)
        line = line.replace('\n', '').strip().split(' ')
        t = ''
        for i in range(len(g)):
            t += g[i]
            if i != len(g) - 1:
                t += '-'

        diff = float(line[len(line) - 1]) - float(line[len(line) - 2])

        t += '-' +str(diff)
        #print(t)

        if t != pre:
            pre = t
            if count >= 4:
                #print(filename)
                n += 1
            count = 1
        else:
            count += 1
    if n <= 2:
        fw = open(dist + filename, 'w')
        fw.write(st)
        pass
    else:
        print(filename,    n)











# 进行第三次处理
def ext3(root, dist, filename):

    f = open(root + filename, 'r')
    c = 0
    diff = 0
    for line in f:
        if c == 0:
            line = line.strip().split(' ')
            diff = float(line[len(line)-2])
        else:
            break
        c += 1

    f = open(root + filename, 'r')
    fw = open(dist + filename, 'w')

    count = 0
    notes = []
    for line in f:
        strr = ''
        g = re.findall('\'(.+?)\'', line)
        line = line.replace('\n', '').strip().split(' ')
        t = ''
        for i in range(len(g)):
            t += g[i]
            if i != len(g) - 1:
                t += '-'

        s = float(line[len(line)-2]) - diff
        e = float(line[len(line)-1]) - diff
        d = e - s

        strr = t + ' ' + str(s) + ' ' + str(e) + ' ' + str(d)
        fw.write(strr)
        fw.write('\n')


def extbybar(root, dist, filename):

    fw = open(dist+filename, 'w')
    f = open(root+filename, 'r')
    time = 16
    ss = ''

    for line in f:
        strr = ''
        g = re.findall('\'(.+?)\'', line)
        line = line.replace('\n', '').strip().split(' ')

        s = float(line[len(line)-2])
        diff = float(line[len(line)-1]) - float(line[len(line)-2])


        if s >= time:
            fw.write(ss)
            fw.write('\n')
            ss = ''
            time += 16

        ss += line[0] + '-' + str(diff) + ' '

    fw.write(ss)
    fw.write('\n')


# 2.5 限制音乐片段长度在100以上
def ext_100(root, dist, filename):
    strr = ''
    f = open(root+filename, 'r')
    count = 0
    for line in f:
        strr += line
        count += 1

    if count > 100:
        fw = open(dist+filename, 'w')
        fw.write(strr)





root = 'C:\\Users\\v-honzhu\\Desktop\\get_3\\'
dist = 'C:\\Users\\v-honzhu\\Desktop\\get_4\\'
c = 0
for p, d, filenames in os.walk(root):
    for filename in filenames:
        try:
            ext3(root, dist, filename)
            c += 1
            print(c)
        except:
            print(filename)