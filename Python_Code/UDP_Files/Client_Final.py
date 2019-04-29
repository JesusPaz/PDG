# Basado en: https://github.com/attreyabhatt/Python-Music-Player/blob/master/main.py
# Es necesario para que funciones importar librerias: pygame, mutagen


import pygame
import tkinter as tk
from mutagen.mp3 import MP3
import threading
import time
import socket
from tkinter import messagebox
from tkinter import font

root = tk.Tk()
root.title("Client")
w, h = root.maxsize()
#root.geometry("%dx%d" % (w, h))
#root.geometry("300x300")
root.attributes("-fullscreen", True)

lbl_welcome = tk.Label(root, text="Gracias por participar en el experimento de anotación \n de salsa. Por favor introduce tu cédula")

btn_send = tk.Button(root, text="Enviar")

txt_cedula = tk.Entry(root, width=20)

root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (width // 2)
y = (height // 2)

lbl_welcome.place(x=x-160, y=y-140)
btn_send.place(x=x+30, y=y-75)
txt_cedula.place(x=x-100, y=y-70)

btn_play = tk.Button(root, text="Reproducir")

btn_stop = tk.Button(root, text="Volver a Intentar")

btn_cont = tk.Button(root, text="Continuar")

btn_reg = tk.Button(root, text="Regresar")

btn_yes = tk.Button(root, text="Si")

btn_ok = tk.Button(root, text = "Ok")

btn_ok_retry = tk.Button(root, text="Ok")

lbl_hidden = tk.Label(root, text = "")

lbl_hidden.place(x=x-600,y=y-350)

lbl_name = tk.Label(root, text="Nombre de la cancion")

Helvfont = font.Font(size=15, weight="bold")


lbl_prog = tk.Label(root, text="1 / 10", font=Helvfont)

lbl_length = tk.Label(root, text="Duración Total : --:--")

lbl_current = tk.Label(root, text="Tiempo Actual : --:--")


lbl_length = tk.Label(root, text="Duración Total : --:--")

lbl_current = tk.Label(root, text="Tiempo Actual : --:--")


#fm_feedback = tk.Canvas(root, width=200, height=20, bg="white")
#fm_feedback.create_rectangle(200, 5, 5, 20, width=2, fill='red')


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

delay = True
delay_num = 0
cont_song = 1

# metodo para centrar ventana
# tomado de https://stackoverrun.com/es/q/754917
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))





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
        user_id_msg = "start;" + cedula
        s.sendall(user_id_msg.encode("utf-8"))
        data = s.recv(1024)
        data = data.decode("utf-8")
        aux = data.split(";")
        if aux[0] == "song_id":
            if aux[1] == "NO_VALIDO":
                # mostrar mensage error
                print("NO_VALIDO")

                messagebox.showerror(message="Este documento no se encuentra registrado", title="ERROR")
            else:
                nom_song = aux[1]
                lbl_name["text"] = nom_song

                if delay:
                    delay_player()
                    load_song("60-bpm-metronome.mp3")
                    print("delay")
                else:
                    load_song(nom_song)
                    print("cancion:" + nom_song)
                    draw_music_player(event)


def show_delay_msg():
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()
    btn_yes.place_forget()


    lbl_name.place(x=x - 140, y=y - 120)
    lbl_name["text"] = "Gracias por practicar. Ahora da click en 'continuar' \n para escuchar la primera canción. Da click en \n 'regresar' si deseas practicar la tarea una vez más."
    btn_cont.place(x=x - 100, y=y - 30)
    btn_reg.place(x=x + 20, y=y - 30)


