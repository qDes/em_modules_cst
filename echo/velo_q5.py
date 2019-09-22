from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import socket

class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.counter = 0
    
        layout = QVBoxLayout()
        
        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)
        
        self.textbox = QLineEdit(self)


        layout.addWidget(self.l)
        layout.addWidget(b)
        layout.addWidget(self.textbox)

        w = QWidget()
        w.setLayout(layout)
    
        self.setCentralWidget(w)
    
        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
    

    def oh_no(self):
        #time.sleep(5)
        textboxValue = int(self.textbox.text())
        self.counter += textboxValue#20

    def recurring_timer(self):
        self.counter +=1
        self.sock_send.sendto(str(self.counter).encode(encoding='utf-8'),('127.0.0.1',5500))
        self.l.setText("Counter: %d" % self.counter)
    
    
app = QApplication([])
window = MainWindow()
app.exec_()
