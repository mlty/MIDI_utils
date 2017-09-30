from mido import Message, MidiFile, MidiTrack, MetaMessage
import re
import os
from collections import Counter



def get_rap(root, dist, filename):
    mid = MidiFile()
    track_w = MidiTrack()
    mid.tracks.append(track_w)

    track_w.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24,
                             notated_32nd_notes_per_beat=8, time=0))
    track_w.append(MetaMessage('set_tempo', tempo=1000000, time=0))

    mid_read = MidiFile(root+filename)

    isF = False


    for j, track in enumerate(mid_read.tracks):
        for i in range(len(track)):
            if track[i].type == 'note_on' or track[i].type == 'note_off':
                if track[i].channel == 9:
                    isF = True
                    track_w.append(track[i])

    if isF:
        mid.save('r2.mid')


normal_time = [0.000, 0.125, 0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000]

#fw = open('ff.txt', 'w')
#f = open('test.txt', 'w')
f = open('record.txt', 'w', errors='ignore', encoding='utf-8')

def normal_beats(t):
    i = int(t)
    temp = round(t - i, 4)

    if temp in normal_time:
        return t
    else:
        for j in range(len(normal_time)):
            if temp < normal_time[j]:
                if (normal_time[j] - temp) < (temp - normal_time[j-1]):
                    return normal_time[j] + i
                else:
                    return normal_time[j-1] + i
    #return i+1+0.000


