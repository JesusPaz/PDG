import os
from tkinter import filedialog
import pymysql


def insert_db(song_name):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa", )

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `despacho_cancion`(`ID_CANCION`, `NOMBRE_CANCION`, `REPETICIONES`, `USUARIO_1`, `FECHA_1`, `USUARIO_2`, `FECHA_2`, `USUARIO_3`, `FECHA_3`) VALUES (%s,%s,0,0,0,0,0,0,0)"
            cursor.execute(sql, ("", song_name))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    finally:
        connection.close()


def choose_dir():
    path = filedialog.askopenfilenames()
    for aux in path:
        file = os.path.basename(aux)
        print(file)
        aux = file.split(".")
        insert_db(aux[0])

choose_dir()