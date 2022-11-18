



HOW IT WORKS ------------------------------------------------------------------------------

beat.py does most of the "heavy lifting" for the program. From either user input,
random number generation, or a combination of both, this file programmatically
assembles the beat in the process detailed below.

    KEY DETERMINATION
    1.  Randomly generate an integer between [0, 10000). If the number is greater than 5000,
        then the beat will use a major key. Otherwise, the beat will use a minor key.

    2.  Choose an integer between [0,11] at random for the key value. This value essentially
        functions as the "offset" value that is used later on in the generation process. In
        terms of the music, 0=C, 1=Db/C#, 2=D ... 11=B.

    SCALE GENERATION
    3.  In MIDI representation, middle C (C3) equals 60. Adding 60 to the offset determined
        in step 2 produces the value for the root note of the program.

    4a. Determine which intervals the beat's scale should use based on whether the
        key is major or minor. These intervals are key-agnostic and depend entirely on the
        mode of the scale. These intervals are hard-coded as lists of ints, where the tonic
        note of the scale = 0 and every subsequent entry is how many semitones above the root
        the proceeding note is. To build the scale that the beat actually uses, add each value
        of the hard-coded interval to the root note value, and append it to a list called scale

    4b. By default, the previous step generates either the C major or C minor scale. To get
        other keys to work, add the key value determined in step 2 to each value in the scale
        list. This shifts each value in the scale a specified number of semitones to be in a
        certain key. For instance, G is 7 semitones above C, so to change the scale from C to
        G would require the program to add 7 to each value in the scales list.

    CHORD PROGRESSION GENERATION
    5.  The scale created in the steps above is the basis for all of the music the program
        generates. Triads are chords made of 3 notes within a given scale. These chords sound
        pleasant and are easy to produce algorithmically. To make a triad, choose any note of
        a major or minor scale. Then go 2 notes up in the scale to get the middle note and 4
        notes up from the start to get the top note. This produces every conventional chord
        associated with a scale and works for both major and minor scales. These chords are
        represented as tuples and are stored in a list called chords.

    6.  From the list of chords, randomly* choose 4 of them to use as the beat's progression.

            * The algorithm for selecting chords has a few options that can be toggled:
                -   force_root=True makes it so that the tonic chord of the scale is always
                        the first chord used in the progression.
                -   force_unique=True prevents a chord from being repeated in the progression
                -   omit_diminished=True does not let the progression used the diminished 7th
                        of the major scale (or diminished 2nd of the minor scale) in order to
                        keep the music generated to sound nice.

    ARPEGGIO, MELODY, AND BASS LINE GENERATION
    7.  The bass line is simple: iterate over the list of chords used in the beat called prog,
        (not to be confused with chords, which are the chords the beat CAN use and is a superset
        of prog), find the root note of the chord, drop it down a couple of octaves, and repeat it.
        That was easy.

    8a. The arpeggio is a little more complicated. The music.py file contains some hardcoded info
        on how to build the arpeggio. The arpeggio algorithm randomly selects a 4-int long tuple
        containing chord indexes. It then iterates over every chord in prog and outputs the
        notes (after lowering them by an octave) of the chord according to the pattern in the tuple.
        Simple, right? The way it actually does this is a little more complicated, but this is the
        necessary information.

    8b. Fundamentally, the melody is generated the same way that the arpeggio is, with some modifications.
        The melody starts with the same pattern as the arpeggio, then runs each value through a "tampering"
        method, which essentially:
            i.  Generates a random number in [0,10000]
            ii. Based on the number generated, can modify the note by changing its octave, raising
                it by a fifth, or simply omitting it from the melody.
        This relatively simple algorithm actually produces interesting yet pleasant sounding melodies.

    WRITING
    9.  In each of the aforementioned steps, where necessary, the data for the notes were written to
        a MIDIFile object from the midiutil.MidiFile module. The beat then gets written to a midifile,
        where it can be opened by a midi player or a DAW like logic