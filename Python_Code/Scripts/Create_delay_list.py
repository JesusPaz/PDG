import pymysql
import librosa

# The method is used to get the delay array whith the parameters called id song and id user.
def get_delay_from_song(id_song, id_user):
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `FECHA`, `CEDULA_USUARIO`, `BEATS_MSG` FROM `delay` WHERE `CEDULA_USUARIO`= %s"
            cursor.execute(sql, id_user)
            query = cursor.fetchall()


            return query

    finally:
        connection.close()


def get_all_delay():
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `FECHA`, `CEDULA_USUARIO`, `BEATS_MSG` FROM `delay`"
            cursor.execute(sql)
            query = cursor.fetchall()


            return query

    finally:
        connection.close()


# The method is used to get all the id songs and id users to get the delay of all the song
def process_all_delays():
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")
    delay_dict = {}
    try:
        with connection.cursor() as cursor:
            # 3 is the max number of repetitions
            sql = "SELECT `ID_CANCION` FROM `despacho_cancion` WHERE `REPETICIONES`=3"
            cursor.execute(sql)
            all_id_songs = cursor.fetchall()

            for song in all_id_songs:
                sql = "SELECT `FK_CEDULA_USUARIO` FROM `databeats` WHERE `FK_ID_CANCION`= %s"
                cursor.execute(sql, song)
                id_users = cursor.fetchall()

                for user in id_users:
                    sql = "SELECT `FECHA` FROM `databeats` WHERE `FK_ID_CANCION`= %s AND `FK_CEDULA_USUARIO` = %s"
                    cursor.execute(sql, (song, user))
                    date_song = cursor.fetchone()[0]
                    delay = get_delay_from_song(song, user)
                    for item in delay:

                        date_delay = item[0]

                        if getattr(date_delay, 'year') == getattr(date_song, 'year') and getattr(date_delay, 'day') == getattr(date_song, 'day') and getattr(date_delay, 'month') == getattr(date_song, 'month'):
                            delay_dict[str(getattr(date_delay, 'year'))+"/"+str(getattr(date_delay, 'month'))+"/"+str(getattr(date_delay, 'day')) + "_" + str(user[0])] = delay


            #print(len(delay_dict))
            return delay_dict
    finally:
        connection.close()

# extract all delay from data base and create a dict with the key: date_user and the value: date, user, beats
def return_all_delay():

    query = get_all_delay()
    dict_beats = {}
    x = 0
    for item in query:

        date = item[0]
        key = str(getattr(date, 'year'))+"/"+str(getattr(date, 'month'))+"/"+str(getattr(date, 'day')) + "_" + str(item[1])
        dict_beats[x] = item
        x+=1

    return dict_beats

def find_value_total_delay():

    delay_list = return_all_delay()
    # print(delay_list)
    value_delay = {}
    # Delay using librosa library
    x, sr = librosa.load('audio/salsa_loop_82bpm.mp3')
    tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=82, units='time')
    # print(beat_times)
    beat_real_times = find_beat_time_from_bpm(82, 30)
    # print("----------------------------")
    # print(beat_real_times)
    beat_times = beat_real_times
    for item in delay_list:
        # print(item)
        delta_list = []
        delay_beats = delay_list[item][2].split(" ")
        index_beat_list = 0

        for i in range(0, len(delay_beats)):
            extra_index=0
            for y in range(0,3):
                extra_index = y
                if (index_beat_list+y) < len(beat_times):

                    if abs(float(delay_beats[i])-float(beat_times[index_beat_list+y]))<0.35:
                        #print(abs(float(delay_beats[i])-float(beat_times[index_beat_list+y])))
                        delta_list.append(abs(round(float(delay_beats[i])-float(beat_times[index_beat_list+y]), 2)))
                        break

            index_beat_list = index_beat_list + extra_index
        value_delay[item] = delta_list
        #print("FIN cancion")

    return value_delay


def find_beat_time_from_bpm(bpm, length_song):

    beat_list = []
    delta = 60/bpm
    end = True
    actual_beat = 0
    # comment the line bellow if beats do not start in zero
    beat_list.append(actual_beat)

    while(end):
        actual_beat = actual_beat + delta
        beat_list.append(actual_beat)

        if (actual_beat +delta) > length_song:
            end = False

    return beat_list

# Process all delays deltas to get how many times
def write_delay_deltas():
    delta_delay = find_value_total_delay()
    output = ""

    for item in delta_delay:

        output += str(item)+"_"+" ".join(str(e) for e in delta_delay[item])+" \n"

    file = open("delay.txt","w")
    file.write(output)
    file.close()

write_delay_deltas()
print("End of Create delay list")