def extract_track(root, dist, filename):

    mid = MidiFile(root + filename)
    all_time = 0
    global_end = 0

    # print(mid.ticks_per_beat)

    #f = open(dist+filename+'.txt', 'w')

    def ticks2beats(t):
        return t / mid.ticks_per_beat

    tempo = 652174
    for msg in mid:
        if msg.type == 'set_tempo':
            tempo = msg.tempo

    # print(tempo)

    def ticks2time(t):
        return t * (tempo * 1e-6 / mid.ticks_per_beat)

    noteList = {}
    # print("note  beat_start  beat_end  time_start  time_end")

    tag = 0

    note_arr = []
    time_arr = []
    line = []

    for j, track in enumerate(mid.tracks):
        for i in range(len(track)):
            if 'note_off' in str(track[i]):
                tag = 1
                break

    if tag == 0:
        for j, track in enumerate(mid.tracks):
            #f.write('------------------------------\n')
            note_arr = []
            time_arr = []
            for i in range(len(track)):
                if 'meta' not in str(track[i]):
                    # 抽出时间
                    relink = 'time=(.*)'
                    cinfo = re.findall(relink, str(track[i]))
                    time = int(cinfo[0])
                    if 'note' in str(track[i]) and track[i].channel != 9:
                        # note
                        relink = 'note=(.+?) velocity'
                        cinfo = re.findall(relink, str(track[i]))
                        # note = table[int(cinfo[0])]
                        note = str(int(cinfo[0]))

                        # velocity
                        relink = 'velocity=(.+?) time'
                        cinfo = re.findall(relink, str(track[i]))
                        velocity = int(cinfo[0])

                        if velocity != 0:
                            noteList[note] = all_time + time
                        if velocity == 0:
                            if note in noteList:
                                start = noteList[note]
                                end = all_time + time
                                noteList.pop(note)

                                diff = normal_beats(ticks2beats(start)) - global_end
                                if diff < 0:
                                    diff = 0.0000
                                    # 进行时间归一化处理
                                    # f.write("%-4s     %.3f     %.3f     %.2f     %.2f\n" % (note, normal_beats(ticks2beats(start)),
                                    # normal_beats(ticks2beats(end)), ticks2time(start), ticks2time(end)))

                                if int(note) >= 60:
                                    pass
                                    #f.write("%-4s     %.4f     %.4f     %.4f\n" % (note, normal_beats(ticks2beats(start)),
                                                                               #normal_beats(ticks2beats(end)), diff))
                                global_end = normal_beats(ticks2beats(end))
                                note_arr.append(note)
                                t = []
                                t.append(note)
                                t.append(normal_beats(ticks2beats(start)))
                                t.append(normal_beats(ticks2beats(end)))
                                time_arr.append(t)

                    all_time += time

            line.append(time_arr)


    if tag == 1:
        for j, track in enumerate(mid.tracks):
            #f.write('------------------------------\n')
            note_arr = []
            time_arr = []
            for i in range(len(track)):
                if 'meta' not in str(track[i]):
                    # 抽出时间
                    relink = 'time=(.*)'
                    cinfo = re.findall(relink, str(track[i]))
                    time = int(cinfo[0])
                    if 'note' in str(track[i]) and track[i].channel != 9:
                        # note
                        relink = 'note=(.+?) velocity'
                        cinfo = re.findall(relink, str(track[i]))
                        # note = table[int(cinfo[0])]
                        note = str(int(cinfo[0]))

                        # velocity
                        relink = 'velocity=(.+?) time'
                        cinfo = re.findall(relink, str(track[i]))
                        velocity = int(cinfo[0])

                        if 'note_off' not in str(track[i]):
                            noteList[note] = all_time + time
                        if 'note_off' in str(track[i]):
                            if note in noteList:
                                start = noteList[note]
                                end = all_time + time
                                noteList.pop(note)
                                # 进行时间归一化处理
                                # f.write("%-4s     %.3f     %.3f     %.2f     %.2f\n" % (
                                # note, normal_beats(ticks2beats(start)), normal_beats(ticks2beats(end)), ticks2time(start), ticks2time(end)))
                                # note_arr.append(note)

                                diff = normal_beats(ticks2beats(start)) - global_end
                                if diff < 0:
                                    diff = 0.0000

                                if int(note) >= 60:
                                    pass
                                    #f.write("%-4s     %.4f     %.4f     %.4f\n" % (note, normal_beats(ticks2beats(start)),
                                                                               #normal_beats(ticks2beats(end)), diff))
                                global_end = normal_beats(ticks2beats(end))
                                note_arr.append(note)
                                t = []
                                t.append(note)
                                t.append(normal_beats(ticks2beats(start)))
                                t.append(normal_beats(ticks2beats(end)))
                                time_arr.append(t)

                    all_time += time

            line.append(time_arr)



    for i in range(len(line)):
        #print(i,    '---------------------------------')
        s = 0
        e = 0
        F = True
        c = 0
        words = 0
        w = []
        cf = 0

        for j in range(len(line[i])):
            if int(line[i][j][0]) < 42:
                F = False
            if float(line[i][j][1]) < float(s):
                c += 1
                #F = False
                #break

            if line[i][j][1] == s or line[i][j][2] == e:
                cf += 1


            if line[i][j][1]!= s or line[i][j][2] != e:
                s = line[i][j][1]
                e = line[i][j][2]

            words += (float(line[i][j][2])-float(line[i][j][1]))
            w.append(float(line[i][j][2])-float(line[i][j][1]))

        if c >= 5:
            F = False

        if F and len(line[i]) != 0:
            #print('ok')
            key = words / len(line[i])
            w.sort()
            print(i, c, cf, key, w[int(len(line[i])/2)])

            if key > 0.3 and key < 1.5 and cf < 100 and len(line[i]) > 100 and w[int(len(line[i])/2)] >= 0.25:

                fw = open(dist + filename + '_' +str(i) +'.txt', 'w', errors='ignore', encoding='utf-8')
                #print(i)

                for k in range(len(line[i])):
                    fw.write(str(line[i][k][0])+' '+str(line[i][k][1])+' '+str(line[i][k][2]))
                    fw.write('\n')

                if i == 0 or i == 1:
                    break
        else:
            f.write(filename)
            f.write('\n')


def get_files(root, dist, filename):

    f = open(root+filename)

    for line in f:
        if '-' not in line:
            pass





#extract_track('','','C:\\Users\\v-honzhu\\Desktop\\data_3\\王菲_棋子.mid')

#extract_track('', 'c_', '2.mid')


if __name__ == '__main__':
    #get_rap('', '', 'f1.mid')
    #extract_track('', 'C:\\Users\\v-honzhu\\Desktop\\t1\\', '27453.mid')
    #get_files('', '', '115.mid')

    root = 'C:\\Users\\v-honzhu\\Desktop\\Music\\c_data\\'

    dist = 'C:\\Users\\v-honzhu\\Desktop\\data_get_2\\'

    id = []
    #f = open('record.txt', 'w')
    c = 0
    for p, d, filenames in os.walk(root):
        for filename in filenames:
            try:
                extract_track(root, dist, filename)
                c += 1
                print(c)
            except:
                print(filename)

