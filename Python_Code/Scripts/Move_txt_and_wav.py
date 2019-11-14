from pydub import AudioSegment
import pymysql
import shutil, os

all_id = {}
path_txt = "../Jupyter_Files/Data/Processed_Songs/"
path_mp3 = "../UDP_Files/Audio/"
path_wav = "../../../PD/cancionesytags/"

# Script to move create all txt and wav files in the folder. Because I want to listen and find the delay un Pure Data.


# Get all songs that have 3 repetitions
def get_songs_completed():
    global all_id

    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:

        with connection.cursor() as cursor:

            sql = "SELECT `ID_CANCION`, `NOMBRE_CANCION` FROM `despacho_cancion` WHERE `REPETICIONES` = 3"
            cursor.execute(sql)
            aux = cursor.fetchall()

            for x in aux:
                all_id[x[0]] = x[1]

    finally:
        connection.close()


def process_all_songs():
    global all_id
    get_songs_completed()
    not_found = []
    total = len(all_id)
    count = 0
    for id in all_id:
        song_name = all_id[id]
        if os.path.exists(path_txt+str(id)+".txt"):
            shutil.copy2(path_txt+str(id)+".txt", path_wav+str(id)+".txt")
            AudioSegment.from_mp3(path_mp3+song_name+".mp3").export(path_wav+str(id)+".wav", format="wav")
            count += 1

            print(str(round(count/total,2)*100)+"%")
        else:
            not_found.append(id)

    print("Not found: "+str(len(not_found))+"/"+str(total))
    print(not_found)


process_all_songs()
