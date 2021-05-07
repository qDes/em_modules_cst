#!/usr/bin/python

import math
import random
import struct
import socket

UDP_IP_ADDRESS = "0.0.0.0"
UDP_PORT_NO = 5500
UDP_SEND = 5550

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
## One difference is that we will have to bind our declared IP address
## and port number to our newly declared serverSock
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

Pos = 0


def get_pseudo_packet(pos, F, pos1, F1):
    pos += 1
    pack = struct.pack(">3c10f", b"H", b"2", b"C", F, pos, 0, 0, 0, F1, pos1, 0, 0, 0)
    return pack


while True:
    F = abs(math.sin(math.radians(Pos)) * 200) + random.randint(1, 200)
    pos = 0.01 * (abs(math.cos(math.radians(Pos)) * 200) + random.randint(1, 20))
    F1 = abs(math.sin(math.radians(Pos)) * 100) + random.randint(10, 40)
    pos1 = abs(math.cos(math.radians(Pos)) * 100) + random.randint(10, 40)
    Pos += 0.1
    data, addr = serverSock.recvfrom(1024)
    data = struct.unpack(">3ci20f", data)
    print(data, addr)
    if data:
        sent = serverSock.sendto(get_pseudo_packet(pos, F, pos1, F1), (addr[0], UDP_SEND))