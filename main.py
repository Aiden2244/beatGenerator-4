from generator import generate, GUI
from tkinter import *
from tkinter import ttk

if not GUI:
    print("BEAT GENERATOR VERSION 1.0.0 | WRITTEN BY AIDEN MCCORMACK")

    while generate():
        pass

    print("Thank you for using the beat generator!")
    print()

else:
    class App:
        def __init__(self):
            self.root = Tk()
            self.root.title("Beat Generator")
            self.root.geometry("700x400")

            self.mainframe = ttk.Frame(self.root)
            self.mainframe.pack(fill='both', expand=True)

            self.text = ttk.Label(self.mainframe, text="Beat Generator", font=("Helvetica", 60))
            self.text.grid(row=1, column=1)

            self.subtitle = ttk.Label(self.mainframe, text="A program by Aiden McCormack", font=("Helvetica", 18))
            self.subtitle.grid(row=2, column=1)

            self.generate_button = ttk.Button(self.mainframe, text="GENERATE BEAT", command=generate)
            self.generate_button.grid(row=3, column=1)

            self.dummy1 = ttk.Label(self.mainframe, text="")
            self.dummy2 = ttk.Label(self.mainframe, text="")
            self.dummy1.grid(row=0, column=0, padx=70, pady=10)
            self.dummy2.grid(row=2, column=2, padx=60, pady=10)


            self.root.mainloop()


    if __name__ == "__main__":
        App()

