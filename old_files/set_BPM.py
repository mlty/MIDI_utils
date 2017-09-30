#encoding=utf-8
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
        [("Ab", 4), ("A", 3), ("Bb", 2), ("B", 1), ("C", 0), ("Db", -1), ("D", -2), ("Eb", -3), ("E", -4), ("F", -5),
         ("Gb", 6), ("G", 5), ("C#", -1), ("D#", -3), ("F#", 6), ("G#", 4), ("A#", 2)])
    # A小调
    minors = dict(
        [("Ab", 1), ("A", 0), ("Bb", -1), ("B", -2), ("C", -3), ("Db", -4), ("D", -5), ("Eb", 6), ("E", 5), ("F", 4),
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


def setBPM(filename):
    mid = MidiFile(filename)

    for j, track in enumerate(mid.tracks):
            for i in range(len(track)):
                if track[i].type == 'set_tempo':
                    track[i].tempo = 1000000

    mid.save('3.mid')


if __name__ == '__main__':
    setBPM('Anything.mid')

'''
    rootdir = "C:\\Users\\v-honzhu\\Desktop\\rap\\"
    dist = "C:\\Users\\v-honzhu\\Desktop\\single_rap\\"

    fw = open('rw.txt', 'w')

    count = 0

    for p, d, filenames in os.walk(rootdir):
        for filename in filenames:
            try:
                setBPM(rootdir, dist, filename)
                count += 1

                if count %100 == 0:
                    print(count)
            except:
                print(filename)
                fw.write(filename+"\n")
'''