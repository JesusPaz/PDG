import pymysql

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
                    ids_databeats[str(x) + "_" + str(y)] = query[y]

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


def check_if_checksum_error():
    data = verification_real_repetitions()

    for x in all_id:
        sum0 = sum_beats(data[str(x) + "_0"][2])
        sum1 = sum_beats(data[str(x) + "_1"][2])
        sum2 = sum_beats(data[str(x) + "_2"][2])

        print("Para el ID: " + str(x))
        print(sum0)
        print(sum1)
        print(sum2)


def read_txt():
    archivo = open("Ses1.txt", "r")
    for linea in archivo.readlines():
        print("----------------LINEA-----------------------")
        msg = linea
        cont = linea.find("save")

        if cont is not -1:
            print(msg[cont:])
        

    archivo.close()


read_txt()
