from generator import generate

print("BEAT GENERATOR VERSION 1.0.0 | WRITTEN BY AIDEN MCCORMACK")
done = False
while not done:
    print()
    generate()
    print()
    are_we_done_yet = input("Press 't' to terminate the program, or press any key to generate a new beat >> ")
    if are_we_done_yet == 't':
        done = True
        print()
        print("Thank you for using the beat generator!")
        print()
    print()

