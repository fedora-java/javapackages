import sys
import subprocess
import os
import re

with open(sys.argv[1], 'r') as scriptfile:
    script = scriptfile.read().split('\n')

if sys.argv[2]:
    config = sys.argv[2]
    script = [re.sub(r'%{javaconfdir}', config, line)
             for line in script]

with open('.script.py', 'w') as newscript:
    newscript.write('\n'.join(script))

proc = subprocess.Popen([sys.executable, '.script.py'] + sys.argv[3:])
sys.exit(proc.wait())
