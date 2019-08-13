import pymysql
import matplotlib.pyplot as plt
import collections
import numpy as np
import seaborn as sns
import pandas as pd

def get_all_delays():
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            sql = "SELECT `CEDULA_USUARIO`, `BEATS_MSG` FROM `delay`"
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
                #print(repetitions[float(item[0])])
    #print(repetitions)
    return repetitions


def find_space_between_data(list_string):
    array_data = list_string.split(" ")
    list_return = []

    for x in range(0, len(array_data)):
        if (x + 1) < len(array_data):
            delta = float(array_data[x + 1]) - float(array_data[x])
            list_aux = []
            list_aux.append(round(delta, 2))
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
            break

    return dict_deltas

def aux_process_dict():
    dict_list = create_dict_list()
    dict_deltas = {}
    user = 1233194515
    dict_deltas[user] = None
    deltas = find_space_between_data(dict_list[user][0])
    dict_deltas[user] = calculate_repetitions_delay_user(deltas, dict_deltas[user])

    return dict_deltas

def print_graphics():

    #delay = process_delay_dict()
    delay = aux_process_dict()

    for user in delay.keys():
        fig, axs = plt.subplots(figsize=(10, 10))
        fig.suptitle(user)
        data_list = []

        data_list = collections.OrderedDict(sorted(delay[user].items()))

        axs.plot(list(data_list.keys()), list(data_list.values()))
        break

    plt.show()

#print_graphics()


def print_heatmap():
    delay = aux_process_dict()

    user = "1233194515"
    date = ""
    msg = "quantity,value,time\n"


    for data in delay:

        x = 1
        for item in delay[data]:

            msg += str(x)+","+str(data)+","+str(item)+"\n"
            x += 1

    file = open("heat.csv", "w")
    file.write(msg)
    file.close()


def aux_print():
    delay = aux_process_dict()

    user = 1233194515
    date = ""
    msg = "quantity,value,time\n"

    for data in delay[user]:

        aux_list = delay[user][data]

        x = 1
        for item in aux_list:
            msg += str(x) + "," + str(data) + "," + str(item) + "\n"
            x += 1


    print(msg)
    file = open("heat.csv", "w")
    file.write(msg)
    file.close()


def draw_heatmap():
    aux_print()

    data = pd.read_csv("heat.csv")
    ax = sns.heatmap(data)




draw_heatmap()