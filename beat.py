"""
beat.py
Created by Aiden McCormack on 11-13-2022

This file declares the Beat object, which encapsulates all of the information
needed to generate and write the beat.



    TODO:
        -   I've decided I dont want lay folk editing the details of the beat. Change UI to be simpler.
        -   The beat itself could be substantially longer. The program pretty much just produces loops,
            so either hardcode a structure you want it to follow or set constraints on how the beat can
            do it itself.
        -   Implement a working dev mode where you can modify details of the beat for debugging reasons.
        -   Edit volume options so the track mixes a little better.
        -   Can it pan? Should it pan?
        -   Improve UX by reading keyboard inputs directly instead of using string inputs
        -   Package this to organize it more

© Copyright Aiden McCormack, 2022, All rights reserved.
"""

from midiutil.MidiFile import MIDIFile
from music import *
from random import randint
from copy import deepcopy


class Beat:

    def __init__(self, key=c, rand_key=True, mode='major', rand_mode=True,
                 force_unique=True, force_root=True, omit_diminished=True, octave=0, arp_pattern=0,
                 arp_duration=.25, rand_arp=True):
        self.mode = self.select_mode(user_mode=mode, random=rand_mode)
        self.key = self.select_key(user_key=key, random=rand_key)
        self.root = middle_c + self.key
        self.tempo = self.set_tempo()
        self.scale = self.determine_scale()
        self.chords = self.generate_chords()
        self.prog = self.select_progression(force_unique=force_unique,
                                            force_root=force_root, omit_diminished=omit_diminished)
        self.octave = octave
        self.midi = self.initialize_midi()
        self.select_instruments()
        self.arp_pattern = self.select_arpeggio(user=arp_pattern, random=rand_arp)
        self.write_progression()
        self.write_bassline()
        self.write_arpeggio_and_melody(pattern_index=self.arp_pattern, note_duration=arp_duration)

    def select_mode(self, random=True, user_mode='major'):
        selector = randint(0, 10000)
        mode = user_mode
        if random:
            if selector > 5000:
                mode = 'minor'
            else:
                mode = 'major'
        return mode

    def select_key(self, random=True, user_key=c):
        selector = randint(0, 11)
        key = user_key
        if random:
            key = selector
        return key

    def determine_scale(self):
        if self.mode == 'major':
            scale = [c, d, e, f, g, a, b]
        elif self.mode == 'minor':
            scale = [c, d, eb, f, g, ab, bb]
        else:
            print("Error: invalid scale mode")
            return

        for i in range(len(scale)):
            scale[i] += self.root
        return scale

    def print_scale(self):
        print(NOTES[self.key] + ' ' + self.mode)

    def print_notes(self):
        print("Notes: ", end='')
        scale_copy = deepcopy(self.scale)
        for i in range(len(self.scale)):
            while scale_copy[i] >= OCTAVE:
                scale_copy[i] -= OCTAVE
            print(NOTES[scale_copy[i]], end=' ')
        print()

    def generate_chords(self):
        """
        generates every triad that works in the given key

        :return: a list of chords, which are tuples of ints
        """
        chords = []
        for i in range(len(self.scale)):
            chord = []
            cur = i
            while len(chord) != 3:
                if cur > (len(self.scale)-1):
                    cur -= (len(self.scale))
                chord.append(self.scale[cur])
                cur += 2
            chords.append(chord)
        return chords

    def print_chords(self):
        print("Chords: ", end='')
        for i in range(len(self.chords)):
            determine_triad_identity(self.chords[i])
        print()

    def select_progression(self, length=4, force_unique=True, force_root=True, omit_diminished=True):
        """
        from the generated chords, make a progression of a specified length (default=4)
        """
        progression = []
        chords_copy = deepcopy(self.chords)
        if omit_diminished:
            if self.mode == 'minor':
                chords_copy.pop(1)
            else:
                chords_copy.pop(len(chords_copy)-1)
        for i in range(length):
            max_index = len(chords_copy)-1
            index = randint(0, max_index)
            if force_root and (i == 0):
                index = 0
            progression.append(chords_copy[index])
            if force_unique:
                chords_copy.pop(index)
        return progression

    def select_arpeggio(self, user, random=True):
        val = user
        if random:
            return randint(0, len(PATTERNS)-1)
        return val

    def print_progression(self):
        print("Progression: ", end='')
        for i in range(len(self.prog)):
            determine_triad_identity(self.prog[i])
        print()

    def write_bassline(self, num_phrases=1, note_duration=0.5, start_time=0):
        current_time = start_time
        for i in range(len(self.prog)):
            cur = self.prog[i]
            root = cur[0]
            if root > (middle_c + a):
                root -= OCTAVE
            root -= (2*OCTAVE)
            total_duration = 0

            for j in range(num_phrases):
                while total_duration < 4:
                    self.midi.addNote(track=1, channel=1, pitch=root,
                                      time=current_time, duration=note_duration, volume=100)
                    total_duration += note_duration
                    current_time += note_duration

    def write_arpeggio_and_melody(self, num_phrases=1, note_duration=0.25, start_time=0, pattern_index=0):
        current_time = start_time
        pattern = PATTERNS[pattern_index]
        # this is definitely the most efficient algorithm for this task
        # this code loops the whole shebang as many times as num phrases is set
        for l in range(num_phrases):
            arp_note_counter = 0
            # this code changes the chord
            for k in range(len(self.prog)):
                chord = self.prog[k]
                # this code outputs the sequence of notes for a given chord
                for j in range(int(1/note_duration)):
                    # this code outputs all the notes of the arpeggio exactly once
                    for i in range(len(pattern)):
                        cur_index = pattern[i]
                        arp_pitch = chord[cur_index] - 12
                        mel_pitch = arp_pitch +12
                        mel_pitch = self.tamper(mel_pitch)

                        if not mel_pitch == 0:
                            self.midi.addNote(track=3, channel=3, pitch=mel_pitch,
                                              time=current_time, duration=note_duration, volume=100)
                        if arp_note_counter % 2 == 0:
                            self.midi.addNote(track=2, channel=2, pitch=arp_pitch,
                                              time=current_time, duration=(2*note_duration), volume=100)
                            self.midi.addNote(track=2, channel=2, pitch=arp_pitch+g,
                                              time=current_time, duration=(2 * note_duration), volume=100)
                        current_time += note_duration
                        arp_note_counter += 1

    def tamper(self, val):
        """
        This function uses some basic random logic to make somewhat interesting random melodies
        :param val: the pitch that is getting messed with
        :return: likely the same value, but sometimes an octave lower or higher
        """
        selector = randint(0, 16384)
        if selector % 3 == 0:
            val -= OCTAVE
        elif selector % 2 == 0:
            val += g
        elif selector % 5 == 0:
            val += OCTAVE
        return val

    def info(self):
        print()
        print("BEAT INFO:")
        print()
        print("Key Info")
        print("Key: ", end='')
        self.print_scale()
        self.print_notes()
        self.print_chords()
        self.print_progression()
        print()
        print("Beat Info")
        print("Tempo: " + str(self.tempo))
        print("Arpeggio Pattern: " + str(self.arp_pattern))
        print()

    """
    below here are functions dedicated to the midi
    """

    def set_tempo(self, tempo_min=90, tempo_max=180, random_tempo=True, user_tempo=120):
        self.tempo = user_tempo
        if random_tempo:
            self.tempo = randint(tempo_min, tempo_max)
        return self.tempo

    def initialize_midi(self, num_tracks=len(INSTRUMENTS)):
        midi = MIDIFile(num_tracks)
        for i in range(num_tracks):
            midi.addTempo(track=i, time=0, tempo=self.tempo)
        return midi

    def select_instruments(self, mode='random'):
        if mode == 'default':
            pass
        elif mode == 'random':
            for i in range(len(INSTRUMENTS)):
                program = get_instrument_val(i)
                self.midi.addProgramChange(tracknum=i, channel=i, time=0, program=program)

    def write(self, filename='output.mid'):
        with open(filename, 'wb') as outf:
            self.midi.writeFile(outf)
        print("Wrote midi to file " + filename + " in current directory")

    def write_progression(self, chord_length=4, starting_beat=0, chord_spacing=4):
        for i in range(len(self.prog)):
            current_chord = self.prog[i]
            current_time = starting_beat + (chord_spacing*i)
            for j in range(len(current_chord)):
                pitch = current_chord[j]
                self.midi.addNote(track=0, channel=0, pitch=(pitch+(12*self.octave)),
                                  time=current_time, duration=chord_length, volume=100)
