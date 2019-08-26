from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
import socket

x = []
y = []
c = 0

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

        self.plotItem = self.addPlot(title="Points")

        self.plotDataItem = self.plotItem.plot([], pen=None, 
            symbolBrush=(255,0,0), symbolSize=5, symbolPen=None)


    def setData(self, x, y):
        self.plotDataItem.setData(x, y)


    def onNewData(self):
        '''
        numPoints = 1000  
        x = np.random.normal(size=numPoints)
        y = np.random.normal(size=numPoints)
        '''
        global x
        global y
        global c
        message = str(c+1)
        message = message.encode()
        self.sock.sendto(message,('0.0.0.0',31337))
        data, ip = self.sock.recvfrom(1024)
        print(data.decode())

        x.append(data.decode()) 
        y.append(data.decode())
        c += 1
        self.setData(x, y)


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
