from mido import Message, MidiFile, MidiTrack, MetaMessage
import re
import os

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


normal_time = [0.0000, 0.0625, 0.1250, 0.1875, 0.2500, 0.3125, 0.3750,
               0.4375, 0.5000, 0.5625, 0.6250, 0.6875, 0.7500, 0.8125, 0.8750, 0.9375]

fw = open('ff.txt', 'w')
#f = open('test.txt', 'w')

def normal_beats(t):
    i = int(t)
    temp = round(t - i, 4)

    if temp in normal_time:
        return t
    else:
        for j in range(len(normal_time)):
            if temp < normal_time[j]:
                #if (normal_time[j] - temp) < (temp - normal_time[j-1]):
                return normal_time[j] + i
                #else:
                    #return normal_time[j-1] + i
    return i+1+0.000


def extract_track(root, dist, filename):

    mid = MidiFile(root + filename)
    all_time = 0
    global_end = 0

    # print(mid.ticks_per_beat)

    f = open(dist+filename+'.txt', 'w')

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
            f.write('------------------------------\n')
            for i in range(len(track)):
                if 'meta' not in str(track[i]):
                    # 抽出时间
                    relink = 'time=(.*)'
                    cinfo = re.findall(relink, str(track[i]))
                    time = int(cinfo[0])
                    if 'note' in str(track[i]): #and track[i].channel == 9
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
                                    f.write("%-4s     %.4f     %.4f     %.4f\n" % (note, normal_beats(ticks2beats(start)),
                                                                               normal_beats(ticks2beats(end)), diff))
                                global_end = normal_beats(ticks2beats(end))
                                note_arr.append(note)
                                t = int((normal_beats(ticks2beats(end)) - normal_beats(ticks2beats(start))) * 16)
                                time_arr.append(t)

                    all_time += time

    if tag == 1:
        for j, track in enumerate(mid.tracks):
            f.write('------------------------------\n')
            for i in range(len(track)):
                if 'meta' not in str(track[i]):
                    # 抽出时间
                    relink = 'time=(.*)'
                    cinfo = re.findall(relink, str(track[i]))
                    time = int(cinfo[0])
                    if 'note' in str(track[i]): #and track[i].channel == 9
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
                                    f.write("%-4s     %.4f     %.4f     %.4f\n" % (note, normal_beats(ticks2beats(start)),
                                                                               normal_beats(ticks2beats(end)), diff))
                                global_end = normal_beats(ticks2beats(end))
                                note_arr.append(note)
                                t = int((normal_beats(ticks2beats(end)) - normal_beats(ticks2beats(start))) * 16)
                                time_arr.append(t)

                    all_time += time

    line.append(note_arr)
    line.append(time_arr)
    fw.write(str(line))
    fw.write('\n')
    print(str(line))


if __name__ == '__main__':
    #get_rap('', '', 'f1.mid')
    extract_track('', '', 'Anonym_El_Noy_de_la_Mare.mid')

    root = 'C:\\Users\\v-honzhu\\Desktop\\guitar\\'

    dist = 'C:\\Users\\v-honzhu\\Desktop\\guitar_txt\\'

    id = []
    for p, d, filenames in os.walk(root):
        for filename in filenames:
            try:
                extract_track(root, dist, filename)
            except:
                print(filename)



