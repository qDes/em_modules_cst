import socket
import struct


class UDP:
    def __init__(self, i0=0, f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=0, f8=0, f9=0, f10=0, f11=0, f12=0, f13=0, f14=0,
                 f15=0, f16=0, f17=0, f18=0, f19=0, f20=0):
        self.i0 = i0
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.f4 = f4
        self.f5 = f5
        self.f6 = f6
        self.f7 = f7
        self.f8 = f8
        self.f9 = f9
        self.f10 = f10
        self.f11 = f11
        self.f12 = f12
        self.f13 = f13
        self.f14 = f14
        self.f15 = f15
        self.f16 = f16
        self.f17 = f17
        self.f18 = f18
        self.f19 = f19
        self.f20 = f20

        self.pack = struct.pack(">3ci20f", b"C", b"2", b"H", i0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13,
                                f14, f15, f16, f17, f18, f19, f20)
        self.ip = '192.168.0.193'
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_send.bind(('0.0.0.0', 5550))
        # self.sock_recv.settimeout(2)
        self.sock_send.settimeout(2)

        self.F0 = 0
        self.F1 = 0
        self.F2 = 0
        self.F3 = 0
        self.F4 = 0
        self.F5 = 0
        self.F6 = 0
        self.F7 = 0
        self.F8 = 0
        self.F9 = 0

        self.enable = False
        self.counter = 0

    def update_params(self, i0=0, f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=0, f8=0, f9=0, f10=0, f11=0, f12=0, f13=0,
                      f14=0, f15=0, f16=0, f17=0, f18=0, f19=0, f20=0):
        self.i0 = i0
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.f4 = f4
        self.f5 = f5
        self.f6 = f6
        self.f7 = f7
        self.f8 = f8
        self.f9 = f9
        self.f10 = f10
        self.f11 = f11
        self.f12 = f12
        self.f13 = f13
        self.f14 = f14
        self.f15 = f15
        self.f16 = f16
        self.f17 = f17
        self.f18 = f18
        self.f19 = f19
        self.f20 = f20
        self.pack = struct.pack(">3ci21f", b"C", b"2", b"H", i0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13,
                                f14, f15, f16, f17, f18, f19, f20)

    def send(self):
        # addr = ("192.168.0.193", 5500)
        addr = (self.ip, 5500)
        self.sock_send.sendto(self.pack, addr)
        data, ip = self.sock_send.recvfrom(2048)
        data = struct.unpack(">3c10f", data)
        self.F0 = data[0]
        self.F1 = data[1]
        self.F2 = data[2]
        self.F3 = data[3]
        self.F4 = data[4]
        self.F5 = data[5]
        self.F6 = data[6]
        self.F7 = data[7]
        self.F8 = data[8]
        self.F9 = data[9]
        return self.F0, self.F1, self.F2, self.F3, self.F4, self.F5, self.F6, self.F7, self.F8, self.F9, self.F10

    def connect(self, ip):
        self.ip = ip
        self.enable = True
