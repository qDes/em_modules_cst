#  . /home/lar/linuxcnc-dev/scripts/rip-environment

import subprocess
import shlex
import time
from datetime import datetime

ps_com = 'halcmd show all inner-loop-paddle.0.*'

def get_hal_value(val: str, proc_stdout: bytes) -> str:
    command = f'grep inner-loop-paddle.0.{val}'
    proc_a = subprocess.Popen(shlex.split(command), 
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE)
    proc_a.stdin.write(proc_stdout)
    value = str(proc_a.communicate()[0]).split()[4]
    return value



if __name__=="__main__":
    with open('kF.txt','a') as writefile:
        while True:
            proc_ps = subprocess.Popen(shlex.split(ps_com), stdout=subprocess.PIPE)
            stdout_ps = proc_ps.communicate()[0]
            
            a = get_hal_value('a', stdout_ps)
            F_act = get_hal_value('F-act', stdout_ps)
            p = get_hal_value('p', stdout_ps)
            p_err = get_hal_value('F-act', stdout_ps)
            print(a, F_act)
            now = datetime.now() 
            #to_file = f"{kF} {kV} {kA} {kP} {F_act} {a} {p} {p_err} {now}"
            to_file = f"F_act = {F_act} a={a} p={p} p_err={p_err} {now}"
            print(to_file)
            time.sleep(1)
            #writefile.write(to_file)
