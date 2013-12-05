# this will be replaced during setup.py build
import os
dirpath = os.path.dirname(os.path.realpath(__file__))
versionpath = os.path.join(dirpath, '..', '..', 'VERSION')
with open(versionpath) as vp:
        __version__ = vp.read().strip()
