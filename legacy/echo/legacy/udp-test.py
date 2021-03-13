#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import socket
import struct
from math import *
from time import *

UDP_IP = "127.0.0.1"
UDP_PORT = 5500

JOINTS = 2


class UDPtest():
    def __init__(self):
        self.num = 0
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

    def send_packet(self):
        #pack = struct.pack(">3cI14fI", "C", "2", "H", 1, 2, 3, 4, 5, 66.7, 7.0, 8.0, 9., 10., 11., 12.,
        #                   13., 14., 15., 16.)
        #pack = struct.pack(">3c4f", "C", "2", "H", 1.1, 2.0, 3.2, 4.3)
        pack = struct.pack(">3c8f", "C", "2", "H", 500, 0.006, 20, 5, 1.1, 1, 5, 200000)
        err = self.sock.sendto(pack, (UDP_IP, UDP_PORT))
        print err
        self.num += 1
        if self.num % 100 == 0:
            print ".",
            sys.stdout.flush()


udp = UDPtest()
while True:
    udp.send_packet()
    print "Send param"
    sleep(1)
    
