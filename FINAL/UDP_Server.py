# Taken from: https://pythontic.com/modules/socket/udp-client-server-example
import socket
import pymysql
from random import randint

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 16384

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")


# SELECT DISTINCT `ID_CANCION` FROM `canciones`, `databeats` AS B1, `databeats` AS B2 WHERE (`ID_CANCION` = B1.`FK_ID_CANCION`) AND (`REPETICIONES`<4)
def save_database(query):
    db = pymysql.connect("127.0.0.1", "admin", "1539321441", "beatsalsa")

    cursor = db.cursor()

    cursor.execute(query)

    data = cursor.fetchone()

    print("Database version : {0}".format(data))

    db.close()
    return


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
            sql = "UPDATE `canciones` SET `REPETICIONES`=%s,`USUARIOS`=%s WHERE `ID_CANCION`=%s"
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


# Listen for incoming datagrams


while True:

    message, address = UDPServerSocket.recvfrom(bufferSize)

    clientMsg = "Message from Client:{}".format(message.decode())
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    text = message.decode()

    if text[:5] == "Ready":

        print("Ready to send the id songs")

        msgDiv = text.split(",")

        # Sending a Answer to client
        UDPServerSocket.sendto(str.encode(select_songs(msgDiv[1])), address)

    elif text[:4] == "Save":

        print("Saving the Beats into DB")

        aux = text.split("|")

        data = aux[1].split(";")

        id_cancion = data[0]
        id_usuario = data[1]
        beats = data[2]
        delay = data[3]

        insert_beat(id_cancion, id_usuario, beats, delay)
        msg = "Beats from song {0}, usr {1} saved ".format(id_cancion,id_usuario)
        # Sending a reply to client
        UDPServerSocket.sendto(str.encode(msg), address)
    else:
        print("-------------------------ERROR MSG----------------------------- ")
