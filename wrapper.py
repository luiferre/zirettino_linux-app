import subprocess
import os
import signal
import time

command = [
    '/bin/python3',
    'ZIRE_app.py',
    '-start',
    '-ip',
    '192.168.102.16',
    '-name',
    '/home/utente/projects/ZIRETTINO/LINUXAPP/runs_4',
    '-comment',
    'test_app',
    '-packets',
    '100'
]
process = subprocess.Popen(command)


# Ottieni il PID del processo
pid = process.pid
time.sleep(5)
os.kill(pid, signal.SIGKILL)
