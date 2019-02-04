# Taken from: https://pythontic.com/modules/socket/udp-client-server-example
import socket

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")


def select_songs():
    songs = "Songs"

    return songs


# Listen for incoming datagrams

while True:

    message, address = UDPServerSocket.recvfrom(bufferSize)

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    if message == "Ready":

        print("Ready to send the id songs")
        # Sending a Answer to client
        UDPServerSocket.sendto(select_songs(), address)


    else:

        print("Receiving the path")
        # Sending a reply to client

        UDPServerSocket.sendto(bytesToSend, address)
