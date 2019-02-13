"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
from random import randint
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    x = randint(1, 10)
 #   client.send_message("/start", str(x))

    rnd_song = randint(1, 10)
    rnd_usr = randint(1, 10)
    example = "{0};{1};0.332,5.336,7.5552;0.5".format(rnd_song, rnd_usr)
    client.send_message("/save", example)

    # time.sleep(1)
