from mido import Message, MidiFile, MidiTrack, MetaMessage
import re
def read_file(filename):
    f = open(filename, 'r')

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

        for i in range(len(cinfo)):
            if i != len(cinfo)-1:
                str += cinfo[i]+' '
            else:
                str += cinfo[i]

        for i in range(len(cinfo1)):
            t = cinfo1[i].replace('[','').replace(']','').replace(' ','')
            if t != '':
                if i != len(cinfo1)-1:
                    str1 += t+ ' '
                else:
                    str1 += t

        l.append(str)
        l.append(str1)

        lines.append(l)

    return lines

def write_mid(s, g, filename):

    s_arr = []
    g_arr = []
    y = s.split(' ')
    y1 = g.split(' ')
    for i in range(len(y)):
        s_arr.append(y[i].replace(' ', ''))
    for j in range(len(y1)):
        g_arr.append(y1[j].replace(' ', ''))
    length = min(len(s_arr), len(g_arr))

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24,
                             notated_32nd_notes_per_beat=8, time=0))
    track.append(MetaMessage('set_tempo', tempo=1000000, time=0))

    for i in range(length):
        lint = int(int(s_arr[i]) * 120 * 4 / 8)
        track.append(Message('note_on', note=int(g_arr[i]), velocity=100, time=0))
        track.append(Message('note_on', note=int(g_arr[i]), velocity=0, time=lint))

    mid.save(filename+'.mid')

got = read_file('2OfAmerikasMostWanted.txt')
print(got[836][0])
print(got[836][1])
#g = '77 75 73 75 77 78 77 68 68 70 72 73 73 73 73 75 77 80 77 78 80 82 82 80 78 80 77 78 77 75 70 70 72 73 75 77 75 73 75 77 78 77 80 77 78 80 82 82 82 82 84 82 80 77 78 80 82 82 84 82 80 77 78 77 75 70 70 70 72 73 72 77 75 75 73'
#s = '4 4 6 4 4 4 4 8 4 4 4 4 2 2 4 4 4 8 4 4 4 8 4 4 4 8 4 4 4 8 4 4 4 4 8 4 4 4 4 4 4 4 8 4 4 4 4 4 2 4 4 4 8 4 4 4 8 4 4 4 8 4 4 4 4 4 4 4 4 4 8 8 4 4 12'
#write_mid(s, g, 'test1')


