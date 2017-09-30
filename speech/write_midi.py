from mido import Message, MidiFile, MidiTrack, MetaMessage
import re
import math
import os
#start = '75-0.25 0-0.25 75-0.625 0-0.375 75-0.25 0-0.25 76-0.875 0-0.125 73-0.75 0-0.25 75-0.75 0-0.25 80-0.75 0-0.25 80-0.75 0-0.25 75-1.0 80-0.375 79-0.25'

#end = ''
def write_midi(root, dist, filename):

    f = open(root+filename, 'r')
    ss = ''
    for line in f:
        strr = line.replace('\n', '').strip().split(' ')

        note = strr[0].split('-')
        s = ''
        for j in range(len(note)):
            s += str(note[j])
            if j != len(note) - 1:
                s += '-'

        s += '-' + str(float(strr[2]) - float(strr[1]))

        ss += s + ' '

    #print(ss)
    start = ss.strip()

    s = start
    s = s.strip()
    l = s.split(' ')
    length = len(l)
    i = 0
    note = []

    while (i < length):
        key = l[i].strip().split('-')
        time = float(key[len(key)-1]) / 0.125
        t = []
        for j in range(len(key)-1):
            tt = []
            tt.append(key[j])
            tt.append(int(time))
            t.append(tt)
        note.append(t)
        i += 1

    # 再写音乐
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24,
                             notated_32nd_notes_per_beat=8, time=0))
    track.append(MetaMessage('set_tempo', tempo=666666, time=0))

    time = int(120 / 8) * 4
    deltime = 0

    for i in range(len(note)):
        if len(note[i]) > 1 or (len(note[i]) == 1 and note[i][0][0] != '0'):

            # on
            for j in range(len(note[i])):
                if j == 0:
                    track.append(Message('note_on', note=int(note[i][j][0]), velocity=100, time=deltime))
                else:
                    track.append(Message('note_on', note=int(note[i][j][0]), velocity=100, time=0))

            # off
            for j in range(len(note[i])):
                if j == 0:
                    track.append(Message('note_off', note=int(note[i][j][0]), velocity=100,
                                         time=time * int(note[i][j][1])))
                else:
                    track.append(Message('note_off', note=int(note[i][j][0]), velocity=100, time=0))

            deltime = 0

        else:
            deltime += time

    mid.save(dist+filename+'.mid')

'''
ss = '0-0.5 64-0.5 72-0.5 74-0.5 76-1.0 76-0.5 72-0.5 71-1.0 79-0.5 67-0.5 67-0.5 72-1.5 '+\
    '0-0.5 69-0.5 72-0.5 74-0.5 76-1.0 74-0.5 76-0.5 79-1.0 76-0.5 79-0.5 79-0.5 81-1.5 '+\
    '0-0.5 84-0.5 81-0.5 72-0.5 76-1.0 76-0.5 79-0.5 79-1.0 76-0.5 74-0.5 76-0.5 77-1.5 '+\
    '0-0.5 76-1.0 74-0.5 76-1.0 76-1.0 74-0.5 79-0.5 83-0.5 81-0.5 79-2.0 '+\
    '0-0.5 64-0.5 72-0.5 74-0.5 76-1.0 76-0.5 72-0.5 71-1.0 79-0.5 67-0.5 67-0.5 72-1.5 '+\
    '0-0.5 69-0.5 72-0.5 74-0.5 76-1.0 74-0.5 76-0.5 79-1.0 76-0.5 79-0.5 79-0.5 81-1.5 '+\
    '0-0.5 84-0.5 81-0.5 72-0.5 76-1.0 76-0.5 79-0.5 79-1.0 76-0.5 74-0.5 76-0.5 77-1.5 '+\
    '0-0.5 76-1.0 74-0.5 76-1.0 76-1.0 74-0.5 79-0.5 83-0.5 81-0.5 79-2.0'



    '0-0.5 69-0.5 72-0.5 74-0.5 74-1.0 72-0.5 74-0.5 72-1.0 69-0.5 72-0.5 74-0.5 72-1.5 '+\
    '0-0.5 81-0.5 81-0.5 86-0.5 84-1.0 81-0.5 76-0.5 74-1.0 76-0.5 77-0.5 76-0.5 77-1.5 ' +\
    '0-0.5 76-0.5 74-0.5 72-0.5 76-1.0 86-0.5 81-0.5 79-1.0 76-0.5 74-0.5 76-0.5 77-1.5 '+\
    '76-0.5 74-1.0 76-0.5 79-1.0 81-1.0 81-0.5 79-0.5 79-0.5 81-0.5 79-2.0'
'''

