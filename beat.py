"""
beat.py
Created by Aiden McCormack on 11-13-2022

This file declares the Beat object, which encapsulates all of the information
needed to generate and write the beat.



    TODO:
        -   The beat itself could be substantially longer. The program pretty much just produces loops,
            so either hardcode a structure you want it to follow or set constraints on how the beat can
            do it itself.
        -   Edit volume options so the track mixes a little better.

© Copyright Aiden McCormack, 2022, All rights reserved.
"""

from midiutil.MidiFile import MIDIFile
from music import *
from random import randint
from copy import deepcopy


class Beat:

    def __init__(self,
                 key=-1,
                 mode=-1,
                 octave=0,
                 tempo=-1,
                 prog_len=-1,
                 bass_note_len=-1,
                 force_unique=True,
                 force_root=True,
                 omit_diminished=True,
                 random_instruments=True,
                 arp_pattern=-1,
                 arp_duration=-1,
                 drum_mode=-1,
                 num_phrases=-1):
        self.num_phrases = num_phrases
        if num_phrases < 1:
            self.num_phrases = 1

        self.mode = self.select_mode(user_mode=mode)
        self.key = self.select_key(user_key=key)
        self.root = middle_c + self.key
        self.tempo = self.set_tempo(user_tempo=tempo)
        self.scale = self.determine_scale()
        self.chords = self.generate_chords()
        self.prog = self.select_progression(length=prog_len, force_unique=force_unique,
                                            force_root=force_root, omit_diminished=omit_diminished)
        self.octave = octave
        self.arp_pattern = arp_pattern
        self.midi = self.initialize_midi()
        self.select_instruments(random_instruments=random_instruments)
        self.write_progression(num_phrases=self.num_phrases)
        self.write_bassline(note_duration=bass_note_len, num_phrases=self.num_phrases)
        self.write_arpeggio_and_moving_chords(pattern=arp_pattern,
                                              note_duration=arp_duration, num_phrases=self.num_phrases)
        self.write_melody(num_phrases=self.num_phrases)
        self.drum_mode = self.write_drums(drum_mode=drum_mode, num_phrases=self.num_phrases)

    @staticmethod
    def select_mode(user_mode=-1):
        selector = 0
        if user_mode == -1:
            selector = randint(0, 10000)
        elif user_mode > 0:
            selector = 9999

        if selector > 5000:
            mode = 'minor'
        else:
            mode = 'major'
        return mode

    @staticmethod
    def select_key(user_key=-1):
        selector = randint(0, 11)
        key = user_key
        if user_key == -1:
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
        prog_len = length
        if length == -1:
            prog_len = 4

        progression = []
        chords_copy = deepcopy(self.chords)
        if omit_diminished:
            if self.mode == 'minor':
                chords_copy.pop(1)
            else:
                chords_copy.pop(len(chords_copy)-1)
        for i in range(prog_len):
            max_index = len(chords_copy)-1
            index = randint(0, max_index)
            if force_root and (i == 0):
                index = 0
            progression.append(chords_copy[index])
            if force_unique:
                chords_copy.pop(index)
        return progression

    def print_progression(self):
        print("Progression: ", end='')
        for i in range(len(self.prog)):
            determine_triad_identity(self.prog[i])
        print()

    def write_bassline(self, num_phrases=1, note_duration=-1, start_time=0):
        note_dur = note_duration
        if note_duration == -1:
            note_dur = 0.25

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
                                      time=current_time, duration=note_dur, volume=100)
                    total_duration += note_dur
                    current_time += note_dur

    def write_arpeggio_and_moving_chords(self, num_phrases=1, note_duration=-1, start_time=0, pattern=-1):
        note_dur = note_duration
        if note_duration == -1:
            selector = randint(1, 2)
            selector += selector
            note_dur = float(1/selector)

        pattern_index = pattern
        if pattern == -1:
            pattern_index = randint(0, len(PATTERNS)-1)
            self.arp_pattern = pattern_index

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
                for j in range(int(1/note_dur)):
                    # this code outputs all the notes of the arpeggio exactly once
                    for i in range(len(pattern)):
                        cur_index = pattern[i]
                        arp_pitch = chord[cur_index] - 12
                        mov_pitch = arp_pitch
                        if not i == 0:
                            mov_pitch = self.tamper(mov_pitch)

                        if not mov_pitch == 0:
                            self.midi.addNote(track=3, channel=3, pitch=mov_pitch,
                                              time=current_time, duration=note_dur, volume=80)
                        if arp_note_counter % 2 == 0:
                            self.midi.addNote(track=2, channel=2, pitch=arp_pitch,
                                              time=current_time, duration=(2*note_dur), volume=90)
                            self.midi.addNote(track=2, channel=2, pitch=arp_pitch+g,
                                              time=current_time, duration=(2 * note_dur), volume=90)
                        current_time += note_dur
                        arp_note_counter += 1

    @staticmethod
    def tamper(val):
        """
        This function uses some basic random logic to make somewhat interesting random melodies
        :param val: the pitch that is getting messed with
        :return: likely the same value, but sometimes an octave lower or higher
        """
        selector = randint(0, 16384)
        if selector % 3 == 0:
            val -= OCTAVE
        elif selector % 5 == 0:
            val += OCTAVE
        elif selector % 4 == 0:
            val += g
        elif selector % 2 == 0:
            val = 0
        return val

    def write_melody(self, num_phrases=1, start_time=0):
        note_lens = [0.25, 0.5, 0.5, 1.0]

        for j in range(num_phrases):
            for i in range(len(self.prog)):
                total_duration = 0.0
                cur_chord = self.prog[i]
                if determine_triad_identity(cur_chord)[1] == 'major':
                    pentatonic = [c, d, e, g, a]
                else:
                    pentatonic = [c, eb, f, g, bb]

                cur_note = self.prog[i][0]-OCTAVE
                while total_duration < 4:
                    pitch = cur_note
                    if total_duration == 0:
                        duration = 0.5
                    else:
                        modifier = pentatonic[randint(0, len(pentatonic)-1)]
                        duration = note_lens[randint(0, len(note_lens)-1)]
                        pitch += modifier
                    while duration + total_duration > 4:
                        duration -= 0.25
                    self.midi.addNote(track=4, channel=4, pitch=pitch,
                                      time=(start_time+total_duration+(4*i)),
                                      duration=duration, volume=120)
                    total_duration += duration

    def write_drums(self, start_time=0, drum_mode=-1, num_phrases=1):
        kick = 36
        snare1 = 40
        snare2 = 38
        clap = 39
        rim = 37
        hat1 = 36 + ab
        hat2 = 36 + gb

        for j in range(num_phrases):
            generation_mode = drum_mode
            if drum_mode == -1:
                generation_mode = randint(0, 1)

            for i in range(4):
                phrase_duration = 0
                while phrase_duration < 16:

                    if generation_mode == 0:
                        if phrase_duration % 1 == 0:
                            self.midi.addNote(track=5, channel=5, pitch=hat1,
                                              time=(start_time + float(phrase_duration / 4) + (4 * i)), duration=0.25,
                                              volume=100)
                        if phrase_duration % 2 == 0:
                            self.midi.addNote(track=5, channel=5, pitch=kick,
                                              time=(start_time + float(phrase_duration/4) + (4 * i)),
                                              duration=0.25, volume=100)
                        if phrase_duration % 4 == 0:
                            self.midi.addNote(track=5, channel=5, pitch=snare1,
                                              time=(start_time + float(phrase_duration/4) + (4 * i) + 0.5),
                                              duration=0.25, volume=100)

                    elif generation_mode == 1:
                        if phrase_duration % 1 == 0:
                            self.midi.addNote(track=5, channel=5, pitch=hat1,
                                              time=(start_time + float(phrase_duration / 4) + (4 * i)), duration=0.25,
                                              volume=100)
                        if phrase_duration % 2 == 0:
                            self.midi.addNote(track=5, channel=5, pitch=clap,
                                              time=(start_time + float(phrase_duration/4) + (4 * i)),
                                              duration=0.25, volume=100)
                            self.midi.addNote(track=5, channel=5, pitch=kick,
                                              time=(start_time + float(phrase_duration/4) + (4 * i)),
                                              duration=0.25, volume=100)

                    phrase_duration += 0.25
            return generation_mode

    def info(self):
        print()
        print("BEAT INFO:")
        print()
        print("Key Info")
        print("Key: ", end='')
        self.print_scale()
        # self.print_notes()
        # self.print_chords()
        self.print_progression()
        print()
        print("Beat Info")
        print("Tempo: " + str(self.tempo))
        print("Arpeggio Pattern: " + str(self.arp_pattern))
        print("Drum Generation Method: " + str(self.drum_mode))
        print("Length: " + str(4*self.num_phrases) + " measures")
        print()

    """
    below here are functions dedicated to the midi
    """

    @staticmethod
    def set_tempo(user_tempo=-1):
        tempo_min = 60
        tempo_max = 100
        tempo = user_tempo
        if user_tempo == -1:
            tempo = randint(tempo_min, tempo_max)
        return tempo

    def initialize_midi(self, num_tracks=len(INSTRUMENTS)):
        midi = MIDIFile(num_tracks)
        for i in range(num_tracks):
            midi.addTempo(track=i, time=0, tempo=self.tempo)
        return midi

    def select_instruments(self, random_instruments=True):
        if random_instruments:
            for i in range(len(INSTRUMENTS)):
                program = get_instrument_val(i)
                self.midi.addProgramChange(tracknum=i, channel=i, time=0, program=program)

    def write(self, filename='output.mid'):
        with open(filename, 'wb') as outf:
            self.midi.writeFile(outf)
        print("Wrote midi to file " + filename + " in current directory")

    def write_progression(self, chord_length=4, starting_beat=0, chord_spacing=4, num_phrases=1):
        for h in range(num_phrases):
            for i in range(len(self.prog)):
                current_chord = self.prog[i]
                current_time = starting_beat + (chord_spacing*i)
                for j in range(len(current_chord)):
                    pitch = current_chord[j]
                    self.midi.addNote(track=0, channel=0, pitch=(pitch+(12*self.octave)),
                                      time=current_time, duration=chord_length, volume=60)
