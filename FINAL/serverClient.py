"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import socket
from random import randint

from pythonosc import dispatcher
from pythonosc import osc_server

# Al parametro save tiene que entrar el idCancion;idUsuario;Beats;Delay
# Donde los beats deben ir separados por comas
# Uun ejemplo 1;2;0.332,5.336,7.5552;0.5


def save_handler(unused_addr, args, save):
    print("[{0}] ~ {1}".format(args[0], save))

    msg_from_client = "Save|{0}".format(save)
    bytes_to_send = str.encode(msg_from_client)
    server_address_port = ("127.0.0.1", 20001)
    buffer_size = 16384

    # Create a UDP socket at client side
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    udp_client_socket.sendto(bytes_to_send, server_address_port)

    msg_from_server = udp_client_socket.recvfrom(buffer_size)

    msg = "Message from Server {}".format(msg_from_server[0])

    print(msg)

    return


def start_handler(unused_addr, args, msg):
    print("[{0}] ~ {1}".format(args[0], msg))

    # Read the .txt using the path addressed by the client

    msg_from_client = "Ready,{0}".format(msg)
    bytes_to_send = str.encode(msg_from_client)
    server_address_port = ("127.0.0.1", 20001)
    buffer_size = 16384

    # Create a UDP socket at client side
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    udp_client_socket.sendto(bytes_to_send, server_address_port)

    msg_from_server = udp_client_socket.recvfrom(buffer_size)

    msg = "Message from Server {}".format(msg_from_server[0])

    print(msg)

    # Send song id to client (Pure Data)

   # client = udp_client.SimpleUDPClient("127.0.0.1", 20002)
    #client.send_message("/songid", msg_from_server[0])

    return


if __name__ == "__main__":

    dispatcher = dispatcher.Dispatcher()

    dispatcher.map("/save", save_handler, "Save ")
    dispatcher.map("/start", start_handler, "Ready")

    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 5005), dispatcher)
    print("ServerOSC in Client Ready on {}".format(server.server_address))
    server.serve_forever()
