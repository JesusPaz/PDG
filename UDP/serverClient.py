"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import socket

from pythonosc import dispatcher
from pythonosc import osc_server


def read_txt(path):
    document = open(path, 'r')

    return document.read()


def path_handler(unused_addr, args, path):
    print("[{0}] ~ {1}".format(args[0], path))

    # Read the .txt using the path addressed by the client

    msg_from_client = read_txt(path)
    bytes_to_send = str.encode(msg_from_client)
    server_address_port = ("127.0.0.1", 20001)
    buffer_size = 1024

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

    msg_from_client = "Ready"
    bytes_to_send = str.encode(msg_from_client)
    server_address_port = ("127.0.0.1", 20001)
    buffer_size = 1024

    # Create a UDP socket at client side
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    udp_client_socket.sendto(bytes_to_send, server_address_port)

    msg_from_server = udp_client_socket.recvfrom(buffer_size)

    msg = "Message from Server {}".format(msg_from_server[0])

    print(msg)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()

    dispatcher.map("/path", path_handler, "Path")
    dispatcher.map("/start", start_handler, "Ready")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("ServerOSC in Client Ready on {}".format(server.server_address))
    server.serve_forever()
