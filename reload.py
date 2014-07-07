import os
import os.path
import sys
import time
import subprocess

args = sys.argv[:]
this_script = args.pop(0)
target_script = args.pop(0)

if not os.path.isfile(target_script):
    print("Not a file: " + target_script)
    sys.exit(0)

def run():
    command = [sys.executable, target_script]
    command.extend(args)
    return subprocess.Popen(command)

class FakeProcess:
    def kill(self):
        pass

p = FakeProcess()
last_mtime = 0
while 1:
    mtime = os.stat(target_script).st_mtime
    
    if mtime != last_mtime:
        print("Modified - Re-running")
        last_mtime = mtime
        p.kill()
        p = run()
        
    time.sleep(1)
