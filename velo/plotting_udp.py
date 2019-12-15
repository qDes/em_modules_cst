from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
import socket
import struct

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
        self.sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_recv.bind(('192.168.0.100',5550))


        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10) # in milliseconds
        self.timer.start()
        self.timer.timeout.connect(self.onNewData)

        self.plotItem = self.addPlot(title="Points_Force")
        self.plotItem.setYRange(0,500)
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
        data, ip = self.sock_recv.recvfrom(1024)
        data = struct.unpack(">3c2f",data)
        F = data[3]
        Pos = data[4]
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

if __name__ == "__main__":
    main()
