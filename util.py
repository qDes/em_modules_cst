import socket
import struct


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

        # self.
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.sock_recv.bind(('0.0.0.0', 5550))
        self.sock_recv.settimeout(1)

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
        self.sock_send.sendto(self.pack, ('0.0.0.0', 5500))
        data, ip = self.sock_recv.recvfrom(1024)
        data = struct.unpack(">3c10f", data)
        self.F = data[3]
        self.pos = data[4]
        return self.F, self.pos


class Plotter:

    def __init__(self):
        self.x1 = []
        self.x2 = []
        self.y1 = []
        self.y2 = []
        self.counter = 0

    def update(self, y1, y2):
        self.counter += 1
        self.y1.append(y1)
        self.y2.append(y2)
        self.x1.append(self.counter)
        self.x2.append(self.counter)
        if len(self.x1) > 100:
            self.x1 = self.x1[1:]
            self.x2 = self.x2[1:]
            self.y1 = self.y1[1:]
            self.y2 = self.y2[1:]
