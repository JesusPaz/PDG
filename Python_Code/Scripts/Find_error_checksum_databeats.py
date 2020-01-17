import pymysql
import io

all_id = {}


# I want to check that all the data it's ok, and the database don't have bad information
def verification_real_repetitions():
    global all_id
    ids_databeats = {}
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:

        with connection.cursor() as cursor:

            sql = "SELECT `ID_CANCION` FROM `despacho_cancion` WHERE `REPETICIONES` = 3"
            cursor.execute(sql)
            all_id = cursor.fetchall()

            for x in all_id:
                # Create a new record
                sql = "SELECT `FK_ID_CANCION`, `FK_CEDULA_USUARIO`, `BEATS` FROM `databeats` WHERE `FK_ID_CANCION` = %s"
                cursor.execute(sql, x)
                query = cursor.fetchall()
                for y in range(3):
                    ids_databeats[str(x[0]) + "_" + str(y)] = query[y]

            print(len(ids_databeats))
            return ids_databeats
    finally:
        connection.close()


def print_data():
    data = verification_real_repetitions()
    for x in data:
        print(str(x) + " - " + data[x][2])


def sum_beats(cad):
    if ((cad is not None) and (len(cad) is not 0)):
        arr = cad.split(" ")
        suma = 0.0
        for x in arr:
            if x is not "":
                suma += float(x)

        return suma
    else:
        return 0


def find_id_to_name(id):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:

        with connection.cursor() as cursor:

            sql = "SELECT `ID_CANCION` FROM `despacho_cancion` WHERE `NOMBRE_CANCION`=%s"
            cursor.execute(sql, id)
            return cursor.fetchone()[0]
            
    finally:
        connection.close()


def read_txt():
    beats = {}
    archivo = io.open("SesTotal.txt", 'r', encoding='utf8')
    # for linea in archivo.readlines():

    #     msg = linea
    #     cont = linea.find("save")

    #     if cont is not -1:
    #         aux = msg[cont:].split(";")
    #         print(aux[1].split(".")[0])
    #         new_id = find_id_to_name(aux[1].split(".")[0])
    #         aux[1] = new_id
    #         beats[str(new_id) + "_" + aux[2]] = aux[1:]

    linea = archivo.readline()
    while linea:

        msg = linea
        cont = linea.find("save")

        if cont is not -1:
            aux = msg[cont:].split(";")
            print(aux[1].split(".")[0])
            new_id = find_id_to_name(aux[1].split(".")[0])
            aux[1] = new_id
            beats[str(new_id) + "_" + aux[2]] = aux[1:]
        
        linea = archivo.readline()

    archivo.close()

    return beats


def update_beats(id_song, id_user, beats):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:

        with connection.cursor() as cursor:

            sql = "UPDATE `databeats` SET `BEATS`= %s WHERE `FK_ID_CANCION` = %s AND `FK_CEDULA_USUARIO` = %s"
            cursor.execute(sql, (beats, id_song, id_user))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

    finally:
        connection.close()


def check_if_checksum_error():
    real_data = read_txt()

    data = verification_real_repetitions()

    bad_beat = {}
    not_found = {}

    for x in all_id:

        if str(x[0]) + "_" + str(data[str(x[0]) + "_0"][1]) in real_data:

            sum0 = sum_beats(data[str(x[0]) + "_0"][2])

            if real_data[str(x[0]) + "_" + str(data[str(x[0]) + "_0"][1])][3] != str(sum0):
                bad_beat[str(x[0]) + "_" + str(data[str(x[0]) + "_0"][1])] = \
                    real_data[str(x[0]) + "_" + str(data[str(x[0]) + "_0"][1])][4]

                update_beats(str(x[0]), str(data[str(x[0]) + "_0"][1]),
                             real_data[str(x[0]) + "_" + str(data[str(x[0]) + "_0"][1])][4])

        else:
            not_found[str(x[0]) + "_" + str(data[str(x[0]) + "_0"][1])] = 0

        if str(x[0]) + "_" + str(data[str(x[0]) + "_1"][1]) in real_data:
            sum1 = sum_beats(data[str(x[0]) + "_1"][2])

            if real_data[str(x[0]) + "_" + str(data[str(x[0]) + "_1"][1])][3] != str(sum1):
                bad_beat[str(x[0]) + "_" + str(data[str(x[0]) + "_1"][1])] = \
                    real_data[str(x[0]) + "_" + str(data[str(x[0]) + "_0"][1])][4]

                update_beats(str(x[0]), str(data[str(x[0]) + "_1"][1]),
                             real_data[str(x[0]) + "_" + str(data[str(x[0]) + "_1"][1])][4])


        else:
            not_found[str(x[0]) + "_" + str(data[str(x[0]) + "_1"][1])] = 0

        if str(x[0]) + "_" + str(data[str(x[0]) + "_2"][1]) in real_data:
            sum2 = sum_beats(data[str(x[0]) + "_2"][2])

            if real_data[str(x[0]) + "_" + str(data[str(x[0]) + "_2"][1])][3] != str(sum2):
                bad_beat[str(x[0]) + "_" + str(data[str(x[0]) + "_2"][1])] = \
                    real_data[str(x[0]) + "_" + str(data[str(x[0]) + "_0"][1])][4]

                update_beats(str(x[0]), str(data[str(x[0]) + "_2"][1]),
                             real_data[str(x[0]) + "_" + str(data[str(x[0]) + "_2"][1])][4])

        else:
            not_found[str(x[0]) + "_" + str(data[str(x[0]) + "_2"][1])] = 0

    print("TAMAÑO TOTAL")
    print(len(bad_beat))

    print("TAMAÑO FALTANTES")
    print(len(not_found))

    for x in not_found:
        print(x)

check_if_checksum_error()
