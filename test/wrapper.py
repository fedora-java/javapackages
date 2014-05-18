import sys
import subprocess
import os
import textwrap
import re

if 'PYTHONPATH' in os.environ:
    PYTHONPATH = os.environ['PYTHONPATH'].split(':')
else:
    PYTHONPATH = "."

injected = textwrap.dedent("""\
        import sys as ____sys
        ____sys.path = ["{pythonpath}"] + ____sys.path
        """.format(pythonpath='" ,"'.join(PYTHONPATH)))

with open(sys.argv[1], 'r') as scriptfile:
    script = scriptfile.read().split('\n')

futures = [idx for idx, line in enumerate(script) if '__future__' in line]
index = futures[-1] if futures else 0
index += 1
script[index:index] = injected.split('\n')

if sys.argv[2]:
    config = sys.argv[2]
    script = [re.sub(r'(CONFIG_PATH\s*=\s*).*', r'\1"{0}"'.format(config), line)
             for line in script]

with open('.script.py', 'w') as newscript:
    newscript.write('\n'.join(script))

proc = subprocess.Popen([sys.executable, '.script.py'] + sys.argv[3:])
sys.exit(proc.wait())
