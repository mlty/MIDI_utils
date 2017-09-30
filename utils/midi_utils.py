#coding:utf-8
import glob
from collections import OrderedDict

import music21
import numpy as np

#import midi as md
from utils import functions as fn

from mido import MidiFile
import re
import os
import os.path

table={}
table[24] = table[0] = table[12] = 'C1'
table[25] = table[1] = table[13] = table[73] = table[85] = table[97] = table[109] = table[121] = 'Db'
table[26] = table[2] = table[14] = table[110] = table[122] = 'D'
table[27] = table[3] = table[15] = table[75] = table[87] = table[99] = table[111] = table[123] = 'Eb'
table[28] = table[4] = table[16] = table[76] = table[88] = table[100] = table[112] = table[124] = 'E'
table[29] = table[5] = table[17] = table[77] = table[89] = table[101] = table[113] = table[125] = 'F'
table[30] = table[6] = table[18] = table[78] = table[90] = table[102] = table[114] = table[126] = 'Gb'
table[31] = table[7] = table[19] = table[79] = table[91] = table[103] = table[115] = table[127] = 'G'
table[32] = table[8] = table[20] = table[80] = table[92] = table[104] = table[116] = 'Ab'
table[33] = table[9] = table[21] = table[81] = table[93] = table[105] = table[117] = 'A'
table[34] = table[10] = table[22] = table[82] = table[94] = table[106] = table[118] = 'Bb'
table[35] = table[11] = table[23] = table[83] = table[95] = table[107] = table[119] = 'B'
table[60] = table[36] = table[48] = 'C4'
table[61] = table[37] = table[49] = 'Db'
table[62] = table[74] = table[38] = table[50] = table[86] = table[98] = 'D'
table[63] = table[39] = table[51] = 'Eb'
table[64] = table[76] = table[40] = table[52] = 'E'
table[65] = table[41] = table[53] = 'F'
table[66] = table[42] = table[54] = 'Gb'
table[67] = table[43] = table[55] = 'G'
table[68] = table[44] = table[56] = 'Ab'
table[69] = table[45] = table[57] = 'A'
table[70] = table[46] = table[58] = 'Bb'
table[71] = table[47] = table[59] = 'B'
table[72] = table[84] = table[96] = 'C7'
table[108] = table[120] = 'C10'

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


# 将MIDI转换成C调
def get_C():

    majors = dict(
        [("A-", 4), ("A", 3), ("B-", 2), ("B", 1), ("C", 0), ("D-", -1), ("D", -2), ("E-", -3), ("E", -4), ("F", -5),
         ("G-", 6), ("G", 5)])

    minors = dict(
        [("A-", 1), ("A", 0), ("B-", -1), ("B", -2), ("C", -3), ("D-", -4), ("D", -5), ("E-", 6), ("E", 5), ("F", 4),
         ("G-", 3), ("G", 2)])


    for file in glob.glob("B_12081.mid"):

        score = music21.converter.parse(file)

        key = score.analyze('key')

        if key.mode == "major":

            halfSteps = majors[key.tonic.name]

        elif key.mode == "minor":

            halfSteps = minors[key.tonic.name]

        newscore = score.transpose(halfSteps)

        key = newscore.analyze('key')

        print(key.tonic.name, key.mode)

        newFileName = "C_" + file

        newscore.write('midi', newFileName)

