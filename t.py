#encoding=utf-8
from mido import MidiFile
from mido import MetaMessage
import re
import os
import os.path
import glob
import music21

def setBPM(filename):
    mid = MidiFile(filename)

    for j, track in enumerate(mid.tracks):
            for i in range(len(track)):
                if track[i].type == 'set_tempo':
                    track[i].tempo = 1000000

    mid.save('33.mid')


if __name__ == '__main__':
    setBPM('3.mid')


