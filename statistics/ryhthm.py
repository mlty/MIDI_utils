# 从每个小节中抽取节奏型
import os

c6 = ['60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71']
c7 = ['72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83']

count_6 = 0
count_7 = 0

def statistics(root, dist, filename):

    f = open(root + filename)
    n6 = 0
    n7 = 0
    c = 0

    global count_6
    global count_7

    for line in f:
        ll = line.replace('\n', '').strip().split(' ')

        if str(ll[0]) in c6:
            n6 += 1
        if str(ll[0]) in c7:
            n7 += 1

        c += 1

    if n6 > c/2 or n7 > c/2:
        if n6 > n7:
            count_6 += 1
            f = open(root + filename, 'r')
            fw = open(dist + filename, 'w')

            for line in f:
                fw.write(line)

        else:
            count_7 += 1

            f = open(root + filename, 'r')
            fw = open(dist + filename, 'w')

            for line in f:
                ll = line.replace('\n', '').strip().split(' ')
                note = ll[0].strip().split('-')
                n = ''
                for j in range(len(note)):
                    n += str(int(note[j]) - 12)
                    if j != len(note)-1:
                        n += '-'
                strr = n + ' ' + ll[1] + ' ' + ll[2]
                fw.write(strr)
                fw.write('\n')


def convert(root, filename):

    f = open(root+filename)
    strr = ''
    for line in f:
        ll = line.replace('\n', '').strip().split(' ')
        diff = float(ll[2]) - float(ll[1])

        strr += ll[0] + '-' + str(diff) + ' '


    print(strr)






root = 'C:\\Users\\v-honzhu\Desktop\\C_music _data\\c6\\'
convert(root, '4955.mid_1.txt1.txt')



root = 'C:\\Users\\v-honzhu\Desktop\\C_music _data\\t4\\'
dist = 'C:\\Users\\v-honzhu\\Desktop\\C_music _data\\c6\\'
for p, d, filenames in os.walk(root):
    for filename in filenames:
        try:
            statistics(root, dist, filename)
        except:
            print(filename)

print(count_6)
print(count_7)