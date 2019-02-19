"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
# Para formatear tabla canciones:
# UPDATE `canciones` SET `REPETICIONES`=0,`USUARIO_1`=0,`FECHA_1`="",`USUARIO_2`=0,`FECHA_2`="",`USUARIO_3`=0,`FECHA_3`=""

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


def sum_beats(cad):

    arr = cad.split(";")

    return 0


def update_usr_song(idSong, idUsr, repeticion, numUsr):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:
            # Create a new record
            if numUsr == 1:
                sql ="UPDATE `canciones` SET `REPETICIONES`=%s,`USUARIO_1`=%s,`FECHA_1`=CURRENT_TIMESTAMP WHERE `ID_CANCION`=%s"
            elif numUsr == 2:
                sql = "UPDATE `canciones` SET `REPETICIONES`=%s,`USUARIO_2`=%s,`FECHA_2`=CURRENT_TIMESTAMP WHERE `ID_CANCION`=%s"
            elif numUsr == 3:
                sql = "UPDATE `canciones` SET `REPETICIONES`=%s,`USUARIO_3`=%s,`FECHA_3`=CURRENT_TIMESTAMP WHERE `ID_CANCION`=%s"

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
            print(str(len(query)) + " tamaño Query <3")
            while end:

                x = randint(0, len(query) - 1)

                row = query[x]
                id = row[0]
                repetition = row[2]
                user_1 = row[3]
                user_2 = row[5]
                user_3 = row[7]

                if repetition == 0:

                    # se queda con esa canción y actualiza los datos
                    repetition += 1
                    update_usr_song(id, idUser, repetition, 1)

                    print("La canción se encontró con id {0} queda asignada para {1}".format(id, idUser))
                    end = False
                    return str(id)

                elif repetition > 0:

                    if user_1 != idUser and user_2 == 0 and user_3 == 0:
                        repetition += 1
                        update_usr_song(id, idUser, repetition, 2)
                        print ("La canción se encontró con id {0} queda asignada para {1}".format(id, idUser))
                        end = False
                        return str(id)
                    elif user_1 != idUser and user_2 != idUser and user_2 != 0 and user_3 == 0:
                        repetition += 1
                        update_usr_song(id, idUser, repetition, 3)
                        print ("La canción se encontró con id {0} queda asignada para {1}".format(id, idUser))
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
    sum_recv = data[4]

    if str(sum_recv) == str(sum_beats(beats)):
        insert_beat(id_cancion, id_usuario, beats, delay)
        msg = "Beats from song {0}, usr {1} saved ".format(id_cancion, id_usuario)
        print(msg)
    else:
        print("--------------------------ERROR: Check Sum Wrong -------------------------")
    return


def start_handler(unused_addr, args, msg):
    print("[{0}] ~ {1}".format(args[0], msg))

    idUser = int(msg)
    select_songs(idUser)

    #print(msg)

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
