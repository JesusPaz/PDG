# Basado en: https://github.com/attreyabhatt/Python-Music-Player/blob/master/main.py
import os
from tkinter.filedialog import askdirectory
import pygame
from tkinter import *
from mutagen.mp3 import MP3
import threading
import time
from tkinter import ttk
import socket

root = Tk()
root.title("Client")
root.geometry("300x300")

lbl_welcome = Label(root, text="Ingresa tu cédula")
lbl_welcome.pack()

btn_send = Button(root, text="Enviar")
btn_send.place(x=180, y=25)

txt_cedula = Entry(root, width=20)
txt_cedula.place(x=50, y=30)

btn_play = Button(root, text="Reproducir")
btn_play.place(x=50, y=150)

btn_stop = Button(root, text="Volver a Intentar")
btn_stop.place(x=150, y=150)

lbl_length = Label(root, text="Duración Total : --:--")
lbl_length.place(x=90, y=80)

lbl_current = Label(root, text="Tiempo Actual : --:--")
lbl_current.place(x=90, y=100)

fm_feedback = Canvas(root, width=200, height=20, bg="white")
fm_feedback.place(x=50, y=200)


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def sum_beats(cad):
    arr = cad.split(",")
    suma = 0.0
    for x in arr:
        suma += float(x)

    return suma


def send_cedula(event):
    cedula = txt_cedula.get()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        user_id_msg = "start;"+cedula
        s.sendall(user_id_msg.encode("utf-8"))
        data = s.recv(1024)
        data = data.decode("utf-8")
        aux = data.split(";")
        if aux[0] == "song_id":
            if aux[1] == "NO_VALIDO":
                #mostrar mensage error
                print("NO_VALIDO")
            else:
                load_song(aux[1])
                print("cancion:"+aux[1])



def space_feedback(event):
    if event.char == ' ':
        fm_feedback.create_oval(10, 10, 20, 20, width=2, fill='blue')

        print("ONE", repr(event.char))
        time.sleep(1)
        fm_feedback.create_oval(10, 10, 40, 40, width=2, fill='blue')


def load_song(song_name):
    pygame.mixer.init()
    pygame.mixer.music.load("Audio\\"+song_name)
    show_length_song(song_name)
    return


def show_length_song(song_name):
    audio = MP3("Audio\\"+song_name)
    total_length = audio.info.length

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)

    timeformat = "{:02d}:{:02d}".format(mins, secs)

    lbl_length["text"] = "Duración Total : " + timeformat

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
                lbl_current['text'] = "Tiempo Actual : " + timeformat
                time.sleep(0.01)
                current_time += 0.01
        if current_time == t:
            end = False




def play_song(event):
    global stop
    pygame.mixer.music.play()
    stop = FALSE


def play_again(event):
    global stop
    pygame.mixer.music.stop()
    stop = TRUE


btn_send.bind("<Button-1>", send_cedula)
btn_play.bind("<Button-1>", play_song)
btn_stop.bind("<Button-1>", play_again)

root.bind("<Key>", space_feedback)



root.mainloop()