import pymysql
import operator
import random

## Numero en milisegundos (*1000), bang;
## 1512, bang;

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


def get_users_from_song(song):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT `FK_CEDULA_USUARIO` FROM `databeats` WHERE `FK_ID_CANCION` = %s"
            cursor.execute(sql, song)
            query = cursor.fetchall()
            return query

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
                if abs(song_annotations[0][data1] - song_annotations[1][data2]) < 0.3 and abs(
                        song_annotations[0][data1] - song_annotations[2][data3]) < 0.3:
                    dispersion = max(
                        [song_annotations[0][data1], song_annotations[1][data2], song_annotations[2][data3]]) - min(
                        [song_annotations[0][data1], song_annotations[1][data2], song_annotations[2][data3]])
                    if dispersion < 0.2:
                        process_beat = (song_annotations[0][data1]*shrp_1) + (song_annotations[1][data2]*shrp_2) + (song_annotations[2][data3] * shrp_3)
                        triad_list.append(process_beat)

    return triad_list


def final_delay_list(song_annotations, sharp_list):
    triad_list = []
    best_user = sharp_list.index(max(sharp_list))
    user_1 = 0
    user_2 = 0

    if best_user == 0:
        user_1 = 1
        user_2 = 2
    if best_user == 1:
        user_1 = 0
        user_2 = 2
    if best_user == 2:
        user_1 = 0
        user_2 = 1

    shrp_best = sharp_list[best_user] / (sharp_list[0] + sharp_list[1] + sharp_list[2])
    shrp_1 = sharp_list[user_1] / (sharp_list[0] + sharp_list[1] + sharp_list[2])
    shrp_2 = sharp_list[user_2] / (sharp_list[0] + sharp_list[1] + sharp_list[2])

    shrp_best_usr_1 = sharp_list[best_user] / (sharp_list[best_user] + sharp_list[user_1])
    shrp_best_usr_2 = sharp_list[best_user] / (sharp_list[best_user] + sharp_list[user_2])
    shrp_1_2 = sharp_list[user_1] / (sharp_list[best_user] + sharp_list[user_1])
    shrp_2_2 = sharp_list[user_2] / (sharp_list[best_user] + sharp_list[user_2])


    index_beat_list_user_1 = 0
    index_beat_list_user_2 = 0

    best_beats = song_annotations[best_user]
    usr_1_beats = song_annotations[user_1]
    usr_2_beats = song_annotations[user_2]

    start_usr_1 = 0
    start_usr_2 = 0
    for i in range(len(best_beats)):
            if abs(float(best_beats[i]) - float(usr_1_beats[0])) < 0.5:
                start_usr_1 = i
                break

    for i in range(len(best_beats)):
        if abs(float(best_beats[i]) - float(usr_2_beats[0])) < 0.5:
            start_usr_2 = i
            break

    start = max(start_usr_2, start_usr_1)

    for i in range(start, len(best_beats)):
        extra_index_user_1 = 0
        extra_index_user_2 = 0
        user_1_value = 0
        user_2_value = 0

        for y in range(0, 3):
            extra_index_user_1 = y
            if (index_beat_list_user_1+y) < len(song_annotations[user_1]):
                if abs(float(best_beats[i])-float(usr_1_beats[index_beat_list_user_1+y]))<0.5:
                    user_1_value = usr_1_beats[index_beat_list_user_1+y]
                    break

        for y in range(0, 3):
            extra_index_user_2 = y
            if (index_beat_list_user_2+y) < len(song_annotations[user_2]):
                if abs(float(best_beats[i])-float(usr_2_beats[index_beat_list_user_2+y]))<0.5:
                    user_2_value = usr_2_beats[index_beat_list_user_2+y]
                    break

        index_beat_list_user_1 = index_beat_list_user_1 + extra_index_user_1
        index_beat_list_user_2 = index_beat_list_user_2 + extra_index_user_2

        if (user_1_value != 0) and (user_2_value == 0):
            process_beat = (float(user_1_value) * float(shrp_1_2)) + (float(best_beats[i]) * float(shrp_best_usr_1))
            triad_list.append(process_beat)

        if (user_1_value == 0) and (user_2_value != 0):
            process_beat = (float(user_2_value) * float(shrp_2_2)) + (float(best_beats[i]) * float(shrp_best_usr_2))
            triad_list.append(process_beat)

        if (user_1_value != 0) and (user_2_value != 0):
            process_beat = (float(user_1_value) * float(shrp_1)) + (float(user_2_value) * float(shrp_2)) + (float(best_beats[i]) * float(shrp_best))
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

    #final_list = create_final_delay_list(list_delay, list_sharp)
    final_list = final_delay_list(list_delay, list_sharp)

    file = open("../Jupyter_Files/Data/Processed_Delay/3_Best.txt", "w")
    msg = ""
    for beat in final_list:
        msg += str(beat) + "\n"
    file.write(msg)
    file.close()
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

    #final_list = create_final_delay_list(list_delay, list_sharp)
    final_list = final_delay_list(list_delay, list_sharp)

    file = open("../Jupyter_Files/Data/Processed_Delay/3_Worst.txt", "w")
    msg = ""
    for beat in final_list:
        msg += str(beat) + "\n"
    file.write(msg)
    file.close()
    return final_list


def get_delay_hw(user_date):
    data = user_date.split('_')

    if user_date in delay_hw_ses.keys():
        return delay_hw_ses[user_date]
    else:
        aux_key = ""
        for key in delay_hw_ses.keys():
            value = key.find(data[0])
            if value != -1:
                aux_key = key

        return delay_hw_ses[aux_key]


def delay_process_5_random_songs():

    load_sharp_data()
    load_delay_hw()
    x = 0
    number_songs = 5
    list_songs = []
    actual_songs = get_songs_3_repetitions()

    while x < number_songs:
        song = actual_songs[random.randint(0, len(actual_songs))][0]
        dict_usrs = {}
        indx = 0
        num_usrs = 3
        aux_users = get_users_from_song(song)
        x += 1
        while indx < num_usrs:
            dict_usrs[aux_users[indx][0]] = 0
            indx += 1

        for usr in dict_usrs.keys():
            query = get_song_by_user(song, usr)
            date = query[1]
            key = "{0}_{1}/{2}/{3}".format(str(usr), str(getattr(date, 'day')),
                                           str(getattr(date, 'month')), str(getattr(date, 'year')))

            delay = get_delay_hw(key)
            dict_usrs[usr] = remove_delay_hw(delay, query[0])

        list_sharp = []
        list_delay = []
        for user in dict_usrs.keys():
            list_sharp.append(sharp_dict[str(user)])
            list_delay.append(dict_usrs[user])

        #final_list = create_final_delay_list(list_delay, list_sharp)
        final_list = final_delay_list(list_delay, list_sharp)

        file = open("../Jupyter_Files/Data/Processed_Songs/"+str(song)+".txt", "w")
        msg = ""
        for beat in final_list:
            msg += str(beat)+"\n"
        file.write(msg)
        file.close()
        print(final_list)


def real_beats():
    beats_list = []
    act_beat = 0
    msg = ""
    while act_beat < 30:
        beats_list.append(act_beat)
        act_beat += 0.7317
        msg += str(act_beat)+"\n"
    file = open("../Jupyter_Files/Data/Processed_Delay/real_beats.txt", "w")
    file.write(msg)
    file.close()


delay_process_3_best()
delay_process_3_worst()
delay_process_5_random_songs()
real_beats()