# 得到MIDI和弦
def get_chords(midifile):

    file_wav = ".wav"
    file_midi = ".mid"
    f = open(midifile+'.txt', 'w')

    chroma = fn.librosa_chroma(midifile+file_wav)

    TONES = 12
    sampling_rate = 44100

    time_unit = 512.0 / 44100
    stop = time_unit * (chroma.shape[1])
    time_ruler = np.arange(0, stop, time_unit)

    one_third = 1.0/3
    chord_dic = OrderedDict()
    chord_dic["C"] = [one_third, 0,0,0, one_third, 0,0, one_third, 0,0,0,0]
    chord_dic["Db"] = [0, one_third, 0,0,0, one_third, 0,0, one_third, 0,0,0]
    chord_dic["D"] = [0,0, one_third, 0,0,0, one_third, 0,0, one_third, 0,0]
    chord_dic["Eb"] = [0,0,0, one_third, 0,0,0, one_third, 0,0, one_third, 0]
    chord_dic["E"] = [0,0,0,0, one_third, 0,0,0, one_third, 0,0, one_third]
    chord_dic["F"] = [one_third, 0,0,0,0, one_third, 0,0,0, one_third, 0,0]
    chord_dic["Gb"] = [0, one_third, 0,0,0,0, one_third, 0,0,0, one_third, 0]
    chord_dic["G"] = [0,0, one_third, 0,0,0,0, one_third, 0,0,0, one_third]
    chord_dic["Ab"] = [one_third, 0,0, one_third, 0,0,0,0, one_third, 0,0,0]
    chord_dic["A"] = [0, one_third, 0,0, one_third, 0,0,0,0, one_third, 0,0]
    chord_dic["Bb"] = [0,0, one_third, 0,0, one_third, 0,0,0,0, one_third, 0]
    chord_dic["B"] = [0,0,0, one_third, 0,0, one_third, 0,0,0,0, one_third]
    chord_dic["Cm"] = [one_third, 0,0, one_third, 0,0,0, one_third, 0,0,0,0]
    chord_dic["Dbm"] = [0, one_third, 0,0, one_third, 0,0,0, one_third, 0,0,0]
    chord_dic["Dm"] = [0,0, one_third, 0,0, one_third, 0,0,0, one_third, 0,0]
    chord_dic["Ebm"] = [0,0,0, one_third, 0,0, one_third, 0,0,0, one_third, 0]
    chord_dic["Em"] = [0,0,0,0, one_third, 0,0, one_third, 0,0,0, one_third]
    chord_dic["Fm"] = [one_third, 0,0,0,0, one_third, 0,0, one_third, 0,0,0]
    chord_dic["Gbm"] = [0, one_third, 0,0,0,0, one_third, 0,0, one_third, 0,0]
    chord_dic["Gm"] = [0,0, one_third, 0,0,0,0, one_third, 0,0, one_third, 0]
    chord_dic["Abm"] = [0,0,0, one_third, 0,0,0,0, one_third, 0,0, one_third]
    chord_dic["Am"] = [one_third, 0,0,0, one_third, 0,0,0,0, one_third, 0,0]
    chord_dic["Bbm"] = [0, one_third, 0,0,0, one_third, 0,0,0,0, one_third, 0]
    chord_dic["Bm"] = [0,0, one_third, 0,0,0, one_third, 0,0,0,0, one_third]


    prev_chord = 0
    sum_chroma = np.zeros(TONES)
    estimate_chords = []

    mm = md.get_track_time(midifile+file_wav)

    m = []
    num = float(mm[0])/(mm[1]-mm[0])
    l = int(round(num))
    m.append(0.0)

    count = l
    for i in range(len(mm)):
        if count < 3:
            count += 1
        else:
            count = 0
            m.append(mm[i])


    m_length = len(m)
    length = 0
    sum_chroma = np.zeros(TONES)

    chord = []
    for time_index, time in enumerate(time_ruler):

        if length < m_length-1:
            if time > m[length] and time < m[length+1]:
                for i in range(TONES):
                    sum_chroma[i] += chroma[i][time_index]
            elif time >= m[length+1]:
                maximum = -100000
                this_chord = ""

                for chord_index, (name, vector) in enumerate(chord_dic.items()):
                    similarity = fn.cos_sim(sum_chroma, vector)

                    if similarity > maximum:
                        maximum = similarity
                        this_chord = name

                sum_chroma = np.zeros(TONES)
                estimate_chords.append(this_chord)
                print("%.2f  | %.2f | %-4s | (%.2f)" % (m[length], m[length+1], this_chord, maximum))
                chord.append([m[length], m[length+1], this_chord])
                length += 1



    print(estimate_chords)

