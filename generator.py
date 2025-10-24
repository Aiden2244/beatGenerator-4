from music import *
from beat import Beat
import os

"""
generator.py

This is basically the config file for the program.

This part of the program is still in development,
and some features may not work as intended if they are not set to random. Each variable has a comment
next to it briefly explaining what aspect of the music generation is affected by altering the variable
value.

The boolean variables, generally, control the user interface and minimize the "chaos" of the
generated beats when set to true. I would recommend leaving them set to true unless you want to make
something that sounds pretty terrible.

The octave is not randomly selected. Changing the octave setting will change the octave of every track.
Feel free to experiment with it, but the program works best when it is set to 0.

The other variables are the randomly-determined elements of the music generation process. Setting the
value of any of these variables to -1 will have the program randomly generate the value. This allows
you to manually assign only certain values, like the key or the tempo, without having to manually
assign EVERY value.
"""


""" CONTROL PANEL """

GUI = True  # enables the graphical user interface (false runs the CLI)
force_unique = True  # disables the repetition of chords in the beat progression if true
force_root = True  # makes the first chord in the progression the tonic chord if true
omit_diminished = True  # the progression will not include diminished chords if true
random_instruments = (
    True  # the instruments in each track will be set to their defaults if false
)

octave = 0  # the octave offset of the beat, affects all tracks [-3, 5] (0 is default)

# FOR EACH OF THE FOLLOWING, SET THE VALUE TO -1 FOR THE DEFAULT
key = -1  # the root note of the beat (c, db, d, eb, e, ... , bb, b OR any int [0, 11] (-1=random) )
mode = -1  # the mode of the beat (0=major/1=minor, -1=random)
tempo = -1  # the tempo of the beat in bpm
arp_pattern = (
    -1
)  # specifies which arp pattern to use from the PATTERNS list in music.py [0,1]
arp_duration = -1  # specifies the note duration of the melody and arpeggio
bass_note_len = -1  # specifies the note duration of the bass note
prog_len = -1  # the number of chords to include within the progression (if >7, disables force_unique)
drum_mode = -1  # the mode to use for generating the drums [0, 1]
num_phrases = -1  # the number of 4-measure loops to generate [1, ]

""" END CONTROL PANEL """


def generate():
    if GUI:
        output = Beat(
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
            num_phrases=num_phrases,
        )
        output.info()
        output.write()
        os.system("open -a GarageBand.app output.mid")

    else:
        # Starts ui sequence
        first_input = input(
            "Press 'return' to generate a beat! (or type 't' to terminate) >> "
        )
        if first_input == "t":
            print("Terminated. No beat generated.")
            return False
        elif first_input == "c":
            print("Custom mode activated. Generating beat with hardcoded settings...")
            output = Beat(
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
                num_phrases=num_phrases,
            )
        else:
            print("Generating...")
            output = Beat()
        print("done!")

        output.info()
        output.write()
        os.system("open -a GarageBand.app output.mid")

        return True
