# Basado en : https://github.com/realpython/materials/blob/master/python-sockets-tutorial/echo-server.py
# UPDATE `despacho_cancion` SET `REPETICIONES`=0,`USUARIO_1`=0,`FECHA_1`="",`USUARIO_2`=0,`FECHA_2`="",`USUARIO_3`=0,`FECHA_3`=""

import argparse
import math
import socket
from random import randint
from datetime import datetime, date, time, timedelta
import pymysql


HOST = "192.168.114.38"  # Standard loopback interface address (localhost)
#HOST = "127.0.0.1"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


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
    if ((cad is not None) and (len(cad) is not 0)):
        arr = cad.split(" ")
        suma = 0.0
        for x in arr:
            suma += float(x)

        return suma
    else:
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
                sql = "UPDATE `despacho_cancion` SET `REPETICIONES`=%s,`USUARIO_1`=%s,`FECHA_1`=CURRENT_TIMESTAMP WHERE `ID_CANCION`=%s"
            elif numUsr == 2:
                sql = "UPDATE `despacho_cancion` SET `REPETICIONES`=%s,`USUARIO_2`=%s,`FECHA_2`=CURRENT_TIMESTAMP WHERE `ID_CANCION`=%s"
            elif numUsr == 3:
                sql = "UPDATE `despacho_cancion` SET `REPETICIONES`=%s,`USUARIO_3`=%s,`FECHA_3`=CURRENT_TIMESTAMP WHERE `ID_CANCION`=%s"

            cursor.execute(sql, (repeticion, idUsr, idSong))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        connection.close()


def validate_user(idUser):
    # hacer llamado a la base de datos para verificar que el cliente existe
    # luego agregar a la lista de fechas en la bd

    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:

            sql1 = "SELECT `FECHAS_VALIDACION` FROM `usuarios` WHERE `CEDULA_USUARIO`=%s"
            cursor.execute(sql1, idUser)
            query = cursor.fetchone()
            ahora = datetime.now().utcnow()
            act_date = str(ahora.year)+"-"+str(ahora.month)+"-"+str(ahora.day)+" "+str(ahora.hour)+":"+str(ahora.minute)+":"+str(ahora.second)
            data = ""
            if query[0] == "":
               # print("no date")
                data = act_date
            else:

                for i in query:
                    data += i + ","
               # print("tiene")
                data += act_date

            #print("Las fechas de validacion son:")
           # print(data)

            # Create a new record
            sql2 = "UPDATE `usuarios` SET `FECHAS_VALIDACION`=%s WHERE `CEDULA_USUARIO`= %s"
            cursor.execute(sql2, (data, idUser))
            connection.commit()
        return True
    finally:
        connection.close()


# falta validar usuario
def select_songs(idUser):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:

            end = True

            # Create a new record
            sql = "SELECT * FROM `despacho_cancion` WHERE `REPETICIONES`<3"
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


def get_idSong(songName):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:

            sql = "SELECT `ID_CANCION` FROM `despacho_cancion` WHERE `NOMBRE_CANCION`=%s"
            cursor.execute(sql, songName)
            query = cursor.fetchone()

            print(query[0])
            return query[0]
    finally:
        connection.close()


# Al parametro save tiene que entrar el idCancion;idUsuario;Beats;Delay
# Donde los beats deben ir separados por comas
# Uun ejemplo 1;2;0.332,5.336,7.5552;0.5
def save_handler(save):
    data = save.split(";")
    #quita .mp3
    aux = data[1].split(".")
    id_cancion = get_idSong(aux[0])
    id_usuario = data[2]
    beats = data[5]
    delay = data[3]
    sum_recv = data[4]
    print(sum_recv)
    print(sum_beats(beats))
    if str(sum_recv) == str(sum_beats(beats)):
        insert_beat(id_cancion, id_usuario, beats, delay)
        msg = "Beats from song {0}, usr {1} saved ".format(id_cancion, id_usuario)
        print(msg)
    else:
        print("--------------------------ERROR: Check Sum Wrong -------------------------")
        insert_beat(id_cancion, id_usuario, beats, delay)
        msg = "Beats from song {0}, usr {1} saved ".format(id_cancion, id_usuario)
        print(msg)
    return

#Este metodo mira si el usuario existe en la base de datos
def user_exists(idUser):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:

            sql = "SELECT `CEDULA_USUARIO` FROM `usuarios`"
            cursor.execute(sql)
            query = cursor.fetchall()

            exists = False
            for x in query:
                if x[0] == idUser:
                    exists = True
            return exists
    finally:
        connection.close()


def get_song_name(idSong):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:

            sql = "SELECT `NOMBRE_CANCION` FROM `despacho_cancion` WHERE `ID_CANCION`= %s"
            cursor.execute(sql, idSong)
            query = cursor.fetchone()

            print(query[0])
            return query[0]
    finally:
        connection.close()

def insert_delay(id_usuario, beats, delay):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )


    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `delay`(`CEDULA_USUARIO`, `BEATS_MSG`, `DELAY_VALUE`, `FECHA`) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
            cursor.execute(sql, (id_usuario, beats, delay))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # your changes.
        connection.commit()

    finally:
        connection.close()

def delay_handler(msg):
    data = msg.split(";")
    idUser= data[1]
    beats = data[2]
    delay = data[3]

    insert_delay(idUser, beats, delay)


def start_handler(msg):
#    print("[{0}] ~ {1}".format(args[0], msg))

    #Falta metodo para ver si existe en la base de datos, depndiendo de eso puede seguir o no
   # client = udp_client.SimpleUDPClient("127.0.0.1", 5006)

    idUser = int(msg)
    if user_exists(idUser):
        validate_user(idUser)
        song_id = select_songs(idUser)
        print("Usuario Valido")
        # Send song id to client (Pure Data)
       # client.send_message("/songid", get_song_name(song_id)+".mp3")
        #client.send_message("/validation", 1)
        return "song_id;"+get_song_name(song_id)+".mp3"
    else:
        return "song_id;"+"NO_VALIDO"



try:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print("Connected by", addr)
                while True:
                    data = conn.recv(65507)
                    if not data:
                        break
                    else:
                        data = data.decode("utf-8")
                        print(data)
                        aux = data.split(";")
                        if aux[0] == "start":
                            print("Rcv start", aux[0])
                            conn.sendall(start_handler(aux[1]).encode("utf-8"))
                        elif aux[0] == "save":
                            print("Rcv save", aux[0])
                            save_handler(data)

                        elif aux[0] == "delay":
                            print("Rcv delay", aux[0])
                            delay_handler(data)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
