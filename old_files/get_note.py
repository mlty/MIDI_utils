#encoding=utf-8

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

if __name__ == '__main__':
    get_note('','','2OfAmerikasMostWanted.mid')

'''
    fe = open('error.txt', 'w')

    root = 'C:\\Users\\v-honzhu\\Desktop\\single_rap\\'

    dist = 'C:\\Users\\v-honzhu\\Desktop\\txt\\'

    for p, d, filenames in os.walk(root):
        for filename in filenames:
            try:
                get_note(root, dist, filename)
            except:
                fe.write(filename)


    fe = open('error.txt', 'w')

    root = 'C:\\Users\\v-honzhu\\Desktop\\mid_single\\mid\\'

    f = open('r_midi.txt', 'r')

    id = []
    for p, d, filenames in os.walk(root):
        for filename in filenames:
            n = filename.replace('.mid', '')
            id.append(n)

    id = set(id)

    count = 0
    for i in f:
        line = i.replace('\n', '')
        if line in id:
            try:
                get_note(root, line+'.mid')
                count += 1
                print(count)
            except:
                fe.write(line+"\n")
'''







