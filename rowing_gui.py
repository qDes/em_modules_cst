    
import tkinter
import os
from PIL import ImageTk, Image
import socket
import struct


class UDP():
    """Rowing control message class"""
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.UDP_IP = '127.0.0.1'
        self.UDP_PORT = 5500
        self.f = 1
        self.m_inner = 20
        self.kOut_mode0 = 1
        self.kOut_mode1 = 1

    def send_message(self):
        
        pack = struct.pack(">3c4f", b"C", b"2", b"H", self.f, self.m_inner,
                self.kOut_mode0, self.kOut_mode1)
    
        #pack = struct.pack(">3c8f", b"C", b"2", b"H", 500, 0.006, 20, 5, 1.1, 1, 5, 200000)
        err = self.sock.sendto(pack, (self.UDP_IP, self.UDP_PORT))
        print(err)
    
    def send_recv_message(self):
        pack = struct.pack(">3c4f", b"C", b"2", b"H", self.f, self.m_inner,
                self.kOut_mode0, self.kOut_mode1)
    
        #pack = struct.pack(">3c8f", b"C", b"2", b"H", 500, 0.006, 20, 5, 1.1, 1, 5, 200000)
        err = self.sock.sendto(pack, (self.UDP_IP, self.UDP_PORT))
        p, addr = self.sock.recvfrom(2048)
        print(p)

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
        self.label_1 = tkinter.Label(window,text = 'Rowing module parameters')
        self.label_1.config(font = ('Helvetica 15 bold'))
        self.label_1.place(x = base_label_x + 70, y = base_label_y - y_delta)
        # label2
        #self.label_2 = tkinter.Label(window,text = 'Mode 5 parameters')
        #self.label_2.config(font = ('Helvetica 15 bold'))
        #self.label_2.place(x = base_label_x + x_delta, y = base_label_y - y_delta)
        
        #f label
        self.label_f = tkinter.Label(window,text = 'f')
        self.label_f.config(font = (FONT, F_size))
        self.label_f.place(x = base_label_x, y = base_label_y + y_delta)
        #f entry
        self.entry_f = tkinter.Entry(window)
        self.entry_f.insert(0,'1')
        self.entry_f.config(font = (FONT, F_size))
        self.entry_f.place(x = base_entry_x, y = base_entry_y + y_delta, width = ent_w)        

        #m_inner label
        self.label_m_inner = tkinter.Label(window,text = 'm_inner')
        self.label_m_inner.config(font = (FONT,F_size))
        self.label_m_inner.place(x = base_label_x, y = base_label_y + y_delta * 2)
        #m_inner entry
        self.entry_m_inner = tkinter.Entry(window)
        self.entry_m_inner.insert(0,'20')
        self.entry_m_inner.config(font = (FONT, F_size))
        self.entry_m_inner.place(x = base_entry_x, y = base_entry_y + y_delta * 2, width = ent_w)

        
        #kOut_mode0 label
        self.label_k0 = tkinter.Label(window,text = 'k0')
        self.label_k0.config(font = (FONT, F_size))
        self.label_k0.place(x = base_label_x + x_delta, y = base_label_y + y_delta)
        #kOut_mode0 entry
        self.entry_k0 = tkinter.Entry(window)
        self.entry_k0.insert(0,'1')
        self.entry_k0.config(font = (FONT, F_size))
        self.entry_k0.place(x = base_entry_x + x_delta, y = base_entry_y + y_delta, width = ent_w)
        
        #kOut_mode1 label
        self.label_shaker_k1 = tkinter.Label(window,text = 'k1')
        self.label_shaker_k1.config(font = (FONT, F_size))
        self.label_shaker_k1.place(x = base_label_x + x_delta, y = base_label_y + y_delta*2)
        #kOut_mode1 entry
        self.entry_k1 = tkinter.Entry(window)
        self.entry_k1.insert(0,'1')
        self.entry_k1.config(font = (FONT, F_size))
        self.entry_k1.place(x = base_entry_x + x_delta, y = base_entry_y + y_delta*2, width = ent_w)


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
        '''
        try:
            self.msg.send_recv_message()
        except:    
            self.msg.send_message()
        '''

    #collect data from entries to UDP attributes
    def get_entries_data(self):
        self.msg.f = float(self.entry_f.get())
        self.msg.m_inner = float(self.entry_m_inner.get())
        self.msg.kOut_mode0 = float(self.entry_k0.get())
        self.msg.kOut_mode1 =  float(self.entry_k1.get())



if __name__ == "__main__":
    App(tkinter.Tk(),"Rowing test")
