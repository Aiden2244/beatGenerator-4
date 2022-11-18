from midiutil.MidiFile import MIDIFile

index = 0
midi = MIDIFile(16)
for i in range(129):
    if i % 16 == 0:
        outstring = "sounds_" + str(i) + ".mid"
        with open(outstring, 'wb') as mid:
            midi.writeFile(mid)
        index = 0
        midi = MIDIFile(16)
    midi.addProgramChange(tracknum=index, channel=index, time=0, program=i)
    midi.addNote(index, index, 60, 0, 4, 100)
    index += 1
