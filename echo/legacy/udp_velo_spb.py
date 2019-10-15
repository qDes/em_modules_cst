#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket
import re
from time import *
import sys
import hal
import struct
from math import *

DEBUG = True
UDP_IP = "127.0.0.1"
UDP_PORT = 5500  # server port
UDP_HOST_PORT = 5550  # client port
PARAM_FILE = os.path.join(os.path.dirname(__file__), "./param.hal")
PACKET_SIZE = 32
HEADER_SIZE = 3

MATH_MODEL = "cls-velo"
INNER_LOOP = "inner-loop-velo"

# Linuxcnc pins list (JOINT_PINS included in there automatically).
PINS = {
    "in":
        {
            "s32": [],
            "bit": [],
            "float": [],
        },
    "out":
        {
            "s32": ["state"],
            "bit": ["connected", "watchdog"],
            "float": ["packets"],
        },
}

# Joints number.
JOINTS = 1

# Pins of each joint.
JOINT_PINS = {"in":
    {
        "s32": [],
        "bit": [],
        "float": [
            "f00",  # F_act
            "f01",  # Pos
            "f02",  # 
            "f03",  # 
            "f04",  # 
            "f05",  # 
            "f06",  # 
            "f07",  # 
        ],
    },
    "out":
        {
            "s32": [],
            "bit": [],
            "float": [],
        },
}

# Join JOINT_PINS to PINS automatically.
for i in range(JOINTS):
    for d in PINS:
        for t in PINS[d]:
            for p in JOINT_PINS[d][t]:
                PINS[d][t].append("j%s.%s" % (i, p))

PARAMS_JOINT = [
    "F-set",
    "kShaker",
    "shaker-freq",
    "m-inner",
    "kPedal",
    "shaker-limit",
    "friction",
    "p-set"
]


class UDP:
    def __init__(self):
        # Create UDP socket.
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

        self.sock.bind((UDP_IP, UDP_PORT))
        self.host_addr = ()
        self.joints = [[] for i in range(JOINTS)]
        self.parameters = [[] for i in range(JOINTS)]
        self.header = []
        self.last_t = 0
        self.connected = False
        self.num = 0
        self.rejected_num = 1

        #return  # comment it on real linuxcnc system

        # Create HAL pins according to the PINS list.
        self.comp = hal.component("udp")
        for p in PINS["in"]["s32"]:
            self.comp.newpin(p, hal.HAL_S32, hal.HAL_IN)
        for p in PINS["in"]["bit"]:
            self.comp.newpin(p, hal.HAL_BIT, hal.HAL_IN)
        for p in PINS["in"]["float"]:
            self.comp.newpin(p, hal.HAL_FLOAT, hal.HAL_IN)
        for p in PINS["out"]["s32"]:
            self.comp.newpin(p, hal.HAL_S32, hal.HAL_OUT)
        for p in PINS["out"]["bit"]:
            self.comp.newpin(p, hal.HAL_BIT, hal.HAL_OUT)
        for p in PINS["out"]["float"]:
            self.comp.newpin(p, hal.HAL_FLOAT, hal.HAL_OUT)

        self.comp.ready()
        self.bad_pack_count = 0

    def __repr__(self):
        res = ""
        res += "UDP %s \n" % [self.header]
        for i in range(JOINTS):
            res += "Joint %s %s\n" % (i, ["%0.2f" % float(f) for f in self.joints[i]])
        # res += "Parmeters %s\n"% ["%0.2f"%float(f) for f in self.parameters[i]]
        res += "\n"
        return res

    def check_packet(self, p, addr):
        if not self.connected:
            header = p[:HEADER_SIZE]
            if header == 'C2H':
                self.host_addr = addr
                self.num = 0
                self.connected = True
                self.last_t = time()
                self.bad_pack_count = 0
                print "udp.py: Connected to %s" % [self.host_addr]
                return True
        if addr == self.host_addr:
            return True
        else:
            return False

    def get_packet(self):
        p, addr = self.sock.recvfrom(2048)  # buffer size is 2048 bytes
        if DEBUG:
            print "\nGot packet: ",
            self.print_packet(p)
            print addr

        if self.last_t < time() - 2 and self.connected:
            self.connected = False
            print "Disconnected"

        if not self.check_packet(p, addr):
            self.rejected_num += 1
            if self.rejected_num % 100 == 0:
                print "x",
                sys.stdout.flush()
            return
        self.last_t = time()
        self.num += 1
        if self.num % 100 == 0:
            print ".",
            sys.stdout.flush()
            if self.num % 400 == 0:
                print self
        self.parse_pack(p)

    def parse_parameters(self, p):
        print(len(p), PACKET_SIZE)
        for i in range(JOINTS):
            if len(p) >= PACKET_SIZE:
                self.parameters[i] = self.parse_param(p[:PACKET_SIZE])
        self.save_param()

    def parse_param(self, p):
        p_num = len(JOINT_PINS['in']['float'])
        if DEBUG:
            print ["%0.2f" % f for f in struct.unpack(">%df" % p_num, p)]
        return ["%0.2f" % f for f in struct.unpack(">%df" % p_num, p)]

    def get_param(self):
        param = {}
        s = open(PARAM_FILE, "r").read()
        for l in s.split("\n"):
            r = re.search("setp\s+((%s|%s).\d+.\S+)\s+(\S+)" % (MATH_MODEL, INNER_LOOP), l)
            if r:
                param[r.group(1)] = r.group(3)
        if DEBUG:
            print(param)
        return param

    def save_param(self):
        joints_data = self.parameters
        if DEBUG:
            print("joints data from udp: ")
            print(joints_data)
        names = PARAMS_JOINT
        param = self.get_param()
        for j, joint in enumerate(joints_data):
            for i, p in enumerate(joint):
                n = '%s.%s.%s' % (MATH_MODEL, j, names[i])
                inn = '%s.%s.%s' % (INNER_LOOP, j, names[i])
                if n in param:
                    param[n] = p
                if inn in param:
                    param[inn] = p
        res = []
        for p in param:
            if DEBUG:
                print("key value: ")
                print(p, param[p])
            res.append("setp %s		%s" % (p, param[p]))
        res.sort()
        f = open(PARAM_FILE, "w")
        f.write("# DO NOT EDIT THIS FILE MANUALLY\n\n")

        for s in res:
            f.write(s + "\n")
        f.close()
        print "udp.py: Parameters save"
        #return  # todo
        print os.popen("halcmd -f %s" % PARAM_FILE).read()

    def parse_pack(self, pack):
        header = pack[:HEADER_SIZE]
        if header == "C2H":
            self.header = header
            self.parse_parameters(pack[HEADER_SIZE:])
            self.send_packet()
            print "z"
        else:
            print "udp.py: Got bad packet - unknown header."
            print self.print_packet(pack)

    def send_packet(self):
        js = "j%s." % 0
        pack = struct.pack(">3c2f", "H", "2", "C", self.comp[js+"f00"], self.comp[js+"f01"])
        self.send(pack)

    def print_packet(self, p):
        for c in p:
            print hex(ord(c)),
        print

    def send(self, pack, addr=None):
        if addr is None:
            addr = (self.host_addr[0], UDP_HOST_PORT)
        print addr
        self.sock.sendto(pack, addr)

        if DEBUG:
            print "Send packet:"
            self.print_packet(pack)


udp = UDP()
while True:
    print("try to get packet")
    udp.get_packet()

