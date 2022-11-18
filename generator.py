from music import *
from beat import Beat


def generate():
    # Programmer Arguments
    rand_key = True
    rand_mode = True
    rand_tempo = True
    rand_arp = True

    force_unique = True
    force_root = True
    omit_diminished = True

    # default values that the user can overwrite
    key = c
    mode = 'major'
    octave = 0

    arp_pattern = 0
    arp_duration = 0.25

    # Starts ui sequence
    print("Writing new beat... ")
    first_input = input("Press 'e' to edit beat details, 'c' to cancel, or any key to randomly generate a beat! >> ")
    if first_input == 'c':
        print("Cancelled. No beat generated.")
        return
    elif first_input == 'e':
        print("You pressed e. This program will break now")
    else:
        print("generating...")
        print()
        __OUTPUT__ = Beat()
        print("done!")

    __OUTPUT__.info()
    __OUTPUT__.write()
