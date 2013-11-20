import sys
import subprocess
import os

PYTHONPATH = os.environ['PYTHONPATH'].split(':')
script = 'import sys; sys.path=["{pythonpath}"]+sys.path;'.format(pythonpath=','.join(PYTHONPATH))
with open(sys.argv[1], 'r') as scriptfile:
    script += scriptfile.read()
with open('.script.py', 'w') as newscript:
    newscript.write(script)

proc = subprocess.Popen([sys.executable, '.script.py'] + sys.argv[2:])
sys.exit(proc.wait())
