import socket
import struct

from dearpygui.core import get_value, clear_plot


class UDP:
    def __init__(self, i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5,
                 d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6):
        self.i0 = i0
        self.jam_pos_in = jam_pos_in
        self.F_set = F_set
        self.kShaker = kShaker
        self.shaker_freq = shaker_freq
        self.m = m
        self.f_mode2 = f_mode2
        self.f_mode3 = f_mode3
        self.a_mode5 = a_mode5
        self.b_mode5 = b_mode5
        self.c_mode5 = c_mode5
        self.d_mode5 = d_mode5
        self.g_mode5 = g_mode5
        self.v_mode6 = v_mode6
        self.kD_mode6 = kD_mode6
        self.pow_mode6 = pow_mode6
        self.pack = struct.pack(">3ci21f", b"C", b"2", b"H", i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2,
                                f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6, 0,
                                0, 0, 0, 0, 0)
        self.ip = '192.168.0.193'
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_send.bind(('0.0.0.0', 5550))
        self.sock_recv.settimeout(2)
        self.sock_send.settimeout(2)
        self.F = 0
        self.pos = 0
        self.enable = False
        self.counter = 0

    def update_params(self, i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2, f_mode3, a_mode5, b_mode5, c_mode5,
                      d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6):
        self.i0 = i0
        self.jam_pos_in = jam_pos_in
        self.F_set = F_set
        self.kShaker = kShaker
        self.shaker_freq = shaker_freq
        self.m = m
        self.f_mode2 = f_mode2
        self.f_mode3 = f_mode3
        self.a_mode5 = a_mode5
        self.b_mode5 = b_mode5
        self.c_mode5 = c_mode5
        self.d_mode5 = d_mode5
        self.g_mode5 = g_mode5
        self.v_mode6 = v_mode6
        self.kD_mode6 = kD_mode6
        self.pow_mode6 = pow_mode6
        self.pack = struct.pack(">3ci21f", b"C", b"2", b"H", i0, jam_pos_in, F_set, kShaker, shaker_freq, m, f_mode2,
                                f_mode3, a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, v_mode6, kD_mode6, pow_mode6, 0,
                                0, 0, 0, 0, 0)

    def send(self):
        addr = ("192.168.0.193", 5500)
        self.sock_send.sendto(self.pack, addr)
        data, ip = self.sock_send.recvfrom(2048)
        data = struct.unpack(">3c10f", data)
        self.F = data[3]
        self.pos = data[4]
        return self.F, self.pos

    def connect(self, ip):
        self.ip = ip
        # self.sock_recv.bind((ip, 5550))
        # self.sock_recv.settimeout(20)
        self.enable = True


class Plotter:
    def __init__(self):
        self.x1 = []
        self.x2 = []
        self.x3 = []
        self.x4 = []

        self.y1 = []
        self.y2 = []
        self.y3 = []
        self.y4 = []

        self.counter = 0

    def update(self, y1=0, y2=0, y3=0, y4=0):
        self.counter += 1

        self.y1.append(y1)
        self.y2.append(y2)
        self.y3.append(y3)
        self.y4.append(y4)

        self.x1.append(self.counter)
        self.x2.append(self.counter)
        self.x3.append(self.counter)
        self.x4.append(self.counter)

        if len(self.x1) > 100:
            self.x1 = self.x1[1:]
            self.x2 = self.x2[1:]
            self.x3 = self.x3[1:]
            self.x4 = self.x4[1:]

            self.y1 = self.y1[1:]
            self.y2 = self.y2[1:]
            self.y3 = self.y3[1:]
            self.y4 = self.y4[1:]



