# Basado en: https://github.com/attreyabhatt/Python-Music-Player/blob/master/main.py
# Es necesario para que funciones importar librerias: pygame, mutagen
import pygame
from tkinter import *
from mutagen.mp3 import MP3
import threading
import time
import socket
from tkinter import messagebox

root = Tk()
root.title("Client")
root.geometry("300x300")

lbl_welcome = Label(root, text="Ingresa tu cédula")

btn_send = Button(root, text="Enviar")

txt_cedula = Entry(root, width=20)

lbl_welcome.pack()
btn_send.place(x=180, y=25)
txt_cedula.place(x=50, y=30)

btn_play = Button(root, text="Reproducir")

btn_stop = Button(root, text="Volver a Intentar")

lbl_name = Label(root, text="Nombre de la cancion")


lbl_length = Label(root, text="Duración Total : --:--")

lbl_current = Label(root, text="Tiempo Actual : --:--")

fm_feedback = Canvas(root, width=200, height=20, bg="white")
fm_feedback.create_rectangle(200, 5, 5, 20, width=2, fill='red')
fm_feedback.place(x=50, y=200)

lbl_aux = Label(root,text="HOLA")
lbl_aux.place(x=20, y=250)

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

#metodo para centrar ventana
#tomado de https://stackoverrun.com/es/q/754917
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


center(root)



def sum_beats(cad):
    arr = cad.split(" ")
    suma = 0.0
    for x in arr:
        suma += float(x)

    return suma


def send_cedula(event):
    global id_user
    cedula = txt_cedula.get()
    id_user = cedula
    global nom_song
    nom_song = "Nombre de la canción"

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

                messagebox.showerror(message="Este documento no se encuentra registrado", title="ERROR")
            else:
                nom_song = aux[1]
                lbl_name["text"] = nom_song
                load_song(aux[1])
                print("cancion:"+aux[1])
                draw_music_player()


def draw_music_player():
    # OCULTA ENTRADA DATOS
    txt_cedula.config(state='disabled')
    txt_cedula.place_forget()
    btn_send.config(state='disabled')
    btn_send.place_forget()
    lbl_welcome.pack_forget()

    # HACE VISIBLE LA REPRODUCCION DE LA CANCION

    btn_play.place(x=50, y=150)
    btn_stop.place(x=150, y=150)
    lbl_name.place(x=50, y=50)
    lbl_length.place(x=90, y=80)
    lbl_current.place(x=90, y=100)
    fm_feedback.place(x=50, y=200)


def draw_data_entry():

    #OCULTA EL REPRODUCTOR
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()
    fm_feedback.place_forget()

    #HACE VISIBLE LA ENTRADA DE DATOS
    txt_cedula.config(state='normal')
    btn_send.config(state='normal')
    lbl_welcome.pack()
    btn_send.place(x=180, y=25)
    txt_cedula.place(x=50, y=30)


def space_feedback(event):
    pygame.mixer.init()
    if pygame.mixer.music.get_busy():
        if event.char == ' ':
            print("ONE", current_time)
            beats.append(current_time)
            #Feedback visual
            #lbl_aux.place_forget()
            #time.sleep(0.3)

            lbl_aux.place(x=20, y=250)


def load_song(song_name):

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
    global current_time
    current_time = 0
    global beats
    beats = []
    end = True
    while(end):
        while current_time <= t and pygame.mixer.music.get_busy():
            if stop:
                current_time = 0
                beats = []
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                lbl_current['text'] = "Tiempo Actual : " + timeformat

                time.sleep(0.01)
                lbl_aux.place_forget()
                current_time += 0.01
            #>= t-260:
            if current_time >= 20:
                beats_msg = ""
                cont = 0
                for item in beats:
                    if cont < len(beats)-1:
                        beats_msg += str(item) + " "
                        cont += 1
                    else:
                        beats_msg += str(item)
                delay = 0
                sum = sum_beats(beats_msg)
                pygame.mixer.music.stop()
                msg_send = "save;"+nom_song+";"+str(id_user)+";"+str(delay)+";"+str(sum)+";"+beats_msg
                print(msg_send)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(msg_send.encode("utf-8"))

                if messagebox.askyesno(message="¿Desea escuchar otra canción?", title="Información"):
                    send_cedula(event="")
                else:
                    draw_data_entry()
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