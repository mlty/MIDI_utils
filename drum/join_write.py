from mido import Message, MidiFile, MidiTrack, MetaMessage
import re
import math

rythm = '2 2 42 42 42 10 42 42 42 138 42 42 42 42 42 42 2 2 42 42 42 10 42 42 42 138 42 42 42 42 42 42'

notes = '46-43-40-36 46 46 46 69-60 69-60 43-40-36 41-35 41-35 41-35 46-41-39-36 46-41-39-36 57 57 57 41-35 46-41-39-36 46-41-39-36 57 57 69-41-36 46-39 61-46 69-43-36 69-61 62 62 69-43-36 69-43-36 60-46 69-43-36 69-43-36 61 46-39 46-39 46-39 46-43-36 46-43-36 69-61 69-61 69 43-36 69 46-43-39-36 69 69 46-43-36 46-43-36 46-43-36 69-61 69-61 69 54 36 36 69-43-36 69 69 69 69 46-43-36 46-43-36 69 69 69'

r = rythm.split(' ')
n = notes.split(' ')
s = ''
count = 0

for i in range(len(r)):
    strr = ''
    num = int(r[i])
    c = 7
    while(c>=0):
        a = int(num / math.pow(2, c))
        num -= a*math.pow(2, c)
        c -= 1

        if a == 1:
            if count > len(n)-1:
                count = 0
            strr += n[count]+' '
            count += 1
        else:
            strr += '0'+' '
    s += strr.strip()+' '


# 版本2 beat转化
'''
s = '42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 0 36 36 0 0 42-39-37 42-37 0 0 0 0 36 36 ' \
    '42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 0 36 36 0 0 42-39-37 42-37 0 0 0 0 36 36 ' \
    '42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 0 36 36 0 0 42-39-37 42-37 0 0 0 0 36 36 ' \
    '42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 0 36 36 0 0 42-39-37 42-37 0 0 0 0 36 36'
'''

s = s.strip()
print(s)
l = s.split(' ')
length = len(l)
i = 0
note=[]

while(i<length):
    if l[i] == '0':
        t = []
        tt = []
        t.append('0')
        t.append(1)
        tt.append(t)
        note.append(tt)
    else:
        ll = l[i].split('-')
        tt = []

        for j in range(len(ll)):
            t = []
            t.append(ll[j])
            t.append(1)

            tt.append(t)
        note.append(tt)

    i += 1


#再写音乐
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24,
                         notated_32nd_notes_per_beat=8, time=0))
track.append(MetaMessage('set_tempo', tempo=666666, time=0))

time = int(120 / 8)*4
deltime = 0

'''
[['42', 2], ['36', 2]]
[['0', 2]]
[['0', 2]]
[['0', 2]]
[['42', 2], ['39', 1], ['37', 2]]
[['0', 2]]
[['0', 2]]
[['0', 2]]
[['42', 2]]
[['36', 2]]
[['0', 2]]
[['0', 2]]
[['42', 2], ['39', 1], ['37', 2]]
'''

for i in range(len(note)):
    print(note[i])


for i in range(len(note)):
    if len(note[i])>1 or (len(note[i])==1 and note[i][0][0]!='0'):

        # on
        for j in range(len(note[i])):
            if j == 0:
                track.append(Message('note_on', channel=9, note=int(note[i][j][0]), velocity=100, time=deltime))
            else:
                track.append(Message('note_on', channel=9, note=int(note[i][j][0]), velocity=100, time=0))

        # off
        for j in range(len(note[i])):
            if j == 0:
                track.append(Message('note_off', channel=9, note=int(note[i][j][0]), velocity=100, time=time*int(note[i][j][1])))
            else:
                track.append(Message('note_off', channel=9, note=int(note[i][j][0]), velocity=100, time=0))

        deltime = 0

    else:
        deltime += time

mid.save('d2.mid')







































