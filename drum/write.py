# 修改版本

from mido import Message, MidiFile, MidiTrack, MetaMessage
import re
import rap.norm_txt as rap
r = rap.get_data('','','f1.mid.txt')
print(r)

s = ''
for i in range(len(r)):
    t = ''
    for j in range(len(r[i])):
        t += str(r[i][j])
        if j != len(r[i])-1:
            t += '-'

    if len(r[i]) == 0:
        t = '0'

    s += t
    if i != len(r)-1:
        s += ' '
print(s)

# 版本2 beat转化
'''
s = '42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 0 36 36 0 0 42-39-37 42-37 0 0 0 0 36 36 ' \
    '42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 0 36 36 0 0 42-39-37 42-37 0 0 0 0 36 36 ' \
    '42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 0 36 36 0 0 42-39-37 42-37 0 0 0 0 36 36 ' \
    '42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 36 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 36 36 42-36 42-36 0 0 0 0 0 0 42-39-37 42-37 0 0 0 0 0 0 42 42 36 0 36 36 0 0 42-39-37 42-37 0 0 0 0 36 36'
'''

l = s.split(' ')
length = len(l)

if length % 2 != 0:
    s += ' 0'
    l = s.split(' ')
    length = len(l)
    print(length)
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
track.append(MetaMessage('set_tempo', tempo=500000, time=0))

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

mid.save('d1.mid')






































