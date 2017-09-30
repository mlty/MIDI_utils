f = open('data_train.txt', 'r')
fw = open('data_train2.txt', 'w')
count = 0
for i in f:
    strr = ''
    line = i.replace('\n','').split(' ')
    strr = i.replace('\n', '')+'|'
    for j in range(len(line)):
        if line[j] != '0':
            strr += '1'
        else:
            strr += 'n'

        if j != len(line)-1:
            strr += ' '

    fw.write(strr)
    fw.write('\n')





