from threading import Thread
import time
import os


def startprgm(i):
    print( "Running thread %d" % i)
    if (i == 0):
        time.sleep(1)
        print('Running: gui_1.py')
        os.system("python gui_1.py")
    elif (i == 1):
        print('Running: proc_plot.py')
        time.sleep(1)
        os.system("python proc_plot.py")
    else:
        pass

for i in range(2):
    t = Thread(target=startprgm, args=(i,))
    t.start()
