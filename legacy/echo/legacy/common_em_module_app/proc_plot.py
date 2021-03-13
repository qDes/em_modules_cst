import subprocess
import matplotlib.pyplot as plt


plt.ion()
samp = []
cnt = 10
def plotN():
    plt.clf()
    #plt.ylim(0,0.5)
    plt.title('Hui v rot test')
    plt.grid(True)
    plt.ylabel('Hui')
    plt.plot(samp, 'rx-', label='rot')
    plt.legend(loc='Hui v rot')
    plt.plot(samp)
    plt.show()

cmd = ['top']

process = subprocess.Popen(cmd, shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE)

for line in process.stdout:
    l = line.decode('utf-8').split()
    #print(l)
    try:
        
        if l[2] == 'qdes':
            
            print('Find qdes process!' +' CPU '+ l[9] + '%')
            c = '.'.join(l[9].split(','))
            c = float(c)
            if len(samp) > cnt:
                samp.append(c)
                samp.pop(0)
            else:
                samp.append(c)
            plotN()
            plt.pause(.05)
    except IndexError:
        pass

erccode = process.returncode
