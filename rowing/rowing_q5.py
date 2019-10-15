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
        #self.pack = struct.pack(">3c1i9f",b"C", b"2", b"H", 2, 10, 1,
        #        1, 1.1, 1.1, 1.1 ,1.1,1.1,0)
        self.pack = b'' 
        layout = QVBoxLayout()
        
        #self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)
        
        self.f_label = QLabel("f")
        self.f_box = QLineEdit('2')
        self.m_label = QLabel("m")
        self.m_box = QLineEdit('10')
        self.k0_label = QLabel("k0")
        self.k0_box = QLineEdit('1')
        self.k1_label = QLabel('k1')
        self.k1_box = QLineEdit('1')
        self.a_label = QLabel('a')
        self.a_box = QLineEdit('1.1')
        self.b_label = QLabel('b')
        self.b_box = QLineEdit('1.1')
        self.c_label = QLabel('c')
        self.c_box = QLineEdit('1.1')
        self.d_label = QLabel('d')
        self.d_box = QLineEdit('1.1')
        self.e_label = QLabel('e')
        self.e_box = QLineEdit('1.1')
        
        self.mode = QComboBox()
        self.mode.addItems(['0','1'])
 
        #layout.addWidget(self.lw)
        layout.addWidget(b)
        layout.addWidget(self.mode)
        layout.addWidget(self.f_label)
        layout.addWidget(self.f_box)
        layout.addWidget(self.m_label)
        layout.addWidget(self.m_box)
        layout.addWidget(self.k0_label)
        layout.addWidget(self.k0_box)
        layout.addWidget(self.k1_label)
        layout.addWidget(self.k1_box)
        layout.addWidget(self.a_label)
        layout.addWidget(self.a_box)
        layout.addWidget(self.b_label)
        layout.addWidget(self.b_box)
        layout.addWidget(self.c_label)
        layout.addWidget(self.c_box)
        layout.addWidget(self.d_label)
        layout.addWidget(self.d_box)
        layout.addWidget(self.e_label)
        layout.addWidget(self.e_box)
        #layout.addWidget(MyWidget())
        #self.sock_send.sendto(self.pack,('127.0.0.1',5500))

        w = QWidget()
        w.setLayout(layout)
    
        self.setCentralWidget(w)
    
        self.show()

        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        #self.sock_send.sendto(self.pack,('127.0.0.1',5500))
    


    def oh_no(self):
        #time.sleep(5)
        f = int(self.f_box.text())
        m = float(self.m_box.text())
        k0 = float(self.k0_box.text())
        k1 = float(self.k1_box.text())
        a = float(self.a_box.text())
        b = float(self.b_box.text())
        c = float(self.c_box.text())
        d = float(self.d_box.text())
        e = float(self.d_box.text())
        mode = float(self.mode.currentText())
        self.pack = struct.pack(">3c1i9f",b"C", b"2", b"H", f, m, 
                k0, k1, a, b, c, d, e, mode)
            
 
        #self.counter += textboxValue#20

    


    def recurring_timer(self):
        #self.counter +=1
        self.sock_send.sendto(self.pack,('127.0.0.1',5500))
        #self.l.setText("Counter: %d" % self.counter)
    
    
app = QApplication([])
window = MainWindow()
app.exec_()
