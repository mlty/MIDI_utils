import re
import os



def read_file(filename):
    f = open(filename)
    count = 0

    lines = []

    for i in f:

        l = []
        line = i.split(']')
        l1 = line[0]
        l2 = line[1]

        restr = '\'(.+?)\''
        cinfo = re.findall(restr, l1)
        cinfo1 = l2.split(',')

        str = ''
        str1 = ''
        c = 0
        c1 = 0

        for i in range(len(cinfo)):
            c += 1
            if i != len(cinfo)-1:
                str += cinfo[i]+' '
            else:
                str += cinfo[i]

        for i in range(len(cinfo1)):
            c1 += 1
            t = cinfo1[i].replace('[','').replace(']','').replace(' ','')
            if t != '':
                if i != len(cinfo1)-1:
                    str1 += t+ ' '
                else:
                    str1 += t

        l.append(str)
        l.append(str1)

        if c<1000:
            count += 1
            #print(str)

        lines.append(l)

    return count

w = read_file('fw.txt')
print(w)



