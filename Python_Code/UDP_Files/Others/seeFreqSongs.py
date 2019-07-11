import os, mutagen.mp3
from tkinter import filedialog


def choose_dir():
    path = filedialog.askopenfilenames()
    for aux in path:
        print(aux, "AUX")
        mp3 = mutagen.mp3.MP3(aux)
        print(mp3.info.sample_rate, "RATE")

choose_dir()