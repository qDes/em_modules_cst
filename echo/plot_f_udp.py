from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
import socket
import struct

x = []
y = []
c = 0
pack = struct.pack(">3c8f",b"C",b"2",b"H", 500, 0.006, 10,
        20,5,1,5,60)
x1 = []
y1 = []

class MyWidget(pg.GraphicsWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10) # in milliseconds
        self.timer.start()
        self.timer.timeout.connect(self.onNewData)

        self.plotItem = self.addPlot(title="Points_Force")

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
        '''
        numPoints = 1000  
        x = np.random.normal(size=numPoints)
        y = np.random.normal(size=numPoints)
        '''
        global x
        global y
        global c
        global pack
        global x1
        global y1
        #message = str(c+1)
        #message = message.encode()
        self.sock.sendto(pack,('127.0.0.1',5500))
        data, ip = self.sock.recvfrom(1024)
        data = struct.unpack(">3c2f",data)
        F = data[3]
        Pos = data[4]
        x.append(c) 
        y.append(F)
        c += 1
        x1.append(c)
        y1.append(Pos)
        self.setData(x, y)
        self.setData1(x1,y1)

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
