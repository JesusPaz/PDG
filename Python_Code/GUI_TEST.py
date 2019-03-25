import tkinter as tk
from tkinter import ttk
from threading import Thread
from urllib.request import urlretrieve, urlcleanup
import pygame
from pygame.locals import *
import os


class Client(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Cliente")

        main_window.resizable(0,0)



        self.lbl = ttk.Label(self, text="Hello")
        self.lbl.place(x=30, y=10)

        self.txt =ttk.Entry(self, width=20)
        self.txt.place(x=50, y=30)


        self.btn_send = ttk.Button(
            self, text="Enviar", command=self.send_cedula())
        self.btn_send.place(x=220, y=25)


        self.btn_play = ttk.Button(
            self, text="Reproducir", command=self.play_song())
        self.btn_play.place(x=90, y=200)


        self.btn_again = ttk.Button(
            self, text="Volver a Intentar", command=self.play_again())
        self.btn_again.place(x=200, y=200)


        self.song_name = ttk.Label(self, text="Nombre Cancion")
        self.song_name.place(x=100, y=100)

        self.progressbar = ttk.Progressbar(self)
        self.progressbar.place(x=50, y=150, width=300)



        self.place(width=400, height=500)
        main_window.geometry("400x500")




    def send_cedula(self):
        self.lbl.configure(text="Button was clicked !!")


    def play_again(self):
        return


    def play_song(self):
        pygame.init()
        pygame.mixer.music.load('.\\OneDrive\\Escritorio\\PDG\\Python_Code\\Audio\\a-donde-iras-sin-mi-puerto-rican-power.mp3')
        #pygame.mixer.music.load('Audio\\a-donde-iras-sin-mi-puerto-rican-power.mp3')

        pygame.mixer.music.play(0)


main_window = tk.Tk()
cli = Client(main_window)
cli.mainloop()