    
import tkinter
import os
from PIL import ImageTk, Image
import socket
import struct


class UDP():
    """Velo control message class"""
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.UDP_IP = '127.0.0.1'
        self.UDP_PORT = 5500
        self.F_set = 500
        self.kShaker = 0.006
        self.shaker_freq = 10
        self.m_inner = 20
        self.kPedal = 5
        self.shaker_limit = 1
        self.friction = 5
        self.p_set = 60

    def send_message(self):
        
        pack = struct.pack(">3c8f", b"C", b"2", b"H", self.F_set, self.kShaker,
                self.shaker_freq, self.m_inner,self.kPedal, self.shaker_limit,
                self.friction, self.p_set)
    
        #pack = struct.pack(">3c8f", b"C", b"2", b"H", 500, 0.006, 20, 5, 1.1, 1, 5, 200000)
        err = self.sock.sendto(pack, (self.UDP_IP, self.UDP_PORT))
        print(err)

class App():
    def __init__(self,window, window_title):
        #UDP manager
        self.msg = UDP()
        
        #app window setup
        self.window = window
        self.window.title(window_title)
        self.window.geometry("450x500")
        
        #setup base geometry and visual params
        base_label_x = 10
        base_label_y = 50
        base_entry_x = 100
        base_entry_y = 50
        y_delta = 40
        x_delta = 250
        ent_w = 70 # entries width
        F_size = 12 # font size
        FONT = 'Courier'

        # label1
        self.label_1 = tkinter.Label(window,text = 'Velo module parameters')
        self.label_1.config(font = ('Helvetica 15 bold'))
        self.label_1.place(x = base_label_x + 70, y = base_label_y - y_delta)
        # label2
        #self.label_2 = tkinter.Label(window,text = 'Mode 5 parameters')
        #self.label_2.config(font = ('Helvetica 15 bold'))
        #self.label_2.place(x = base_label_x + x_delta, y = base_label_y - y_delta)
        
        #F-set label
        self.label_F_set = tkinter.Label(window,text = 'F-set')
        self.label_F_set.config(font = (FONT, F_size))
        self.label_F_set.place(x = base_label_x, y = base_label_y + y_delta)
        #F-set entry
        self.entry_F_set = tkinter.Entry(window)
        self.entry_F_set.insert(0,'400')
        self.entry_F_set.config(font = (FONT, F_size))
        self.entry_F_set.place(x = base_entry_x, y = base_entry_y + y_delta, width = ent_w)        

        #kShaker label
        self.label_kShaker = tkinter.Label(window,text = 'kShaker')
        self.label_kShaker.config(font = (FONT,F_size))
        self.label_kShaker.place(x = base_label_x, y = base_label_y + y_delta * 2)
        #kShaker entry
        self.entry_kShaker = tkinter.Entry(window)
        self.entry_kShaker.insert(0,'0.006')
        self.entry_kShaker.config(font = (FONT, F_size))
        self.entry_kShaker.place(x = base_entry_x, y = base_entry_y + y_delta * 2, width = ent_w)

        #shaker freq
        self.label_shaker_freq = tkinter.Label(window,text = 'Shaker f.')
        self.label_shaker_freq.config(font = (FONT,F_size))
        self.label_shaker_freq.place(x = base_label_x, y = base_label_y + y_delta * 3)
        #shaker freq entry
        self.entry_shaker_freq = tkinter.Entry(window)
        self.entry_shaker_freq.insert(0,'10')
        self.entry_shaker_freq.config(font = (FONT, F_size))
        self.entry_shaker_freq.place(x = base_entry_x, y = base_entry_y + y_delta * 3, width = ent_w)
        
        
        #m_inner label
        self.label_m_inner = tkinter.Label(window,text = 'Inertia')
        self.label_m_inner.config(font = (FONT,F_size))
        self.label_m_inner.place(x = base_label_x, y = base_label_y + y_delta * 4)
        #m_inner entry
        self.entry_m_inner = tkinter.Entry(window)
        self.entry_m_inner.insert(0,'20')
        self.entry_m_inner.config(font = (FONT, F_size))
        self.entry_m_inner.place(x = base_entry_x, y = base_entry_y + y_delta * 4, width = ent_w)
        
        #kPedal label
        self.label_kPedal = tkinter.Label(window,text = 'kPedal')
        self.label_kPedal.config(font = (FONT, F_size))
        self.label_kPedal.place(x = base_label_x + x_delta, y = base_label_y + y_delta)
        #kPeadl entry
        self.entry_kPedal = tkinter.Entry(window)
        self.entry_kPedal.insert(0,'1.1')
        self.entry_kPedal.config(font = (FONT, F_size))
        self.entry_kPedal.place(x = base_entry_x + x_delta, y = base_entry_y + y_delta, width = ent_w)
        
        #shaker_limit label
        self.label_shaker_limit = tkinter.Label(window,text = 'Shaker lim')
        self.label_shaker_limit.config(font = (FONT, F_size))
        self.label_shaker_limit.place(x = base_label_x + x_delta, y = base_label_y + y_delta*2)
        #shaker_limit entry
        self.entry_shaker_limit = tkinter.Entry(window)
        self.entry_shaker_limit.insert(0,'1')
        self.entry_shaker_limit.config(font = (FONT, F_size))
        self.entry_shaker_limit.place(x = base_entry_x + x_delta, y = base_entry_y + y_delta*2, width = ent_w)

        #friction label
        self.label_friction = tkinter.Label(window,text = 'Friction')
        self.label_friction.config(font = (FONT, F_size))
        self.label_friction.place(x = base_label_x + x_delta, y = base_label_y + y_delta*3)
        #friction entry
        self.entry_friction = tkinter.Entry(window)
        self.entry_friction.insert(0,'5')
        self.entry_friction.config(font = (FONT, F_size))
        self.entry_friction.place(x = base_entry_x + x_delta, y = base_entry_y + y_delta*3, width = ent_w)

        #p_set label
        self.label_p_set = tkinter.Label(window,text = 'p_set')
        self.label_p_set.config(font = (FONT, F_size))
        self.label_p_set.place(x = base_label_x + x_delta, y = base_label_y + y_delta*4)
        #p_set entry
        self.entry_p_set = tkinter.Entry(window)
        self.entry_p_set.insert(0,'60')
        self.entry_p_set.config(font = (FONT, F_size))
        self.entry_p_set.place(x = base_entry_x + x_delta, y = base_entry_y + y_delta*4, width = ent_w)


        #set button
        self.btn_set = tkinter.Button(window, text = 'Set parameters', command = self.act_set)
        self.btn_set.config(font = (FONT,F_size))
        self.btn_set.place(x = 85, y = 420)
        
        #call event loop
        self.window.mainloop()

    
    #button action
    def act_set(self):
        
        self.get_entries_data()
        self.msg.send_message()
    
    #collect data from entries to UDP attributes
    def get_entries_data(self):
        self.msg.F_set = float(self.entry_F_set.get())
        self.msg.kShaker = float(self.entry_kShaker.get())
        self.msg.shaker_freq = float(self.entry_shaker_freq.get())
        self.msg.m_inner = float(self.entry_m_inner.get())
        self.msg.kPedal = float(self.entry_kPedal.get())
        self.msg.shaker_limit = float(self.entry_shaker_limit.get())
        self.msg.friction = float(self.entry_friction.get())
        self.msg.p_set =  float(self.entry_p_set.get())



if __name__ == "__main__":
    App(tkinter.Tk(),"Velo test")
