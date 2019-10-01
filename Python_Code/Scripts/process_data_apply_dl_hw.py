import pymysql
import operator

# Constants
sharp_dict = {}
delay_hw_ses = {}


def load_sharp_data():
    global sharp_dict
    f = open("../Jupyter_Files/Data/sharp.txt", "r")
    for line in f:
        data = line.split(",")
        sharp_dict[data[0]] = float(data[1].split("\n")[0])
    f.close()
    aux_dict = sorted(sharp_dict.items(), key=operator.itemgetter(1))
    pre_sharp = {}
    for act in aux_dict:
        pre_sharp[act[0]] = act[1]
    sharp_dict = pre_sharp


def load_delay_hw():
    global delay_hw_ses
    f = open("../Jupyter_Files/Data/delay_hw_ses.txt", "r")
    for line in f:
        data = line.split(",")
        delay_hw_ses[data[0]] = float(data[1].split("\n")[0])
    f.close()


def get_last_delay_user(user):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT `BEATS_MSG`,`FECHA` FROM `delay` WHERE `CEDULA_USUARIO` = %s"
            cursor.execute(sql, user)
            query = cursor.fetchall()

            return query[len(query)-1]

    finally:
        connection.close()


def get_song_by_user(song, user):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT `BEATS`, `FECHA` FROM `databeats` WHERE `FK_ID_CANCION`=%s AND `FK_CEDULA_USUARIO`=%s"
            cursor.execute(sql, (song, user))
            query = cursor.fetchone()

            return query

    finally:
        connection.close()


def get_songs_3_repetitions():
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
            return query

    finally:
        connection.close()


def create_final_delay_list(song_annotations, sharp_list):
    triad_list = []
    minimum_list = min(len(song_annotations[0]), len(song_annotations[1]), len(song_annotations[2]))
    shrp_1 = sharp_list[0] / (sharp_list[0]+sharp_list[1]+sharp_list[2])
    shrp_2 = sharp_list[1] / (sharp_list[0]+sharp_list[1]+sharp_list[2])
    shrp_3 = sharp_list[2] / (sharp_list[0]+sharp_list[1]+sharp_list[2])
    for data1 in range(minimum_list):
        for data2 in range(minimum_list):
            for data3 in range(minimum_list):

                # find if all three annotations are closer by less than 500ms
                if abs(song_annotations[0][data1] - song_annotations[1][data2]) < 0.5 and abs(
                        song_annotations[0][data1] - song_annotations[2][data3]) < 0.5:
                    dispersion = max(
                        [song_annotations[0][data1], song_annotations[1][data2], song_annotations[2][data3]]) - min(
                        [song_annotations[0][data1], song_annotations[1][data2], song_annotations[2][data3]])
                    if dispersion < 0.2:
                        process_beat = (song_annotations[0][data1]*shrp_1) + (song_annotations[1][data2]*shrp_2) + (song_annotations[2][data3] * shrp_3)
                        triad_list.append(process_beat)

    return triad_list


def remove_delay_hw(delay, beats):

    delay = delay/1000
    data = beats.split(' ')
    final_list = []
    for beat in data:
        final_list.append(float(beat)-float(delay))

    return final_list


def delay_process_3_best():
    load_sharp_data()
    load_delay_hw()
    get_songs_3_repetitions()
    dict_usrs = {}
    indx = 0
    num_usrs = 3
    while indx < num_usrs:
        dict_usrs[list(sharp_dict.keys())[-indx]] = 0
        indx += 1

    for usr in dict_usrs.keys():
        query = get_last_delay_user(usr)
        date = query[1]
        key = "{0}_{1}/{2}/{3}".format(str(usr), str(getattr(date, 'day')),
                                        str(getattr(date, 'month')), str(getattr(date, 'year')))

        delay = delay_hw_ses[key]
        dict_usrs[usr] = remove_delay_hw(delay, query[0])

    list_sharp = []
    list_delay = []
    for user in dict_usrs.keys():
        list_sharp.append(sharp_dict[user])
        list_delay.append(dict_usrs[user])

    final_list = create_final_delay_list(list_delay, list_sharp)
    print(final_list)
    return final_list


def delay_process_3_worst():
    dict_usrs = {}
    indx = 0
    num_usrs = 3
    while indx < num_usrs:
        dict_usrs[list(sharp_dict.keys())[indx]] = 0
        indx += 1

    for usr in dict_usrs.keys():
        query = get_last_delay_user(usr)
        date = query[1]
        key = "{0}_{1}/{2}/{3}".format(str(usr), str(getattr(date, 'day')),
                                        str(getattr(date, 'month')), str(getattr(date, 'year')))

        delay = delay_hw_ses[key]
        dict_usrs[usr] = remove_delay_hw(delay, query[0])

    list_sharp = []
    list_delay = []
    for user in dict_usrs.keys():
        list_sharp.append(sharp_dict[user])
        list_delay.append(dict_usrs[user])

    final_list = create_final_delay_list(list_delay, list_sharp)
    print(final_list)
    return final_list


delay_process_3_best()
delay_process_3_worst()
