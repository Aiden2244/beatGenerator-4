"""
music.py
Created by Aiden McCormack on 11-13-2022

Stores some information that is useful for the entire program, such as
note values, a procedure for converting note values to strings, and more

© Copyright Aiden McCormack, 2022-2023, All rights reserved.
"""

from random import randint

# assigns numeric offsets to note names (all sharps represented as flats)
middle_c = 60
c = 0
db = 1
d = 2
eb = 3
e = 4
f = 5
gb = 6
g = 7
ab = 8
a = 9
bb = 10
b = 11
OCTAVE = 12

# the inverse of the above---relates offset to a string
NOTES = (
    'C',
    'Db',
    'D',
    'Eb',
    'E',
    'F',
    'Gb',
    'G',
    'Ab',
    'A',
    'Bb',
    'B'
)


# takes a triad as an input and outputs the string representation of the triad
def determine_triad_identity(chord=(60, 64, 67)):
    type_of_chord = 'undefined'
    fifth = chord[2]
    third = chord[1]
    root = chord[0]

    if third < root:
        third += OCTAVE
    if fifth < root:
        fifth += OCTAVE

    if third-root == 4:
        type_of_chord = 'major'
    elif third-root == 3:
        if fifth-third == 4:
            type_of_chord = 'minor'
        else:
            type_of_chord = 'diminished'

    while root >= OCTAVE:
        root -= OCTAVE

    root_note_str = NOTES[root]

    print(root_note_str + ' ' + type_of_chord, end=" ")
    return [root_note_str, type_of_chord]


# a list for keeping track of arpeggio patterns. The numbers in the tuples correspond to the
# index of the note of the scale. Patterns are all four notes long since the more complicated
# melodic stuff will be handled by the solo function.
# NOTE: It is assumed that the scale being referenced is a heptatonic scale (major scale or some mode of it).
PATTERNS = [

    (0, 1, 2, 1),
    (0, 1, 0, 2),

]

# TRACK INSTRUMENT HANDLING
# tracks are handled as follows:
#   Track 0 = Chords
#   Track 1 = Bass
#   Track 2 = Arpeggio
#   Track 3 = Melody
#   Track 4 = Kick
#   Track 5 = Snare


# These lists are the program numbers for specific categories of instruments


# Below is a list of tuples. The tuple's place in the list corresponds to the instrument channel
# it programs. The numbers within the list are the midi instruments that can be used
PIANOS = [0, 4, 5]
DRUMS = [9, 73]
ELEC_DRUMS = [118, 119, 118]
PERCUSSION = [10, 11, 12, 13]
ROCK_ORGANS = [16, 17, 18]
TRAD_ORGANS = [19, 20, 21, 22, 82]
ACOUSTIC_GUITARS = [31, 15]
ELEC_GUITARS = [26, 28, 29]
BASSES = [32, 33, 34, 35]
SYNTH_BASSES = [38, 39]
ORCHESTRAL = [40, 41, 55, 56, 58, 60, 64, 68, 69, 71, 74]
LEAD_SYNTHS = [80, 83, 84, 86, 87, 112, 14]  # omitted 81
PADS = [53, 76, 75, 85, 62, 51, 88, 90, 92, 93, 50, 94, 95, 96,
        99, 101, 102, 103, 122]

# initializes a list of lists. Each list in the list lists the program numbers
# each track will be able to use, and these numbers are selected by instrument type.
INSTRUMENTS = [
    [],  # chords 0
    [],  # bass 1
    [],  # moving chords 2
    [],  # arp 3
    [],  # melody 4
    [],  # kick 5
    [],  # snare 6

]

# The thing that does the selecting
INSTRUMENTS[0] += (PIANOS + TRAD_ORGANS + ROCK_ORGANS + ORCHESTRAL + PADS)
INSTRUMENTS[1] += (BASSES + SYNTH_BASSES)
INSTRUMENTS[2] += (PIANOS + TRAD_ORGANS + PADS + ORCHESTRAL)
INSTRUMENTS[3] += (PIANOS + ROCK_ORGANS + PERCUSSION)
INSTRUMENTS[4] += (LEAD_SYNTHS + PIANOS + ELEC_GUITARS + ROCK_ORGANS)
INSTRUMENTS[5] += ELEC_DRUMS
INSTRUMENTS[6] += ELEC_DRUMS


def get_instrument_val(i):
    cur_list = INSTRUMENTS[i]
    max_index = len(cur_list) - 1
    rand_index = randint(0, max_index)
    print("Generating track " + str(i) + " with random index " + str(rand_index))
    print(cur_list[rand_index])
    return cur_list[rand_index]
