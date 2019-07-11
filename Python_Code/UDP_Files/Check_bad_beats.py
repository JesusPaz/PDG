import pymysql


# a song is completed when has 3 repetitions in the database
def get_songs_complete():
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT `ID_CANCION` FROM `despacho_cancion` WHERE `REPETICIONES` = 3"
            cursor.execute(sql)
            query = cursor.fetchall()

            print(len(query))
            return query

    finally:
        connection.close()


# I want to check that all the data it's ok, and the database don't have bad information
def verification_real_repetitions():
    # ids_despacho = get_songs_complete()
    ids_databeats = {}
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:

        with connection.cursor() as cursor:

            sql = "SELECT `ID_CANCION` FROM `despacho_cancion`"
            cursor.execute(sql)
            all_id = cursor.fetchall()

            for x in all_id:
                # Create a new record
                sql = "SELECT `FK_ID_CANCION` FROM `databeats` WHERE `FK_ID_CANCION` = %s"
                cursor.execute(sql, x)
                query = cursor.fetchall()
                ids_databeats[x] = len(query)

            len(ids_databeats)
            return ids_databeats
    finally:
        connection.close()


# Search what are the real 3 repetitions in the table databeats
def find_3_real_repetitions():
    data = verification_real_repetitions()
    data_3_repetitions = {}

    for id in data:
        rep = data[id]
        if rep == 3:
            data_3_repetitions[id] = rep

    return data_3_repetitions


def print_all_data(id):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:

        with connection.cursor() as cursor:

            sql = "SELECT `FK_ID_CANCION`, `FK_CEDULA_USUARIO` FROM `databeats` WHERE `FK_ID_CANCION` = %s"
            cursor.execute(sql, id)
            all_id = cursor.fetchall()
            print("ID : ", id)
            for x in all_id:
                print(x[0], x[1])
    finally:
        connection.close()


# Search the ids that don't have 3 repetitions but in the table despacho_cancion has 3 repetitions
def find_bad_id_repetitions():
    ids_despacho = get_songs_complete()
    real_repetitions = verification_real_repetitions()

    print("List of the wrong repetitions in the table")
    for id in ids_despacho:
        if real_repetitions[id] < 3:
            print_all_data(id)


find_bad_id_repetitions()