def clip():
    import os.path
    import shutil

    rootdir = "/home/honzhu/c++/ext/miditest/test/"
    dir = []
    dir.append("/home/honzhu/c++/ext/miditest/w1/")
    dir.append("/home/honzhu/c++/ext/miditest/w2/")
    dir.append("/home/honzhu/c++/ext/miditest/w3/")
    dir.append("/home/honzhu/c++/ext/miditest/w4/")
    dir.append("/home/honzhu/c++/ext/miditest/w5/")

    count = 0
    for p, d, filenames in os.walk(rootdir):
        for filename in filenames:
            c = count % 5
            shutil.copy(rootdir + filename, dir[c] + filename)
            if os.path.isfile(dir[c] + filename):
                print(filename + "Success")
            count += 1
            print(count)

def get_major(filename):
    from mido import MidiFile
    import re
    import os
    import os.path

    count = 0

    def get_key(filename):
        mid = MidiFile(filename)

        # f = open("/home/honzhu/c++/ext/miditest/note2/"+filename+'.txt', 'w')

        for j, track in enumerate(mid.tracks):
            for i in range(len(track)):
                print(track[i])

    get_key(filename)

def get_note(root, dist, filename):

    mid = MidiFile(root+filename)
    all_time = 0
    global_end = 0

    #print(mid.ticks_per_beat)

    f = open(dist+filename.replace('.mid','')+'.txt', 'w')

    def ticks2beats(t):
        return t / mid.ticks_per_beat

    tempo = 652174
    for msg in mid:
        if msg.type == 'set_tempo':
            tempo = msg.tempo

    #print(tempo)

    def ticks2time(t):
        return t * (tempo * 1e-6 / mid.ticks_per_beat)


    noteList = {}
    #print("note  beat_start  beat_end  time_start  time_end")

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
            for i in range(len(track)):
                if 'meta' not in str(track[i]):
                    # 抽出时间
                    relink = 'time=(.*)'
                    cinfo = re.findall(relink, str(track[i]))
                    time = int(cinfo[0])
                    if 'note' in str(track[i]):
                        # note
                        relink = 'note=(.+?) velocity'
                        cinfo = re.findall(relink, str(track[i]))
                        #note = table[int(cinfo[0])]
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
                                #f.write("%-4s     %.3f     %.3f     %.2f     %.2f\n" % (note, normal_beats(ticks2beats(start)),
                                                                                        #normal_beats(ticks2beats(end)), ticks2time(start), ticks2time(end)))
                                if track[i].channel == 9:
                                    f.write("%-4s     %.4f     %.4f     %.4f\n" % (note, normal_beats(ticks2beats(start)),
                                                                                            normal_beats(ticks2beats(end)), diff))
                                global_end = normal_beats(ticks2beats(end))
                                note_arr.append(note)
                                t = int((normal_beats(ticks2beats(end))-normal_beats(ticks2beats(start)))*16)
                                time_arr.append(t)


                    all_time += time

    if tag == 1:
        for j, track in enumerate(mid.tracks):
            for i in range(len(track)):
                if 'meta' not in str(track[i]):
                    # 抽出时间
                    relink = 'time=(.*)'
                    cinfo = re.findall(relink, str(track[i]))
                    time = int(cinfo[0])
                    if 'note' in str(track[i]):
                        # note
                        relink = 'note=(.+?) velocity'
                        cinfo = re.findall(relink, str(track[i]))
                        #note = table[int(cinfo[0])]
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
                                #f.write("%-4s     %.3f     %.3f     %.2f     %.2f\n" % (
                                #note, normal_beats(ticks2beats(start)), normal_beats(ticks2beats(end)), ticks2time(start), ticks2time(end)))
                                #note_arr.append(note)

                                diff = normal_beats(ticks2beats(start)) - global_end
                                if diff < 0:
                                    diff = 0.0000

                                if track[i].channel == 9:
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