#metodo para pintar el player del delay
def delay_player():

    # OCULTA ENTRADA DATOS
    txt_cedula.config(state='disabled')
    txt_cedula.place_forget()
    btn_send.config(state='disabled')
    btn_send.place_forget()
    lbl_welcome.place_forget()
    btn_cont.place_forget()
    btn_reg.place_forget()
    btn_yes.place_forget()

    # HACE VISIBLE LA REPRODUCCION DE LA CANCION

    lbl_name.place(x=x - 140, y=y - 120)
    lbl_name["text"] = "Durante el experimento te pediremos que escuches \n canciones de salsa y que marques el pulso de la \n canción (en negras) usando la barra espaciadora \n del teclado. Practica la tarea del experimento \n escuchando un fragmento de salsa:"
    lbl_length.place(x=x - 60, y=y)
    lbl_current.place(x=x - 60, y=y + 20)
    btn_play.place(x=x - 100, y=y + 60)
    btn_stop.place(x=x, y=y + 60)
    #fm_feedback.place(x=x - 110, y=y + 110)


def draw_music_player(event):
    # OCULTA ENTRADA DATOS
    txt_cedula.config(state='disabled')
    txt_cedula.place_forget()
    btn_send.config(state='disabled')
    btn_send.place_forget()
    lbl_welcome.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()
    btn_yes.place_forget()
    btn_ok_retry.place_forget()
    # HACE VISIBLE LA REPRODUCCION DE LA CANCION

    lbl_name.place(x=x - 130, y=y - 110)
    lbl_name["text"] = "Escucha con atención la canción y marca el \n puso (en negras) usando la barra espaciadora \n del teclado. Si por alguna razón, deseas repetir \n la canción haz click en 'volver a intentar'"
    lbl_length.place(x=x - 60, y=y)
    lbl_current.place(x=x - 60, y=y + 20)
    btn_play.place(x=x - 100, y=y + 60)
    btn_stop.place(x=x, y=y + 60)
    lbl_prog.place(x=x + 450, y=y + 300)
    lbl_prog["text"] = str(cont_song) + " / 10"
    #fm_feedback.place(x=x - 110, y=y + 110)

def draw_data_entry():
    # OCULTA EL REPRODUCTOR
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()
    btn_yes.place_forget()
    lbl_prog.place_forget()
    btn_ok.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()
   # fm_feedback.place_forget()

    # HACE VISIBLE LA ENTRADA DE DATOS
    txt_cedula.config(state='normal')
    btn_send.config(state='normal')
    lbl_welcome.place(x=x-160, y=y-140)
    btn_send.place(x=x + 30, y=y - 75)
    txt_cedula.place(x=x - 100, y=y - 70)

def show_next_song():
    # OCULTA EL REPRODUCTOR
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()
    # fm_feedback.place_forget()

    lbl_name.place(x=x - 140, y=y - 75)
    lbl_name["text"] = "Gracias. ¿Estás listo para escuchar la siguiente canción?"
    btn_yes.place(x=x , y=y - 40)
    lbl_prog.place(x=x + 450, y=y + 300)
    lbl_prog["text"] = str(cont_song) + " / 10"
    return

def space_feedback(event):
    global space_boolean
    space_boolean = False
    pygame.mixer.init()
    if pygame.mixer.music.get_busy():
        if event.char == ' ':
            print("ONE", current_time)
            beats.append(current_time)
            # Feedback visual
            space_boolean = True
            space_time = 0
           # fm_feedback.place(x=x - 110, y=y + 110)


def load_song(song_name):
    pygame.mixer.music.load("Audio\\" + song_name)
    show_length_song(song_name)
    return


