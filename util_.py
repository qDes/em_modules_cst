import csv
import datetime
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
        self.pack = struct.pack(">3ci20f", b"C", b"2", b"H", i0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13,
                                f14, f15, f16, f17, f18, f19, f20)

    def send(self):
        # addr = ("192.168.0.193", 5500)
        addr = (self.ip, 5500)
        try:
            self.sock_send.sendto(self.pack, addr)
            data, ip = self.sock_send.recvfrom(2048)
            data = struct.unpack(">3c10f", data)
            self.F0 = data[3]
            self.F1 = data[4]
            self.F2 = data[5]
            self.F3 = data[6]
            self.F4 = data[7]
            self.F5 = data[8]
            self.F6 = data[9]
            self.F7 = data[10]
            self.F8 = data[11]
            self.F9 = data[12]
            return self.F0, self.F1, self.F2, self.F3, self.F4, self.F5, self.F6, self.F7, self.F8, self.F9
        except socket.timeout:
            print("timeout")
            self.enable = False
            return None

    def connect(self, ip):
        self.ip = ip
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
        ts = int(datetime.datetime.now().timestamp())

        self.y1.append(y1)
        self.y2.append(y2)
        self.y3.append(y3)
        self.y4.append(y4)
        '''
        self.x1.append(ts)
        self.x2.append(ts)
        self.x3.append(ts)
        self.x4.append(ts)
        '''
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


class PlotSaver:
    def __init__(self, directory, name):
        self.is_saving = False
        self.directory = directory
        self.param1 = []
        self.param2 = []
        self.param3 = []
        self.param4 = []
        self.ts = []
        self.my_file = ''
        self.name = name

    def start(self):
        if self.is_saving:
            return None

        self.is_saving = True
        self.my_file = self.directory+f'/{self.name}_{datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")}.csv'
        with open(self.my_file, 'w+') as my_file:
            pass

    def stop(self):
        self.is_saving = False
        self.__save()

    def get_data(self, param1, param2, param3=None, param4=None):
        self.ts.append(datetime.datetime.now().timestamp())
        self.param1.append(param1)
        self.param2.append(param2)
        if param3:
            self.param3.append(param3)
        if param4:
            self.param4.append(param4)

        if len(self.ts) > 100:
            self.__save()


    def __save(self):
        with open(self.my_file, 'a+') as my_file:
            writer = csv.writer(my_file, delimiter=',')
            for i, item in enumerate(self.ts):
                if self.param3:
                    writer.writerow([self.param1[i], self.param2[i], self.param3[i], self.param4[i], item])
                else:
                    writer.writerow([self.param1[i], self.param2[i], item])
        self.param1 = []
        self.param2 = []
        self.param3 = []
        self.param4 = []
        self.ts = []
