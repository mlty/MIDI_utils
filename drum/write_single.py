from rap import norm_txt

f = norm_txt.get_data('', '', 'The Foundation-Xzibit.txt')

print(f)
length = len(f)
i = 0
note=[]

while(i<length):
    print(f[i])

    i += 1


'''
    if len(s1) >= len(s2):
        for j in range(len(s1)):
            if s1[j] in s2:
                t = []
                t.append(s1[j])
                t.append(2)
                tt.append(t)
            else:
                t = []
                t.append(s1[j])
                t.append(1)
                tt.append(t)
    else:
        for j in range(len(s2)):
            if s2[j] in s1:
                t = []
                t.append(s2[j])
                t.append(2)
                tt.append(t)
            else:
                t = []
                t.append(s2[j])
                t.append(1)
                tt.append(t)
    note.append(tt)

    i += 2
'''