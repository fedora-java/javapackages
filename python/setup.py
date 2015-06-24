import os
from setuptools import setup

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
    download_url="https://fedorahosted.org/released/javapackages/",
    url="https://git.fedorahosted.org/git/javapackages.git",
    packages=["javapackages", "javapackages.maven", "javapackages.metadata",
              "javapackages.xmvn", "javapackages.common", "javapackages.ivy",
              "javapackages.cache"],
    test_suite="test",
    maintainer="javapackages maintainers",
    maintainer_email="java-devel@lists.fedoraproject.org"
)
