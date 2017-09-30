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
track_w.append(Message('note_off', channel=9, note=36, velocity=64, time=36*2))
track_w.append(Message('note_off', channel=9, note=49, velocity=64, time=0))
track_w.append(Message('note_on', channel=9, note=42, velocity=68, time=89*2))
track_w.append(Message('note_off', channel=9, note=42, velocity=64, time=37*2))


track_w.append(MetaMessage('end_of_track', time=0))


mid.save('1.mid')