import socket
import asyncio
import struct
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
from datetime import datetime

class MyWidget(pg.GraphicsWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.c = datetime.now().timestamp()
        self.x = []
        self.y = []
        self.x1 = []
        self.y1 = []
        
        self.pack = struct.pack(">3c8f",b"C",b"2",b"H", 500, 0.006, 10,
        1,5,1,5,60)
        self.sock_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_recv.connect(('192.168.0.101', 23))


        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10) # in milliseconds
        self.timer.start()
        self.timer.timeout.connect(self.onNewData)

        self.plotItem = self.addPlot(title="Points_Force")
        self.plotItem.setYRange(0,2500)
        self.plotDataItem = self.plotItem.plot([], pen=None, 
            symbolBrush=(255,0,0), symbolSize=5, symbolPen=None)
        
        ####
        self.plotItem1 = self.addPlot(title="Points_Pos")
        
        self.plotDataItem1 = self.plotItem1.plot([], pen=None, 
            symbolBrush=(255,0,0), symbolSize=5, symbolPen=None)
 

    def setData(self, x, y):
        self.plotDataItem.setData(x, y)
    
    def setData1(self, x, y):
        self.plotDataItem1.setData(x, y)



    def onNewData(self):
        #self.sock_send.sendto(self.pack,('127.0.0.1',5500))
        pedal_tenzo = self.sock_recv.recv(1024)
        if chr(pedal_tenzo[0]) == '$':
            message = pedal_tenzo[:12]
            data = decode_wifi(message)

            F = data[4]
            Pos = data[5]
            self.x.append(self.c) 
            self.y.append(F)
            #selfc += 1
            self.c = datetime.now().timestamp()
            self.x1.append(self.c)
            self.y1.append(Pos)
        
        if len(self.x1) > 300:
            del self.x1[0]
            del self.y1[0]
            del self.x[0]
            del self.y[0]

        self.setData(self.x, self.y)
        self.setData1(self.x1,self.y1)

def main():
    app = QtWidgets.QApplication([])

    pg.setConfigOptions(antialias=False) # True seems to work as well

    win = MyWidget()
    win.show()
    win.resize(800,600) 
    win.raise_()
    app.exec_()

def decode_wifi(data: list) -> tuple:
    try:
        header, number, t0, t1,  t2, half, encoderL, f0, f1, sum1 = struct.unpack('<ccBBBBBhhB', data)
    except struct.error:
        return None
    timer = bytearray(4)
    #print(type(t0))
    timer[0] = t0
    timer[1] = t1
    timer[2] = t2
    timer[3] = half & 0xF0
    timer_long = struct.unpack('<L', timer)
    encoder = bytearray(2)
    encoder[0] = encoderL
    encoder[1] = half & 0x0F
    encoder_int = struct.unpack('<H', encoder)

    return (header, ord(number), timer_long[0], encoder_int[0], f0, f1, sum1)


async def read_pedal(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    while True:
        pedal_tenzo = await reader.read(2048)
        # check header
        if chr(pedal_tenzo[0]) == '$':
            message = pedal_tenzo[:12]
            data = decode_wifi(message)
            print(f"f0={data[4]},f1={data[5]}")



if __name__ == "__main__":
    main()
    '''
    sock_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_recv.connect(('192.168.0.101', 23))
    while True:
        pedal_tenzo = sock_recv.recv(1024)
        if chr(pedal_tenzo[0]) == '$':
            message = pedal_tenzo[:12]
            data = decode_wifi(message)
            print(f"f0={data[4]},f1={data[5]}")
    '''
