#encoding=utf-8

def word2speech(filename, temp):

    f = open(filename, 'r', encoding='utf-8')
    fw = open('w.txt', 'w', encoding='utf-8')

    temp =int(temp)
    for line in f:
        line = line.strip().split('|')

        for i in range(len(line)):
            if len(list(line[i])) != 0:
                l = len(list(line[i]))
                c = list(line[i])
                t = format(float(60000) / (temp * 2 * l), '.2f')

                for j in range(len(c)):
                    fw.write(str(c[j]) + ' ' + str(t))
                    fw.write('\n')

word2speech('test.txt', 68)






