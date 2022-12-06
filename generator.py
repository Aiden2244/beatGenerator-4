from music import *
from beat import Beat
import os

# CONTROL PANEL

GUI = True  # enables the graphical user interface

force_unique = True  # disables the repetition of chords in the beat progression if true
force_root = True  # makes the first chord in the progression the tonic chord if true
omit_diminished = True  # the progression will not include diminished chords if true
random_instruments = True  # the instruments in each track will be set to their defaults if false
octave = 0  # the octave offset of the beat, affects all tracks [-3, 5]

# FOR EACH OF THE FOLLOWING, SET THE VALUE TO -1 FOR THE DEFAULT
key = c  # the root note of the beat (c, db, d, eb, e, ... , bb, b OR any int [0, 11] )
mode = -1  # the mode of the beat (0=major/1=minor)
tempo = -1  # the tempo of the beat in bpm
arp_pattern = -1  # specifies which arp pattern to use from the PATTERNS list in music.py [0,1]
arp_duration = -1  # specifies the note duration of the melody and arpeggio
bass_note_len = -1  # specifies the note duration of the bass note
prog_len = -1  # the number of chords to include within the progression (if >7, disables force_unique)
drum_mode = -1  # the mode to use for generating the drums [0, 1]
num_phrases = -1  # the number of 4-measure loops to generate [1, ]

def generate():
    if GUI:
        __OUTPUT__ = Beat()
        __OUTPUT__.info()
        __OUTPUT__.write()
        os.system("open -a GarageBand.app output.mid")

    else:
        # Starts ui sequence
        first_input = input("Press 'return' to generate a beat! (or type 't' to terminate) >> ")
        if first_input == 't':
            print("Terminated. No beat generated.")
            return False
        elif first_input == 'c':
            print("Custom mode activated. Generating beat with hardcoded settings...")
            __OUTPUT__ = Beat(
                    key=key,
                    mode=mode,
                    octave=octave,
                    tempo=tempo,
                    prog_len=prog_len,
                    bass_note_len=bass_note_len,
                    force_unique=force_unique,
                    force_root=force_root,
                    omit_diminished=omit_diminished,
                    random_instruments=random_instruments,
                    arp_pattern=arp_pattern,
                    arp_duration=arp_duration,
                    drum_mode=drum_mode,
                    num_phrases=num_phrases
                    )
        else:
            print("Generating...")
            __OUTPUT__ = Beat()
        print("done!")

        __OUTPUT__.info()
        __OUTPUT__.write()
        os.system("open -a GarageBand.app output.mid")

        return True
