import pymysql


def get_all_delays():
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `CEDULA_USUARIO`, `BEATS_MSG`, `FECHA` FROM `delay`"
            cursor.execute(sql)
            query = cursor.fetchall()
            # print(query)
            return query

    finally:
        connection.close()


def global_create_dict_list():
    query = get_all_delays()
    dict_beats = {}
    for item in query:
        if item[0] not in dict_beats.keys():
            list = []
            list.append(item[1])
            dict_beats[item[0]] = list

        else:
            aux_list = dict_beats[item[0]]
            aux_list.append(item[1])
            dict_beats[item[0]] = aux_list

    return dict_beats


def individual_create_dict_list():
    query = get_all_delays()
    dict_beats = {}
    for item in query:
        date = "{0}-{1}-H{2}-{3}".format(str(getattr(item[2], 'day')), str(getattr(item[2], 'month')),
                                        str(getattr(item[2], 'hour')), str(getattr(item[2], 'minute')))
        dict_beats[str(item[0])+"_"+date] = item[1]

    return dict_beats


def subs_gap_to_list(gap, list):
    return_list = []
    for x in list:
        if x != "":
            return_list.append(abs(float(x)-gap))

    return return_list


def process_global_delays():
    query = global_create_dict_list()

    return_dict = {}

    for user in query:
        list_gaps = []
        for delays in query[user]:

            act_delays = delays.split(" ")
            act_delays = subs_gap_to_list(0.05, act_delays)

            for beat in act_delays:
                act_beat = str(int(round(beat - (int(beat/0.7317)*0.7317), 4)*1000))
                list_gaps.append(act_beat)

        return_dict[user] = list_gaps
    return return_dict


def process_individual_delays():
    query = individual_create_dict_list()
    return_dict = {}
    for user in query.keys():

        list_gaps = []

        act_delays = query[user].split(" ")
        act_delays = subs_gap_to_list(0.05, act_delays)

        for beat in act_delays:
            act_beat = str(int(round(beat - (int(beat/0.7317)*0.7317), 4)*1000))
            list_gaps.append(act_beat)

        return_dict[user] = list_gaps
    return return_dict


def write_global_gaps():
    delay = process_global_delays()
    msg = ""
    for user in delay:
        msg += str(user)+"_"+" ".join(delay[user])+"\n"

    file = open("../Jupyter_Files/Data/Global_Hw/gap_hw.txt","w")
    file.write(msg)
    file.close()

    delay = process_individual_delays()
    msg = ""
    for user in delay:
        msg += str(user) + "_" + " ".join(delay[user]) + "\n"

    file = open("../Jupyter_Files/Data/Individual_Hw/gap_hw.txt", "w")
    file.write(msg)
    file.close()

write_global_gaps()
print("End of Get gap hw")