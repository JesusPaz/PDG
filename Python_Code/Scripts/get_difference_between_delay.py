import pymysql
import matplotlib.pyplot as plt
import collections

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


def create_dict_list():
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


def aux_create_dict_list():
    query = get_all_delays()
    dict_beats = {}
    for item in query:
        date = "{0}-{1}-H{2}-{3}".format(str(getattr(item[2], 'day')), str(getattr(item[2], 'month')),
                                        str(getattr(item[2], 'hour')), str(getattr(item[2], 'minute')))
        dict_beats[str(item[0])+"_"+date] = item[1]

    return dict_beats


def calculate_repetitions_delay_user(new_deltas, actual_deltas):
    if actual_deltas == None:
        repetitions = {}
    else:
        repetitions = actual_deltas

    for item in new_deltas:
        list_aux = []
        if float(item[1]) <= 30:
            if float(item[0]) in repetitions:
                aux = repetitions[float(item[0])]
                aux.append(item[1])
                repetitions[float(item[0])] = aux
            else:
                list_aux.append(item[1])
                repetitions[float(item[0])] = list_aux

    return repetitions


def find_space_between_data(list_string):
    array_data = list_string.split(" ")
    list_return = []
    gap = 0.051
    for x in range(0, len(array_data)):
        if (x + 1) < len(array_data):
            delta = (float(array_data[x + 1]) + gap) - (float(array_data[x]) + gap)
            list_aux = []
            list_aux.append(round(delta, 3))
            list_aux.append(float(array_data[x]))
            list_return.append(list_aux)

    return list_return


def process_delay_dict():
    dict_list = create_dict_list()
    dict_deltas = {}
    for user in dict_list:

        dict_deltas[user] = None

        for item in dict_list[user]:

            deltas = find_space_between_data(item)
            dict_deltas[user] = calculate_repetitions_delay_user(deltas, dict_deltas[user])

    return dict_deltas


def aux_process_delay_dict():
    dict_list = aux_create_dict_list()
    dict_deltas = {}

    for user in dict_list:
        deltas = find_space_between_data(dict_list[user])
        dict_deltas[user] = calculate_repetitions_delay_user(deltas, None)

    return dict_deltas


def print_graphics():

    delay = process_delay_dict()
    #delay = aux_process_dict()

    for user in delay.keys():
        fig, axs = plt.subplots(figsize=(10, 10))
        fig.suptitle(user)
        data_list = []

        data_list = collections.OrderedDict(sorted(delay[user].items()))

        axs.plot(list(data_list.keys()), list(data_list.values()))
        break

    plt.show()


def aux_print_heatmap():
    delay = aux_process_delay_dict()

    for user in delay:
        msg = "counts,value,time\n"
        compare_index = delay[user]
        #print(compare_index)
        for data in delay[user]:

            aux_list = delay[user][data]

            x = 0
            for item in aux_list:
                msg += str(x) + "," + str(data) + "," + str(item) + "\n"
                x += 1

        index_numbers = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]

        for x in index_numbers:

            if x not in compare_index.keys():
                msg += "0,"+str(x)+",\n"

        path = "../Jupyter_Files/Data/Individual/"+user+".csv"
        count_number_values_individual(delay, user)
        #print(path)
        file = open(path, "w")
        file.write(msg)
        file.close()


def aux_print_global_heatmap():

    delay = process_delay_dict()
    count_number_values_global(delay)
    for user in delay:
        msg = "counts,value,time\n"
        compare_index = delay[user]

        for data in delay[user]:

            aux_list = delay[user][data]

            x = 0
            for item in aux_list:
                msg += str(x) + "," + str(data) + "," + str(item) + "\n"
                x += 1

        index_numbers = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]

        for x in index_numbers:

            if x not in compare_index.keys():
                msg += "0,"+str(x)+",\n"

        path = "../Jupyter_Files/Data/Global/"+str(user)+".csv"

        file = open(path, "w")
        file.write(msg)
        file.close()


def count_number_values_global(delay):

    for user in delay:

        dict_count = {}
        for value in delay[user]:
            if (int(value*1000) >= 300) & (int(value*1000) <= 800):
                dict_count[int(value*1000)] = len(delay[user][value])

        # if user == 1002956450:
            # print(delay[1002956450])
            # print(delay[1143874902])
            # print(dict_count)

        index = 300
        while index <=800:
            if index not in dict_count:
                dict_count[index] = 0

            index += 1

        dict_count = sorted(dict_count.items())

        msg = "value,counts\n"
        for value in dict_count:
            msg += str(value[0]) + "," + str(value[1]) + "\n"

        path = "../Jupyter_Files/Data/Global_Counts/" + str(user) + ".csv"

        file = open(path, "w")
        file.write(msg)
        file.close()



def count_number_values_individual(delay, name):



    for user in delay:
        dict_count = {}
        for value in delay[user]:
            if (int(value*1000) >= 300) & (int(value*1000) <= 800):
                dict_count[int(value*1000)] = len(delay[user][value])


        index = 300
        while index <=800:

            if index not in dict_count:
                dict_count[index] = 0

            index += 1



        dict_count = sorted(dict_count.items())

        msg = "value,counts\n"
        for value in dict_count:
            msg += str(value[0]) + "," + str(value[1]) + "\n"

        path = "../Jupyter_Files/Data/Individual_Counts/" + str(user) + ".csv"

        file = open(path, "w")
        file.write(msg)
        file.close()


aux_print_heatmap()
aux_print_global_heatmap()
print("End of get diff btw hw")




