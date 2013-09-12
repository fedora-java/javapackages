import sys
import subprocess

proc = subprocess.Popen([sys.executable, sys.argv[1]] + sys.argv[2:])
sys.exit(proc.wait())
