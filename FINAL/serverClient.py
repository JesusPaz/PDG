"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import socket
from random import randint

from pythonosc import dispatcher
from pythonosc import osc_server

import pymysql



def insert_beat(id_cancion, id_usuario, beats, delay):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `databeats` (`FK_ID_CANCION`, `FK_CEDULA_USUARIO`, `BEATS`, `DELAY`, `FECHA`) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
            cursor.execute(sql, (id_cancion, id_usuario, beats, delay))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        connection.close()


def update_usr_song(idSong, idUsr, repeticion):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "UPDATE `canciones` SET `REPETICIONES`=%s,`USUARIO_1`=%s WHERE `ID_CANCION`=%s"
            cursor.execute(sql, (repeticion, idUsr, idSong))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        connection.close()


def select_songs(idUser):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:
            end = True

            # Create a new record
            sql = "SELECT * FROM `canciones` WHERE `REPETICIONES`<3"
            cursor.execute(sql)
            query = cursor.fetchall()
            print(str(len(query)) + "tamaño cons")
            while end:

                x = randint(0, len(query) - 1)

                row = query[x]
                id = row[0]
                repetition = row[2]
                users = row[3].split(",")

                if repetition == 0:

                    # se queda con esa canción y actualiza los datos
                    repetition += 1
                    update_usr_song(id, idUser, repetition)

                    print("La cancion se encontro con id {0} queda asignada para {1}".format(id, idUser))
                    end = False
                    return str(id)

                elif repetition == 1:

                    if users[0] != idUser:
                        repetition += 1
                        aux = users[0] + "," + idUser
                        update_usr_song(id, aux, repetition)
                        print ("La cancion se encontro con id {0} queda asignada para {1}".format(id, idUser))
                        end = False
                        return str(id)
                    else:
                        print("Descartada cancion id {0}".format(id))

                elif repetition == 2:

                    if (users[0] != idUser) and (users[1] != idUser):
                        repetition += 1
                        aux = users[0] + "," + users[1] + "," + idUser
                        update_usr_song(id, aux, repetition)
                        print ("La cancion se encontro con id {0} queda asignada para {1}".format(id, idUser))
                        end = False
                        return str(id)
                    else:
                        print("Descartada cancion id {0}".format(id))


    finally:
        connection.close()






# Al parametro save tiene que entrar el idCancion;idUsuario;Beats;Delay
# Donde los beats deben ir separados por comas
# Uun ejemplo 1;2;0.332,5.336,7.5552;0.5


def save_handler(unused_addr, args, save):
    print("[{0}] ~ {1}".format(args[0], save))

    data = save.split(";")

    id_cancion = data[0]
    id_usuario = data[1]
    beats = data[2]
    delay = data[3]

    insert_beat(id_cancion, id_usuario, beats, delay)
    msg = "Beats from song {0}, usr {1} saved ".format(id_cancion, id_usuario)
    print(msg)

    return


def start_handler(unused_addr, args, msg):
    print("[{0}] ~ {1}".format(args[0], msg))

    select_songs(msg)

    print(msg)

    # Send song id to client (Pure Data)

   # client = udp_client.SimpleUDPClient("127.0.0.1", 20002)
    #client.send_message("/songid", msg_from_server[0])

    return


if __name__ == "__main__":

    dispatcher = dispatcher.Dispatcher()

    dispatcher.map("/save", save_handler, "Save ")
    dispatcher.map("/start", start_handler, "Ready")

    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 5005), dispatcher)
    print("ServerOSC in Client Ready on {}".format(server.server_address))
    server.serve_forever()
