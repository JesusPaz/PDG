import pymysql


def get_all_delay_beats():
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `BEATS_MSG` FROM `delay`"
            cursor.execute(sql)
            query = cursor.fetchall()

            return query

    finally:
        connection.close()


def convert_query_to_dict():
    query = get_all_delay_beats()
    dict = {}
    x = 0
    for item in query:
        dict[x] = item[0]
        x += 1

    return dict


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


def process_delay_using_gap(gap, delay):
    list_processed = []
    for x in delay:
        if x != "":
            list_processed.append(abs(float(x) - gap))

    return list_processed


def find_value_total_delay():

    delay_list = convert_query_to_dict()

    value_delay = {}

    dict_counts = {}

    beat_times = find_beat_time_from_bpm(82, 30)

    # For to get all the gaps

    gap = 0
    while gap < 1:

        for item in delay_list:

            delta_list = []
            delay_beats = delay_list[item].split(" ")

            # Process the list using the gap
            delay_beats = process_delay_using_gap(gap, delay_beats)

            #print(delay_beats)

            index_beat_list = 0

            for i in range(0, len(delay_beats)):
                extra_index = 0
                for y in range(0, 3):
                    extra_index = y
                    if (index_beat_list+y) < len(beat_times):

                        if abs(float(delay_beats[i])-float(beat_times[index_beat_list+y])) < 0.2:

                            delta_list.append(abs(round(float(delay_beats[i])-float(beat_times[index_beat_list+y]), 2)))
                            break

                index_beat_list = index_beat_list + extra_index
            value_delay[item] = delta_list

        cont = 0
        # print(value_delay)
        for item in value_delay:

            cont += len(value_delay[item])

        # print(gap)
        # print(cont)
        dict_counts[gap] = cont
        gap += 0.001

    return dict_counts


def write_counts_file():
    dict = find_value_total_delay()
    msg = "gap,value\n"
    for x in dict:
        msg += str(x*1000)[:5] + "," + str(dict[x])+"\n"

    file = open("gap_counts.txt","w")
    file.write(msg)
    file.close()


write_counts_file()
print("End of Find Gap")