def get_rap():
    from mido import Message, MidiFile, MidiTrack, MetaMessage
    import re
    import os

    mid_read = MidiFile('test.mid')

    mid = MidiFile()
    track_w = MidiTrack()
    mid.tracks.append(track_w)

    track_w.append(MetaMessage('track_name', name='090 S01 Chorus F5', time=0))
    track_w.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24,
                               notated_32nd_notes_per_beat=8, time=0))
    track_w.append(MetaMessage('end_of_track', time=0))
    track_w.append(MetaMessage('set_tempo', tempo=666667, time=0))

    track_w.append(Message('note_on', channel=9, note=36, velocity=95, time=0))
    track_w.append(Message('note_on', channel=9, note=49, velocity=117, time=0))
    track_w.append(Message('note_off', channel=9, note=36, velocity=64, time=36 * 2))
    track_w.append(Message('note_off', channel=9, note=49, velocity=64, time=0))
    track_w.append(Message('note_on', channel=9, note=42, velocity=68, time=89 * 2))
    track_w.append(Message('note_off', channel=9, note=42, velocity=64, time=37 * 2))

    track_w.append(MetaMessage('end_of_track', time=0))

    mid.save('1.mid')

def setBPM(filename):
    # encoding=utf-8
    from mido import MidiFile
    from mido import MetaMessage
    import re
    import os
    import os.path
    import glob
    import music21

    def transformC(filename):

        mid = MidiFile(filename)
        # C 大调
        majors = dict(
            [("Ab", 4), ("A", 3), ("Bb", 2), ("B", 1), ("C", 0), ("Db", -1), ("D", -2), ("Eb", -3), ("E", -4),
             ("F", -5),
             ("Gb", 6), ("G", 5), ("C#", -1), ("D#", -3), ("F#", 6), ("G#", 4), ("A#", 2)])
        # A小调
        minors = dict(
            [("Ab", 1), ("A", 0), ("Bb", -1), ("B", -2), ("C", -3), ("Db", -4), ("D", -5), ("Eb", 6), ("E", 5),
             ("F", 4),
             ("Gb", 3), ("G", 2), ("C#", -4), ("D#", 6), ("F#", 3), ("G#", 1), ("A#", -1)])

        model = "major"
        ckey = "C"

        score = music21.converter.parse(filename)

        key = score.analyze('key')

        print(key.mode)

        model = key.mode

        for j, track in enumerate(mid.tracks):
            for i in range(len(track)):
                if track[i].type == 'key_signature':
                    ckey = track[i].key

                    if model == "major":
                        track[i].key = 'C'
                    else:
                        track[i].key = 'A'
                    break

        for j, track in enumerate(mid.tracks):
            for i in range(len(track)):
                if track[i].type == 'note_on' or track[i].type == 'note_off':
                    if model == "major":
                        track[i].note += majors[ckey]
                    else:
                        track[i].note += minors[ckey]
                if track[i].type == 'set_tempo':
                    track[i].tempo = 1000000

        mid.save('test_60.mid')

    mid = MidiFile(filename)

    for j, track in enumerate(mid.tracks):
            for i in range(len(track)):
                if track[i].type == 'set_tempo':
                    track[i].tempo = 1000000

    mid.save('3.mid')

def write_mid(s, g, filename):

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
                if i != len(cinfo) - 1:
                    str += cinfo[i] + ' '
                else:
                    str += cinfo[i]

            for i in range(len(cinfo1)):
                t = cinfo1[i].replace('[', '').replace(']', '').replace(' ', '')
                if t != '':
                    if i != len(cinfo1) - 1:
                        str1 += t + ' '
                    else:
                        str1 += t

            l.append(str)
            l.append(str1)

            lines.append(l)

        return lines

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




