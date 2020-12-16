import os
from setuptools import setup, find_packages

dirpath = os.path.dirname(os.path.realpath(__file__))
versionpath = os.path.join(dirpath, "..", "VERSION")
moduleversion = os.path.join(dirpath, "javapackages", "version.py")
with open(versionpath) as vp:
    __version__ = vp.read().strip()
    with open(moduleversion, "w") as mv:
        mv.write("__version__ = '{v}'".format(v=__version__))

setup(
    name="javapackages",
    description="Module for handling, querying and manipulating of various "
                "files for Java packaging in Linux distributions",
    version=__version__,
    license="BSD",
    download_url="https://github.com/fedora-java/javapackages/releases",
    url="https://github.com/fedora-java/javapackages",
    packages=find_packages(exclude=["test"]),
    maintainer="javapackages maintainers",
    maintainer_email="javapackages-tools-owner@fedoraproject.org"
)
