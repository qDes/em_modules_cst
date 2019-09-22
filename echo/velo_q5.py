from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import socket
import struct

from plotting_udp import MyWidget

class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #self.counter = 0
        self.pack = struct.pack(">3c8f",b"C", b"2", b"H", 20, 0.006, 10,
                20, 1.1, 1, 5 ,60)
        layout = QVBoxLayout()
        
        #self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)
        
        self.f_set_label = QLabel("F-set")
        self.f_set_box = QLineEdit('20')
        self.kShaker_label = QLabel("kShaker")
        self.kShaker_box = QLineEdit('0.006')
        self.shaker_freq_label = QLabel("shaker_freq")
        self.shaker_freq_box = QLineEdit('10')
        self.m_label = QLabel('m-inner')
        self.m_box = QLineEdit('20')
        self.kPedal_label = QLabel('kPedal')
        self.kPedal_box = QLineEdit('1.1')
        self.shaker_limit_label = QLabel('shaker limit')
        self.shaker_limit_box = QLineEdit('1')
        self.friction_label = QLabel('friction')
        self.friction_box = QLineEdit('5')
        self.p_set_label = QLabel('p-set')
        self.p_set_box = QLineEdit('60')
        

        #layout.addWidget(self.l)
        layout.addWidget(b)
        
        layout.addWidget(self.f_set_label)
        layout.addWidget(self.f_set_box)
        layout.addWidget(self.kShaker_label)
        layout.addWidget(self.kShaker_box)
        layout.addWidget(self.shaker_freq_label)
        layout.addWidget(self.shaker_freq_box)
        layout.addWidget(self.m_label)
        layout.addWidget(self.m_box)
        layout.addWidget(self.kPedal_label)
        layout.addWidget(self.kPedal_box)
        layout.addWidget(self.shaker_limit_label)
        layout.addWidget(self.shaker_limit_box)
        layout.addWidget(self.friction_label)
        layout.addWidget(self.friction_box)
        layout.addWidget(self.p_set_label)
        layout.addWidget(self.p_set_box)
        
        #layout.addWidget(MyWidget())
        #self.sock_send.sendto(self.pack,('127.0.0.1',5500))

        w = QWidget()
        w.setLayout(layout)
    
        self.setCentralWidget(w)
    
        self.show()

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        #self.sock_send.sendto(self.pack,('127.0.0.1',5500))
    


    def oh_no(self):
        #time.sleep(5)
        f_set = float(self.f_set_box.text())
        kShaker = float(self.kShaker_box.text())
        shaker_freq = float(self.shaker_freq_box.text())
        m = float(self.m_box.text())
        kPedal = float(self.kPedal_box.text())
        shaker_limit = float(self.shaker_limit_box.text())
        friction = float(self.friction_box.text())
        p_set = float(self.p_set_box.text())
        self.pack = struct.pack(">3c8f",b"C", b"2", b"H", f_set, kShaker, 
                shaker_freq, m, kPedal, shaker_limit, friction,
                p_set)
 
        #self.counter += textboxValue#20

    


    def recurring_timer(self):
        #self.counter +=1
        self.sock_send.sendto(self.pack,('127.0.0.1',5500))
        #self.l.setText("Counter: %d" % self.counter)
    
    
app = QApplication([])
window = MainWindow()
app.exec_()
