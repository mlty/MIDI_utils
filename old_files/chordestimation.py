#coding:utf-8
from collections import OrderedDict

import numpy as np

import midi as md
from utils import functions as fn


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

get_chords("CC_35")


'''
    #---------------------------------------------------------------------------------------------------------------------
    # 以上是和弦计算 下面是进行和弦和音符匹配

    def note2chord(start, end):
        for i in range(len(chord)):
            if chord[i][0] <= start and end <= chord[i][1]:
                return chord[i][2]
        return None

    mid = MidiFile(midifile+file_midi)
    tempo = 652174
    for msg in mid:
        if msg.type == 'set_tempo':
            tempo = msg.tempo

    def triks2time(t):
        return t*(tempo * 1e-6 / mid.ticks_per_beat)

    def ticks2beats(t):
        return t / mid.ticks_per_beat


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


    t = []
    all_time = 0
    bar = 1
    b_time = 0

    print("%d   bar     " % (bar))
    f.write("%d   bar     \n" % (bar))

    for j, track in enumerate(mid.tracks):
        for i in range(len(track)):
            if 'note' in str(track[i]) and 'time' in str(track[i]) and 'velocity' in str(track[i]):
                # note
                relink = 'note=(.+?) velocity'
                cinfo = re.findall(relink, str(track[i]))
                note = table[int(cinfo[0])]

                # time
                relink = 'time=(.*)'
                cinfo = re.findall(relink, str(track[i]))
                time = int(cinfo[0])

                t.append(time)

                # velocity
                relink = 'velocity=(.+?) time'
                cinfo = re.findall(relink, str(track[i]))
                velocity = int(cinfo[0])

                if velocity == 0:
                    start = all_time + triks2time(t[0])
                    end = start + triks2time(t[1])
                    all_time = end

                    b_start = b_time + ticks2beats(t[0])
                    b_end = b_start + ticks2beats(t[1])
                    b_time = b_end

                    t = []

                    if start > m[bar] and bar < m_length-1:
                        print("%d   bar     " % (bar+1))
                        f.write("%d   bar     \n" % (bar+1))
                        bar += 1
                    #print("%-4s  | %.2f | %.2f | %-4s" % (note, b_start, b_end, note2chord(start,end)))
                    print("[%.2f - %.2f]  %-4s %-4s" % (b_start, b_end, note, note2chord(start, end)))
                    f.write("[%.2f - %.2f]  %-4s %-4s\n" % (b_start, b_end, note, note2chord(start, end)))
'''