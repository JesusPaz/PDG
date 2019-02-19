"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client


def create_rnd_beats(n):
    sum = 0
    cad = ""
    for x in range(0, n-1):
        num = random.random()
        sum += num
        cad += str(num)[:15]+","

    return cad, sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    x = random.randint(1, 10)
    client.send_message("/start", str(x))

    print("start {}".format(x))

    rnd_song = random.randint(1, 10)
    rnd_usr = random.randint(1, 10)
    beats, sum = create_rnd_beats(500)
    #aprint("Suma beats = {0}".format(sum))
   # print("Beats : {0}".format(beats))
    example = "{0};{1};{2};0.5".format(rnd_song, rnd_usr,beats)
    #client.send_message("/save", example)

    # time.sleep(1)
