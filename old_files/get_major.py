from mido import MidiFile
import re
import os
import os.path

count = 0
def get_key(filename):
    mid = MidiFile(filename)

    #f = open("/home/honzhu/c++/ext/miditest/note2/"+filename+'.txt', 'w')

    for j, track in enumerate(mid.tracks):
        for i in range(len(track)):
            print(track[i])


if __name__ == '__main__':
    get_key('195.mid')

'''
    rootdir = "/home/honzhu/c++/ext/miditest/midishow_data/"

    global count

    for p, d, filenames in os.walk(rootdir):
        for filename in filenames:
            try:
                get_key(rootdir, filename)
                print(count)
            except:
                print(filename)
'''