ss = '0-0.5 64-0.5 65-0.5 72-0.5 71-0.5 72-0.5 71-1.0 69-1.0 69-0.5 67-0.5 64-0.5 64-0.5 64-1.0 '+\
    '64-0.5 64-0.5 67-2.0 69-0.5 64-0.5 64-0.5 59-0.5 60-2.0 0-1.0 '+\
    '0-0.5 60-0.5 67-0.5 69-0.5 67-0.5 69-0.5 67-1.0 65-1.0 64-0.5 62-0.5 60-0.5 62-0.5 64-1.0 '+\
    '60-0.5 62-0.5 62-2.0 64-0.5 62-0.5 62-0.5 62-0.5 60-2.0 0-1.0 '+\
    '0-0.5 64-0.5 65-0.5 72-0.5 71-0.5 72-0.5 71-1.0 69-1.0 69-0.5 67-0.5 64-0.5 64-0.5 64-1.0 '+\
    '64-0.5 64-0.5 67-2.0 69-0.5 64-0.5 64-0.5 59-0.5 60-2.0 0-1.0 '+\
    '0-0.5 60-0.5 67-0.5 69-0.5 67-0.5 69-0.5 67-1.0 65-1.0 64-0.5 62-0.5 60-0.5 62-0.5 64-1.0 '+\
    '60-0.5 62-0.5 62-2.0 64-0.5 62-0.5 62-0.5 62-0.5 60-2.0 0-1.0'

start = ss.strip()

s = start
s = s.strip()
l = s.split(' ')
length = len(l)
i = 0
note = []

while (i < length):
    key = l[i].strip().split('-')
    time = float(key[len(key)-1]) / 0.125
    t = []
    for j in range(len(key)-1):
        tt = []
        tt.append(key[j])
        tt.append(int(time))
        t.append(tt)
    note.append(t)
    i += 1

# 再写音乐
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24,
                         notated_32nd_notes_per_beat=8, time=0))
track.append(MetaMessage('set_tempo', tempo=666666, time=0))

time = int(120 / 8) * 4
deltime = 0

for i in range(len(note)):
    if len(note[i]) > 1 or (len(note[i]) == 1 and note[i][0][0] != '0'):

        # on
        for j in range(len(note[i])):
            if j == 0:
                track.append(Message('note_on', note=int(note[i][j][0]), velocity=100, time=deltime))
            else:
                track.append(Message('note_on', note=int(note[i][j][0]), velocity=100, time=0))

        # off
        for j in range(len(note[i])):
            if j == 0:
                track.append(Message('note_off', note=int(note[i][j][0]), velocity=100,
                                     time=time * int(note[i][j][1])))
            else:
                track.append(Message('note_off', note=int(note[i][j][0]), velocity=100, time=0))

        deltime = 0

    else:
        deltime += time*int(note[i][j][1])

mid.save('2.mid')


'''
root = 'C:\\Users\\v-honzhu\\Desktop\\t4\\'
dist = 'C:\\Users\\v-honzhu\\Desktop\\t6\\'
c = 0
for p, d, filenames in os.walk(root):
    for filename in filenames:
        try:
            write_midi(root, dist, filename)
            c += 1
            print(c)
        except:
            print(filename)
            '''

'''

'''