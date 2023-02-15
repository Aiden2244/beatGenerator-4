OVERVIEW ----------------------------------------------------------------------------------

This is a pure python program for macOS. Executing the program will prompt the user to
press a button that generates a brief piece of music in GarageBand. Each piece of music
is unique, 4 measures long, and uses an assortment of different instruments in order to
create variety. A combination of random number generation and constraints I have put in
place make it so each beat sounds different but maintains a degree of cohesiveness and
"listenability."

I wrote this program as a research project for a class on music and appropriation I took
during my time as an undergraduate at Georgetown University. The program, which uses no
AI at any stage of the process, generates a piece of music automatically according to a
strict, previously-defined template.

The source for this program is copyright protected, but any music generated from it is
free for the public to use.

The MIDI API is provided by the MIDIUtil python library, written by Mark Conway Wirt
and used with permission for educational purposes. The link to the docs is here:
https://midiutil.readthedocs.io/en/1.2.1/common.html



HOW TO USE --------------------------------------------------------------------------------

In order to use this program, you need to be using a computer running macOS and have
GarageBand installed (its free and on most Mac laptops, it should be by default). You
also need to have python 3 installed on your computer as well in order to run the program.
You can download the latest version from this website: https://www.python.org/downloads/ .
After you have set this up, proceed with the download and usage. I am assuming that the
user has no experience with Bash or programming, but even so it is relatively easy to
use the program.

    DOWNLOAD AND RUN
    1.  Download the repository "beatgenerator-4" from GitHub and move the folder called
        "beatGenerator-4" into your "Downloads" folder (it should go there by default).

    2.  In the "beatGenerator-4" folder, there will be a file called "Python Beat Generator"
        which will run the program if you click on it.

            NOTE: the program will not run unless
            the folder "beatGenerator-4" is within the "Downloads" folder on your system.

            (ADVANCED: for those familiar with Bash, all the executable does is run the command
            "$ python3 ~/Downloads/beatGenerator4" and if you want to move the directory elsewhere
            you can just edit the path in the exec file)

    3.  A window should pop up. Press the button that says "Generate Beat." It should automatically
        open up GarageBand to the brand new beat! Pressing "Generate Beat" will open both GarageBand
        and Terminal, and you can look at the output in the terminal to get information about the
        beat.

            NOTE: Sometimes, if GarageBand is not previously opened, the program will not take you to
            the generated beat. If you press "Generate Beat" and it opens GarageBand but does open up
            an untitled project, just press the "Generate Beat" button again.

    4. 	Repeat as many times as you like! The program will automatically stop once the window is
        closed.

    OPTIONAL: The program generates most of the information about the beat, such as its key signature
    and tempo using random number generation. This should be fine for the vast majority of users, but
    if you would like to manually specify information for your generated beats, you can change some
    of the settings in the "generator.py" file. More information on how to do that when is in the
    file itself.


HOW IT WORKS (FOR THE NERDS) --------------------------------------------------------------

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
        of the hard-coded interval to the root note value, and append it to a list called
        scale.

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
        of prog), find the root note of the chord, drop it down a couple of octaves, and repeat
        it. That was easy.

    8a. The arpeggio is a little more complicated. The music.py file contains some hardcoded info
        on how to build the arpeggio. The arpeggio algorithm randomly selects a 4-int long tuple
        containing chord indexes. It then iterates over every chord in prog and outputs the
        notes (after lowering them by an octave) of the chord according to the pattern in the
        tuple. Simple, right? The way it actually does this is a little more complicated, but this
        is the necessary information.

    8b. Fundamentally, the melody is generated the same way that the arpeggio is, with some
        modifications. The melody starts with the same pattern as the arpeggio, then runs each
        value through a "tampering" method, which essentially:
            i.  Generates a random number in [0,10000]
            ii. Based on the number generated, can modify the note by changing its octave, raising
                it by a fifth, or simply omitting it from the melody.
        This relatively simple algorithm actually produces interesting yet pleasant sounding
        melodies.

    WRITING
    9.  In each of the aforementioned steps, where necessary, the data for the notes were written
        to a MIDIFile object from the midiutil.MidiFile module. The beat then gets written
        to a midifile, where it can be opened by a midi player or a DAW like GarageBand.