def show_length_song(song_name):
    audio = MP3("Audio\\" + song_name)
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
    global delay
    stop = False
    global current_time
    current_time = 0
    global beats
    beats = []
    end = True
    global space_time
    space_time = 0
    global msg_send
    global cont_song

    while end:
        while current_time <= t and pygame.mixer.music.get_busy():
            if stop:
                current_time = 0
                space_time = 0
                beats = []
            else:
                mins, secs = divmod(current_time, 59)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                lbl_current['text'] = "Tiempo Actual : " + timeformat

                time.sleep(0.01)
                if space_time > 0.1 and space_boolean:
                    #fm_feedback.place_forget()
                    space_time = 0
                space_time += 0.01
                current_time += 0.01
            # >= t-260:
            if ((delay == False) & (current_time >= t)) | ((delay == True) & (current_time >= 20)):
                beats_msg = ""
                cont = 0
                for item in beats:
                    if cont < len(beats) - 1:
                        beats_msg += str(item) + " "
                        cont += 1
                    else:
                        beats_msg += str(item)

                if delay:
                    pygame.mixer.music.stop()
                    msg_send = "delay;" + str(id_user) + ";" + beats_msg + ";" + str(get_delay(beats_msg))
                    print(msg_send)

                    show_delay_msg()

                    end = False

                else:
                    beats_ok = beats_validation(beats)
                    sum = sum_beats(beats_msg)
                    pygame.mixer.music.stop()
                    msg_send = "save;" + nom_song + ";" + str(id_user) + ";" + str(delay_num) + ";" + str(sum) + ";" + beats_msg
                    print(msg_send)
                    if beats_ok:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((HOST, PORT))
                            s.sendall(msg_send.encode("utf-8"))

                        if cont_song <2:
                            show_next_song()
                            cont_song+=1
                        else:
                            show_end_message()
                        end = False
                    else:
                        show_msg_bad_bpm()


def show_end_message():
    # OCULTA EL REPRODUCTOR
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()

    lbl_name["text"] = "Muchas gracias por participar debes tomar un descanso \n de 30 minutos para continuar con la actividad."
    lbl_name.place(x=x - 140, y=y - 75)
    btn_ok.place(x=x , y=y - 20)

def restart(event):
    global cont_song
    global delay
    draw_data_entry()
    cont_song = 1
    delay = True

def show_msg_bad_bpm():
    global nom_song
    # OCULTA EL REPRODUCTOR
    btn_play.place_forget()
    btn_stop.place_forget()
    lbl_name.place_forget()
    lbl_length.place_forget()
    lbl_current.place_forget()

    btn_cont.place_forget()
    btn_reg.place_forget()

    lbl_name["text"] = "Los datos no tienen la calidad necesaria, por \n favor escucha nuevamente la canción."
    lbl_name.place(x=x - 90, y=y - 75)

    btn_ok_retry.place(x=x,y=y-20)

    load_song(nom_song)


def beats_validation(beats):

    cont_minute_1 = 0
    cont_minute_2 = 0
    cont_minute_3 = 0
    is_ok = False

    for x in beats:
        if x <= 60:
            cont_minute_1 += 1
        if x > 60 and x <= 120:
            cont_minute_2 += 1
        if x > 120 and x <= 180:
            cont_minute_3 += 1

    print("Minuto 1 : "+ str(cont_minute_1))
    print("Minuto 2 : " + str(cont_minute_2))
    print("Minuto 3 : " + str(cont_minute_3))

    if (cont_minute_1 >= 60) and (cont_minute_1 <= 140):
        if (cont_minute_2 >= 60) and (cont_minute_2 <= 140):
            is_ok = True
            if (cont_minute_3 >= 60) and (cont_minute_3 <= 140):
                print("ook 3 minutos")

    print(is_ok)
    return is_ok


def continue_delay(event):
    global delay
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(msg_send.encode("utf-8"))
    delay = False

    lbl_name["text"] = nom_song
    load_song(nom_song)
    print("cancion:" + nom_song)
    draw_music_player(event)

    return

def repeat_delay(event):
    global delay
    delay_player()
    load_song("60-bpm-metronome.mp3")
    print("delay")
    delay = True
    return


def get_delay(beats_delay):
    return 0

def play_song(event):
    global stop
    pygame.mixer.music.play()
    stop = False


def play_again(event):
    global stop
    pygame.mixer.music.stop()
    stop = True


btn_send.bind("<Button-1>", send_cedula)
btn_play.bind("<Button-1>", play_song)
btn_stop.bind("<Button-1>", play_again)
btn_cont.bind("<Button-1>", continue_delay)
btn_reg.bind("<Button-1>", repeat_delay)
btn_yes.bind("<Button-1>", send_cedula)
lbl_hidden.bind("<Button-1>", restart)
btn_ok.bind("<Button-1>", restart)
btn_ok_retry.bind("<Button-1>",draw_music_player)

root.bind("<Key>", space_feedback)

root.mainloop()
