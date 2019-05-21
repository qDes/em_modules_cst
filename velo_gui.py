    
import tkinter
import os
from PIL import ImageTk, Image

class UDP():
    def __init__(self):
        pass

    def send_message(self):
        pass

class App():
    def __init__(self,window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("850x500")
        
        base_label_x = 10
        base_label_y = 50
        base_entry_x = 95
        base_entry_y = 50
        y_delta = 40
        x_delta = 250
        ent_w = 60 # entries width
        F_size = 14 # font size
        FONT = 'Courier'

        # label1
        self.label_1 = tkinter.Label(window,text = 'Velo module parameters')
        self.label_1.config(font = ('Helvetica 15 bold'))
        self.label_1.place(x = base_label_x + 200, y = base_label_y - y_delta)
        # label2
        #self.label_2 = tkinter.Label(window,text = 'Mode 5 parameters')
        #self.label_2.config(font = ('Helvetica 15 bold'))
        #self.label_2.place(x = base_label_x + x_delta, y = base_label_y - y_delta)
        
        #F-set label
        self.label_mass = tkinter.Label(window,text = 'F-set')
        self.label_mass.config(font = (FONT, F_size))
        self.label_mass.place(x = base_label_x, y = base_label_y + y_delta)
        #F-set entry
        self.entry_mass = tkinter.Entry(window)
        self.entry_mass.insert(0,'400')
        self.entry_mass.config(font = (FONT, F_size))
        self.entry_mass.place(x = base_entry_x, y = base_entry_y + y_delta, width = ent_w)        

        self.window.mainloop()



if __name__ == "__main__":
    App(tkinter.Tk(),"Velo test")
