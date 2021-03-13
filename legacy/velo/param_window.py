from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from dataclasses import dataclass

import dataclasses
import time
import socket
import struct

from plotting_udp import MyWidget


@dataclass
class VeloParams:
    f_set:        float
    kShaker:      float
    shaker_freq:  float
    m_inner:      float
    kPedal:       float
    shaker_limit: float
    friction:     float
    p_set:        float
    calib:        float

    def update(self, f_set, kShaker,
            shaker_freq, m_inner, kPedal,
            shaker_limit, friction,
            p_set, calib):
        self.f_set = f_set
        self.kShaker = kShaker
        self.shaker_limit = shaker_limit
        self.friction=friction
        self.p_set = self.p_set
        self.calib = self.calib

class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        layout = QVBoxLayout()
        
        #self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.press_button)
        
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
        self.calib_label = QLabel('calib')
        self.calib_box = QLineEdit('0')

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
        layout.addWidget(self.calib_label)
        layout.addWidget(self.calib_box)
        
        #layout.addWidget(MyWidget())
        #self.sock_send.sendto(self.pack,('127.0.0.1',5500))
        

        self.params = VeloParams(0,0,0,0,0,0,0,0,0)
        w = QWidget()
        w.setLayout(layout)
    
        self.setCentralWidget(w)
    
        self.show()
    

        self.get_params()
        '''
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        '''
        
    

    def get_params(self):
        f_set = float(self.f_set_box.text())
        kShaker = float(self.kShaker_box.text())
        shaker_freq = float(self.shaker_freq_box.text())
        m = float(self.m_box.text())
        kPedal = float(self.kPedal_box.text())
        shaker_limit = float(self.shaker_limit_box.text())
        friction = float(self.friction_box.text())
        p_set = float(self.p_set_box.text())
        calib = float(self.calib_box.text())
        self.params.update(f_set=f_set, kShaker=kShaker,
                shaker_freq=shaker_freq, m_inner=m,
                kPedal=kPedal, shaker_limit=shaker_limit,
                p_set=p_set, calib=calib, friction=friction)
        self.pack = struct.pack(">3c9f",b"C", b"2", b"H", f_set, kShaker, 
                shaker_freq, m, kPedal, shaker_limit, friction,
                p_set, calib)
 
    def press_button(self):
        #time.sleep(5
        print("pressed")
        print(dataclasses.asdict(self.params))
        print(self.params)
        self.get_params()
        #self.counter += textboxValue#20

    '''
    def recurring_timer(self):
        #self.counter +=1
        self.sock_send.sendto(self.pack,('192.168.0.102',5500))
        #self.l.setText("Counter: %d" % self.counter)
    '''
    
    
app = QApplication([])
window = MainWindow()
app.exec_()
