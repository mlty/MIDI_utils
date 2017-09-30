#encoding=utf-8
import os

# 数据规整化
def norm_txt(root, dist, filename):
    f = open(root+filename, 'r')

    fw = open(dist+filename, 'w')

    c = 0

    for i in f:
        line = i.replace('\n','')
        l = line.split('     ')
        if c == 0:
            diff = float(l[1])
        c += 1
        fw.write(str(l[0])+'  '+str(float(l[1])-diff)+'  '+str(float(l[2])-diff))
        fw.write('\n')


# 数据格式化成想要的样子
normal_t = [0.000, 0.125, 0.250, 0.375, 0.500, 0.625, 0.750, 0.875]

def normal_time(t):
    i = int(t)
    temp = round(t - i, 3)

    if temp in normal_t:
        return t
    else:
        for j in range(len(normal_t)):
            if temp < normal_t[j]:
                #if (normal_t[j] - temp) < (temp - normal_t[j-1]):
                    #return normal_t[j] + i
                #else:
                return normal_t[j-1] + i
    return i+1+0.00

def get_data(root, dist, filename):
    f = open(root+filename)
    for i in f:
        line = i.replace('\n', '').split('  ')
        end = line[2]

    length = round(float(end)/0.125)+1

    threshold = 0.125
    records = [[] for i in range(length)]

    f = open(root + filename)

    for i in f:
        line = i.replace('\n','').split('  ')
        note = line[0]
        start = normal_time(float(line[1]))
        end = normal_time(float(line[2]))

        #print(start, '   ', end)

        s = round(start/threshold)
        e = round(end/threshold)

        if s == e:
            records[s].append(note)
        else:
            for i in range(s,e):
                records[i].append(note)

    return records

# 取到不重复的数据
def ext_data(filename):

    f = open()

if __name__ == '__main__':

    f = open('data.txt', 'w')
    root = 'C:\\Users\\v-honzhu\\Desktop\\rap_norm_text\\'

    for p, d, filenames in os.walk(root):
        for filename in filenames:
            try:

                g = get_data(root, '', filename)

                c = 0
                line = ''
                for i in range(len(g)):
                    g[i].sort(reverse=True)
                    str = ''
                    if len(g[i]) == 0:
                        str = '0'
                    else:
                        for j in range(len(g[i])):
                            str += g[i][j]
                            if j != len(g[i]) - 1:
                                str += '-'
                    c += 1
                    if c == 128:
                        line += str
                        f.write(line)
                        f.write('\n')
                        line = ''
                        c = 0
                    else:
                        line += str
                        line += ' '
                #f.write('\n')

                #norm_txt(root, dist, filename)
            except:
                print(filename)

        #print(g[i])
'''
    root = 'C:\\Users\\v-honzhu\\Desktop\\t\\'
    dist = 'C:\\Users\\v-honzhu\\Desktop\\n\\'

    #norm_txt(root, dist, '2OfAmerikasMostWanted.txt')

    for p, d, filenames in os.walk(root):
        for filename in filenames:
            try:
                norm_txt(root, dist, filename)
            except:
                print(filename)

    r = get_data('','','f1.mid.txt')
    print(r)
'''