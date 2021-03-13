from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import socket
import struct

class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #self.counter = 0
        #self.pack = struct.pack(">3c1i14f1I",b"C", b"2", b"H", 2, 10, 1,
                #1, 1.1, 1.1, 1.1 ,1.1,1.1,0)
        layout = QVBoxLayout()
        layout = QGridLayout()
        layout.setSpacing(10) 
        
        #self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)
        self.jam_pos_in_label = QLabel("jam_pos_in")
        self.jam_pos_in_box = QLineEdit('2')
        self.F_set_label = QLabel("F_set")
        self.F_set_box = QLineEdit('10')
        self.kShaker_label = QLabel("kShaker")
        self.kShaker_box = QLineEdit('1')
        self.shaker_freq_label = QLabel('shaker_freq')
        self.shaker_freq_box = QLineEdit('10')
        self.m_label = QLabel('m')
        self.m_box = QLineEdit('5')
        self.f_mode2_label = QLabel('f_mode2')
        self.f_mode2_box = QLineEdit('1.1')
        self.f_mode3_label = QLabel('f_mode3')
        self.f_mode3_box = QLineEdit('2.1')
        self.a_mode5_label = QLabel('a_mode5')
        self.a_mode5_box = QLineEdit('1.1')
        self.b_mode5_label = QLabel('b_mode5')
        self.b_mode5_box = QLineEdit('1.1')
        self.c_mode5_label = QLabel('c_mode5')
        self.c_mode5_box = QLineEdit('1.1')
        self.d_mode5_label = QLabel('d_mode5')
        self.d_mode5_box = QLineEdit('1.1')
        self.g_mode5_label = QLabel('g_mode5')
        self.g_mode5_box = QLineEdit('1.1')
        self.v_mode6_label = QLabel('v_mode6')
        self.v_mode6_box = QLineEdit('1.1')
        self.kD_mode6_label = QLabel('kD_mode6')
        self.kD_mode6_box = QLineEdit('1.1')
        self.pow_mode6_label = QLabel('pow_mode6')
        self.pow_mode6_box = QLineEdit('3')
        
        self.mode = QComboBox()
        self.mode.addItems(['1','2','3','4','5','6'])
 
        #layout.addWidget(self.lw)
        layout.addWidget(b,1,10)
        layout.addWidget(self.mode,20,20)
        layout.addWidget(self.jam_pos_in_label)
        layout.addWidget(self.jam_pos_in_box)
        layout.addWidget(self.F_set_label)
        layout.addWidget(self.F_set_box)
        layout.addWidget(self.kShaker_label)
        layout.addWidget(self.kShaker_box)
        layout.addWidget(self.shaker_freq_label)
        layout.addWidget(self.shaker_freq_box)
        layout.addWidget(self.m_label)
        layout.addWidget(self.m_box)
        layout.addWidget(self.f_mode2_label)
        layout.addWidget(self.f_mode2_box)
        layout.addWidget(self.f_mode3_label)
        layout.addWidget(self.f_mode3_box)
        layout.addWidget(self.a_mode5_label)
        layout.addWidget(self.a_mode5_box)
        layout.addWidget(self.b_mode5_label)
        layout.addWidget(self.b_mode5_box)
        layout.addWidget(self.c_mode5_label)
        layout.addWidget(self.c_mode5_box)
        layout.addWidget(self.d_mode5_label)
        layout.addWidget(self.d_mode5_box)
        layout.addWidget(self.g_mode5_label)
        layout.addWidget(self.g_mode5_box)
        layout.addWidget(self.v_mode6_label)
        layout.addWidget(self.v_mode6_box)
        layout.addWidget(self.kD_mode6_label)
        layout.addWidget(self.kD_mode6_box)
        layout.addWidget(self.pow_mode6_label)
        layout.addWidget(self.pow_mode6_box)

        w = QWidget()
        w.setLayout(layout)
    
        self.setCentralWidget(w)
    
        self.show()
        
        self.get_params()
        
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        #self.sock_send.sendto(self.pack,('127.0.0.1',5500))
    
    def get_params(self):
        mode = int(self.mode.currentText())
        jam_pos_in = float(self.jam_pos_in_box.text())
        F_set = float(self.F_set_box.text())
        kShaker = float(self.kShaker_box.text())
        shaker_freq = float(self.shaker_freq_box.text())
        m = float(self.m_box.text())
        f_mode2 = float(self.f_mode2_box.text())
        f_mode3 = float(self.f_mode3_box.text())
        a_mode5 = float(self.a_mode5_box.text())
        b_mode5 = float(self.b_mode5_box.text())
        c_mode5 = float(self.c_mode5_box.text())
        d_mode5 = float(self.d_mode5_box.text())
        g_mode5 = float(self.g_mode5_box.text())
        v_mode6 = float(self.v_mode6_box.text())
        kD_mode6 = float(self.kD_mode6_box.text())
        pow_mode6 = int(self.pow_mode6_box.text())
        self.pack = struct.pack(">3c1i14f1I",b"C", b"2", b"H", mode, jam_pos_in,
                F_set, kShaker, shaker_freq, m, f_mode2 ,f_mode3,
                a_mode5, b_mode5, c_mode5, d_mode5, g_mode5, 
                v_mode6, kD_mode6, pow_mode6)
        

    def oh_no(self):
        self.get_params()

    


    def recurring_timer(self):
        #self.counter +=1
        self.sock_send.sendto(self.pack,('127.0.0.1',5500))
        #self.l.setText("Counter: %d" % self.counter)
    
    
app = QApplication([])
window = MainWindow()
app.exec_()
