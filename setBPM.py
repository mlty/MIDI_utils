#encoding=utf-8
from mido import MidiFile
from mido import MetaMessage
import re
import os
import os.path
import glob
import music21
import os
import shutil

def setBPM(root, dist, filename):
    mid = MidiFile(root+filename)

    for j, track in enumerate(mid.tracks):
            for i in range(len(track)):
                if track[i].type == 'set_tempo':
                    track[i].tempo = 1000000

    mid.save(dist+filename)


if __name__ == '__main__':


    rootdir = "C:\\Users\\v-honzhu\\Desktop\\data_3\\"
    dist = "C:\\Users\\v-honzhu\\Desktop\\bpm\\"

    fw = open('rw.txt', 'w')

    count = 0

    for p, d, filenames in os.walk(rootdir):
        for filename in filenames:
            try:
                setBPM(rootdir, dist, filename)
            except:
                print(filename)
                #fw.write(filename+"\n")