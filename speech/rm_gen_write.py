notes = '0 60 62 62 62 64 62 62 60'
rhythm = '0.5 0.5 2.0 0.5 0.5 0.5 0.5 2.0 1.0'
n = notes.strip().split(' ')[::-1]
r = rhythm.strip().split(' ')

strr = ''
for i in range(len(n)):
    strr += str(n[i]) + '-' + str(r[i]) + ' '

print(strr)

