"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client
import numpy as np


def create_rnd_beats(n):
    sum = 0
    cad = ""
    for x in range(0, n-1):
        num = random.random()
        sum += num
        if(x<n-2):
            cad += str(num)[:5]+","
        else:
            cad += str(num)[:5]
    return cad, sum


def sum_beats(cad):
    arr = cad.split(",")
    suma = 0.0
    for x in arr:
        suma += float(x)

    return suma


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    x = random.randint(1, 10)
   # client.send_message("/start", str(x))

    print("start {}".format(x))

    rnd_song = random.randint(1, 10)
    rnd_usr = random.randint(1, 10)
    beats, sum = create_rnd_beats(5)
    print("Suma beats = {0}".format(sum))
    print("Beats : {0}".format(beats))
    example = "{0} {1} {2} 0.5 {3}".format("Marc_Anthony-Ahora_Quien.wav", "5", "0", "10 20 50 30 60 90 80 8 07 04 06 060 ")
    client.send_message("/save", example)
    print("Suma del metodo =",str(sum_beats(beats)))
#1;1;0.374,0.497,0.950,0.074;1.895
    # time.sleep(1)
