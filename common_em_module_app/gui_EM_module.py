import tkinter
import os
from PIL import ImageTk, Image

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
        self.label_1 = tkinter.Label(window,text = 'Main parameters')
        self.label_1.config(font = ('Helvetica 15 bold'))
        self.label_1.place(x = base_label_x, y = base_label_y - y_delta)
        # label2
        self.label_2 = tkinter.Label(window,text = 'Mode 5 parameters')
        self.label_2.config(font = ('Helvetica 15 bold'))
        self.label_2.place(x = base_label_x + x_delta, y = base_label_y - y_delta)
        
        #listbox
        self.listbox = tkinter.Listbox(window)
        for i in range(6):
            self.listbox.insert(tkinter.END, str(i+1))
        self.listbox.config(font = (FONT,F_size))
        self.listbox.place(x = base_entry_x, y = base_entry_y, width = ent_w,height = 25)
        #listboxlabel
        self.label_list = tkinter.Label(window, text = 'Mode')
        self.label_list.config(font = (FONT,F_size))
        self.label_list.place(x = base_label_x, y = base_label_y)
        
        #mass label
        self.label_mass = tkinter.Label(window,text = 'Mass')
        self.label_mass.config(font = (FONT, F_size))
        self.label_mass.place(x = base_label_x, y = base_label_y + y_delta)
        #mass entry
        self.entry_mass = tkinter.Entry(window)
        self.entry_mass.insert(0,'8')
        self.entry_mass.config(font = (FONT, F_size))
        self.entry_mass.place(x = base_entry_x, y = base_entry_y + y_delta, width = ent_w)

        #F_set label
        self.label_f = tkinter.Label(window,text = 'F-set')
        self.label_f.config(font = (FONT,F_size))
        self.label_f.place(x = base_label_x, y = base_label_y + y_delta * 2)
        #F_set entry
        self.entry_f = tkinter.Entry(window)
        self.entry_f.insert(0,'40')
        self.entry_f.config(font = (FONT, F_size))
        self.entry_f.place(x = base_entry_x, y = base_entry_y + y_delta * 2, width = ent_w)

        #kShaker label
        self.label_shaker = tkinter.Label(window,text = 'f-mode2')
        self.label_shaker.config(font = (FONT,F_size))
        self.label_shaker.place(x = base_label_x, y = base_label_y + y_delta * 3)
        #kShker entry
        self.entry_shaker = tkinter.Entry(window)
        self.entry_shaker.insert(0,'15.1')
        self.entry_shaker.config(font = (FONT, F_size))
        self.entry_shaker.place(x = base_entry_x, y = base_entry_y + y_delta * 3, width = ent_w)

        #pow-mode6 label
        self.label_pow6 = tkinter.Label(window,text = 'pow-m6')
        self.label_pow6.config(font = (FONT,F_size))
        self.label_pow6.place(x = base_label_x, y = base_label_y + y_delta * 4)
        #pow-mode6 entry
        self.entry_pow6 = tkinter.Entry(window)
        self.entry_pow6.insert(0,'10')
        self.entry_pow6.config(font = (FONT, F_size))
        self.entry_pow6.place(x = base_entry_x, y = base_entry_y + y_delta * 4, width = ent_w)


        #mode5 a lable
        self.label_a5 = tkinter.Label(window,text = 'a')
        self.label_a5.config(font = (FONT, F_size))
        self.label_a5.place(x = base_label_x + x_delta, y = base_label_y )
        #mode 5 a entry
        self.entry_a5 = tkinter.Entry(window)
        self.entry_a5.insert(0,'1')
        self.entry_a5.config(font = (FONT, F_size))
        self.entry_a5.place(x = base_entry_x + x_delta - 40, y = base_entry_y, width = ent_w)
        
        #mode5 b lable
        self.label_b5 = tkinter.Label(window,text = 'b')
        self.label_b5.config(font = (FONT, F_size))
        self.label_b5.place(x = base_label_x + x_delta, y = base_label_y + y_delta )
        #mode b a entry
        self.entry_b5 = tkinter.Entry(window)
        self.entry_b5.insert(0,'2')
        self.entry_b5.config(font = (FONT, F_size))
        self.entry_b5.place(x = base_entry_x + x_delta - 40, y = base_entry_y + y_delta, width = ent_w)

        #mode5 c lable
        self.label_c5 = tkinter.Label(window,text = 'c')
        self.label_c5.config(font = (FONT, F_size))
        self.label_c5.place(x = base_label_x + x_delta, y = base_label_y + y_delta * 2 )
        #mode 5 c entry
        self.entry_c5 = tkinter.Entry(window)
        self.entry_c5.insert(0,'3')
        self.entry_c5.config(font = (FONT, F_size))
        self.entry_c5.place(x = base_entry_x + x_delta - 40, y = base_entry_y + y_delta *2, width = ent_w)

        #mode5 d lable
        self.label_d5 = tkinter.Label(window,text = 'd')
        self.label_d5.config(font = (FONT, F_size))
        self.label_d5.place(x = base_label_x + x_delta, y = base_label_y + y_delta * 3 )
        #mode 5 d entry
        self.entry_d5 = tkinter.Entry(window)
        self.entry_d5.insert(0,'4')
        self.entry_d5.config(font = (FONT, F_size))
        self.entry_d5.place(x = base_entry_x + x_delta - 40, y = base_entry_y + y_delta *3, width = ent_w)

        #mode5 g lable
        self.label_g5 = tkinter.Label(window,text = 'g')
        self.label_g5.config(font = (FONT, F_size))
        self.label_g5.place(x = base_label_x + x_delta, y = base_label_y + y_delta * 4 )
        #mode 5 g entry
        self.entry_g5 = tkinter.Entry(window)
        self.entry_g5.insert(0,'5')
        self.entry_g5.config(font = (FONT, F_size))
        self.entry_g5.place(x = base_entry_x + x_delta - 40, y = base_entry_y + y_delta * 4, width = ent_w)

        img = ImageTk.PhotoImage(Image.open('formulas.jpeg').resize((400,300)))
        self.label_pic = tkinter.Label(window, image = img)
        self.label_pic.place(x= 400, y = 40)

 
        #set button
        self.btn_set = tkinter.Button(window, text = 'Set parameters', command = self.act_set)
        self.btn_set.config(font = (FONT,F_size))
        self.btn_set.place(x = 85, y = 420)
        



        self.sasi()
        self.window.mainloop()
      
    def sasi(self):
        self.entry_mass.config({"background":"White"})
        self.entry_a5.config({"background":"Gray"})
        self.entry_b5.config({"background":"Gray"})
        self.entry_c5.config({"background":"Gray"})
        self.entry_d5.config({"background":"Gray"})
        self.entry_g5.config({"background":"Gray"})
        self.entry_f.config({"background":"Gray"})
        self.entry_shaker.config({"background":"Gray"})
        self.entry_pow6.config({"background":"Gray"})



    def act_set(self):
        m = self.entry_mass.get()
        mode = self.listbox.get(tkinter.ACTIVE)
        f_s = self.entry_f.get()
        f_mode2 = self.entry_shaker.get()
        pow6 = self.entry_pow6.get()
        a5 = self.entry_a5.get()
        b5 = self.entry_b5.get()
        c5 = self.entry_c5.get()
        d5 = self.entry_d5.get()
        g5 = self.entry_g5.get()
        if mode == '1':
            self.entry_mass.config({"background":"White"})
            self.entry_a5.config({"background":"Gray"})
            self.entry_b5.config({"background":"Gray"})
            self.entry_c5.config({"background":"Gray"})
            self.entry_d5.config({"background":"Gray"})
            self.entry_g5.config({"background":"Gray"})
            self.entry_f.config({"background":"Gray"})
            self.entry_shaker.config({"background":"Gray"})
            self.entry_pow6.config({"background":"Gray"})
        if mode == '2':
            self.entry_mass.config({"background":"Gray"})
            self.entry_a5.config({"background":"Gray"})
            self.entry_b5.config({"background":"Gray"})
            self.entry_c5.config({"background":"Gray"})
            self.entry_d5.config({"background":"Gray"})
            self.entry_g5.config({"background":"Gray"})
            self.entry_f.config({"background":"White"})
            self.entry_shaker.config({"background":"White"})
            self.entry_pow6.config({"background":"Gray"})
        if mode == '3':
            self.entry_mass.config({"background":"Gray"})
            self.entry_a5.config({"background":"Gray"})
            self.entry_b5.config({"background":"Gray"})
            self.entry_c5.config({"background":"Gray"})
            self.entry_d5.config({"background":"Gray"})
            self.entry_g5.config({"background":"Gray"})
            self.entry_f.config({"background":"White"})
            self.entry_shaker.config({"background":"White"})
            self.entry_pow6.config({"background":"Gray"})
        if mode == '4':
            self.entry_mass.config({"background":"Gray"})
            self.entry_a5.config({"background":"Gray"})
            self.entry_b5.config({"background":"Gray"})
            self.entry_c5.config({"background":"Gray"})
            self.entry_d5.config({"background":"Gray"})
            self.entry_g5.config({"background":"Gray"})
            self.entry_f.config({"background":"White"})
            self.entry_shaker.config({"background":"White"})
            self.entry_pow6.config({"background":"Gray"})
        if mode == '5':
            self.entry_mass.config({"background":"Gray"})
            self.entry_a5.config({"background":"White"})
            self.entry_b5.config({"background":"White"})
            self.entry_c5.config({"background":"White"})
            self.entry_d5.config({"background":"White"})
            self.entry_g5.config({"background":"White"})
            self.entry_f.config({"background":"Gray"})
            self.entry_shaker.config({"background":"Gray"})
            self.entry_pow6.config({"background":"Gray"})
        if mode == '6':
            self.entry_mass.config({"background":"Gray"})
            self.entry_a5.config({"background":"Gray"})
            self.entry_b5.config({"background":"Gray"})
            self.entry_c5.config({"background":"Gray"})
            self.entry_d5.config({"background":"Gray"})
            self.entry_g5.config({"background":"Gray"})
            self.entry_f.config({"background":"Gray"})
            self.entry_shaker.config({"background":"Gray"})
            self.entry_pow6.config({"background":"White"})
        

        
        self.setp(m,mode,f_s, f_mode2,pow6,a5,b5,c5,d5,g5)

    def setp(self,m1,mode1,f_s,f_mode2, pow6, a5, b5, c5, d5, g5):
        cmd = []
        cmd.append('halcmd setp cls-train.0.m ' + m1)
        cmd.append('halcmd setp cls-train.0.mode ' + mode1)
        cmd.append('halcmd setp cls-train.0.F-set ' + f_s)
        cmd.append('halcmd setp cls-train.0.f-mode2 ' + f_mode2)
        cmd.append('halcmd setp cls-train.0.pow-mode6 '+ pow6)
        cmd.append('halcmd setp cls-train.0.a-mode5 ' + a5)
        cmd.append('halcmd setp cls-train.0.b-mode5 ' + b5)
        cmd.append('halcmd setp cls-train.0.c-mode5 ' + c5)
        cmd.append('halcmd setp cls-train.0.d-mode5 ' + d5)
        cmd.append('halcmd setp cls-train.0.g-mode5 ' + g5)


        for i in cmd:
            #print(i)
            os.system(i)
        print('')



if __name__ == "__main__":
    App(tkinter.Tk(),"Linear test")
