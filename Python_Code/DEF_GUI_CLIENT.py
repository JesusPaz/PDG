# Basado en: https://github.com/attreyabhatt/Python-Music-Player/blob/master/main.py
import os
from tkinter.filedialog import askdirectory
import pygame
from mutagen.mp3 import MP3
import threading
import time
from tkinter import ttk
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client
import numpy as np
import argparse
import random
from tkinter import *


class GUI(threading.Thread):
    def __init__(self):
        super().__init__(daemon=False, target=self.run)
        self.root = Tk()
        self.root.title("Client")
        self.root.geometry("300x300")

        self.lbl_welcome = Label(self.root, text="Ingresa tu cédula")
        self.lbl_welcome.pack()

        self.btn_send = Button(self.root, text="Enviar")
        self.btn_send.place(x=180, y=25)

        self.txt_cedula = Entry(self.root, width=20)
        self.txt_cedula.place(x=50, y=30)

        self.btn_play = Button(self.root, text="Reproducir")
        self.btn_play.place(x=50, y=150)

        self.btn_stop = Button(self.root, text="Volver a Intentar")
        self.btn_stop.place(x=150, y=150)

        self.lbl_length = Label(self.root, text="Duración Total : --:--")
        self.lbl_length.place(x=90, y=80)

        self.lbl_current = Label(self.root, text="Tiempo Actual : --:--")
        self.lbl_current.place(x=90, y=100)

        self.fm_feedback = Frame(self.root, width=200, height=20, bg="blue")
        self.fm_feedback.place(x=50, y=200)


        def send_cedula(event):
            cedula = self.txt_cedula.get()

            client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
            client.send_message("/start", cedula)
            client.recv(1024)

            return

        def play_song(event):
            global stop
            pygame.mixer.music.play()
            stop = FALSE

        def play_again(event):
            global stop
            pygame.mixer.music.stop()
            stop = TRUE

        def space_feedback(event):
            if event.char == ' ':
                self.fm_feedback.place_forget()

                print("ONE", repr(event.char))
                time.sleep(0.3)
                self.fm_feedback.place()


        self. btn_send.bind("<Button-1>", send_cedula)
        self.btn_play.bind("<Button-1>", play_song)
        self.btn_stop.bind("<Button-1>", play_again)

        self.root.bind("<Key>", space_feedback)

        self.root.mainloop()
        #self.root.destroy()

        def load_song(song_name):
            pygame.mixer.init()
            pygame.mixer.music.load("Audio\\"+song_name)
            show_length_song(song_name)
            return

        def run(self):
            self.root.mainloop()
            self.root.destroy()


        def show_length_song(song_name):
            audio = MP3("Audio\\"+song_name)
            total_length = audio.info.length

            mins, secs = divmod(total_length, 60)
            mins = round(mins)
            secs = round(secs)

            timeformat = "{:02d}:{:02d}".format(mins, secs)

            self.lbl_length["text"] = "Duración Total : " + timeformat

            t1 = threading.Thread(target=start_count, args=(total_length,))
            t1.start()

        def start_count(t):

            # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
            # Continue - Ignores all of the statements below it. We check if music is paused or not.
            global stop
            stop = FALSE
            current_time = 0

            end = True
            while(end):
                while current_time <= t and pygame.mixer.music.get_busy():
                    if stop:
                        current_time=0
                    else:
                        mins, secs = divmod(current_time, 60)
                        mins = round(mins)
                        secs = round(secs)
                        timeformat = '{:02d}:{:02d}'.format(mins, secs)
                        self.lbl_current['text'] = "Tiempo Actual : " + timeformat
                        time.sleep(1)
                        current_time += 1
                if current_time == t:
                    end = False


        def create_rnd_beats(n):
            sum = 0
            cad = ""
            for x in range(0, n-1):
                num = random.random()
                sum += num
                if(x<n-2):
                    cad += str(num)[:5]+","
                else:
                    cad += str(num)[:5]
            return cad, sum

        def sum_beats(cad):
            arr = cad.split(",")
            suma = 0.0
            for x in arr:
                suma += float(x)

            return suma

