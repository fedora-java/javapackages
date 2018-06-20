import os
import re
import shutil
import subprocess
import sys
import unittest

from javapackages.metadata.metadata import Metadata
from javapackages.common import util
from os import path
from test_rpmbuild import Package
from xml_compare import compare_xml_files
from functools import wraps
from lxml import etree

DIRPATH = path.dirname(path.realpath(__file__))
SCRIPT_ENV = {
    'PATH': '{mock}:{real}'.format(mock=DIRPATH, real=os.environ['PATH']),
    'LC_ALL': 'C.UTF-8',
}

for var in ('PYTHONPATH', 'COVERAGE_PROCESS_START'):
    if var in os.environ:
        SCRIPT_ENV[var] = os.environ[var]


def call_script(name, args, stdin=None, extra_env={}, wait=True):
    with open("tmpout", 'w') as outfile:
        with open("tmperr", 'w') as errfile:
            procargs = [sys.executable, name]
            env = SCRIPT_ENV.copy()
            env.update(extra_env)
            proc = subprocess.Popen(procargs + args, shell=False,
                                    stdout=outfile,
                                    stderr=errfile,
                                    env=env,
                                    stdin=subprocess.PIPE,
                                    universal_newlines=True)
            if not wait:
                return (outfile, errfile, proc)
            proc.communicate(stdin)
            ret = proc.wait()
    with open("tmpout", 'r') as outfile:
        out = outfile.read()
    with open("tmperr", 'r') as errfile:
        err = errfile.read()
    os.remove('tmpout')
    os.remove('tmperr')
    return (out, err, ret)


def get_config_file_list():
    try:
        return os.listdir('.xmvn/config.d/')
    except OSError:
        return []

def get_actual_config(filename):
    return path.join('.xmvn', 'config.d', filename)

def get_expected_config(filename, scriptname, testname):
    fileno = re.findall('[0-9]+', filename)
    if fileno:
        expfname = '{name}_{idx}.xml'.format(name=testname, idx=fileno[-1])
    else:
        expfname = filename
    return path.join(DIRPATH, 'data', scriptname, expfname)


def get_actual_args():
    with open('.xmvn/out', 'r') as f:
        args = f.read()
    return args


def get_expected_args(scriptname, testname):
    fpath = path.join(DIRPATH, 'data', scriptname, "{name}_out".format(name=testname))
    with open(fpath, 'r') as f:
        args = f.read()
    return args


def preload_xmvn_config(name, filename, dstname=None, update_index=False):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            src = path.join(DIRPATH, 'data', name, filename)
            os.mkdir('.xmvn')
            os.mkdir('.xmvn/config.d')
            dst = path.join('.xmvn', 'config.d', dstname or filename)
            shutil.copy(src, dst)
            if update_index:
                idx = 1
                if path.exists('.xmvn/javapackages-rule-index'):
                    with open('.xmvn/javapackages-rule-index', 'r') as index:
                        idx = int(index.read())
                with open('.xmvn/javapackages-rule-index', 'w') as index:
                    index.write(str(idx))
            fun(self)
        return test_decorated
    return test_decorator


def prepare_metadata(metadata_dir):
    for dirname, dirnames, filenames in os.walk(metadata_dir):
        for filename in filenames:
            if filename.endswith("-want.xml"):
                want_file = os.path.join(dirname, filename)
                xml = etree.parse(want_file)
                for path in xml.xpath('//*[local-name()="path"]'):
                    if '%' in path.text:
                        path.text = path.text % (metadata_dir)
                xml.write(want_file)


def javautils_script(name, fnargs):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            scriptpath = path.join(DIRPATH, '..', 'java-utils', name + '.py')
            (stdout, stderr, return_value) = call_script(scriptpath, fnargs)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator


def bindir_script(name, fnargs):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            scriptpath = path.join(DIRPATH, '..', 'bin', name)
            (stdout, stderr, return_value) = call_script(scriptpath, fnargs)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator


def call_rpmgen(rpmgen_name, filelist_prefix, filelist, env=None,
                config=''):
    scriptpath = path.join(DIRPATH, '..', 'depgenerators', rpmgen_name)
    stdin = []
    if not filelist:
        filelist = ["/dev/null"]

    if filelist_prefix:
        stdin.extend([os.path.abspath(os.path.join(filelist_prefix, x))
                     for x in filelist])
    else:
        stdin = filelist

    if not env:
        env = {}

    buildroot = "/dev/null"
    if "RPM_BUILD_ROOT" not in env and stdin:
        result = re.match(".*?/buildroot/", stdin[0])
        if result:
            buildroot = os.path.abspath(result.group(0))
    env.update({"RPM_BUILD_ROOT": buildroot})

    try:
        shutil.rmtree("/tmp/.javapackages_cache/")
    except OSError:
        pass
    for line in stdin:
        # FIXME this PID is a temporary hack
        ret = call_script(scriptpath, ["--cachedir", "/tmp", "--rpm-pid", "1"],
                          stdin=line, extra_env=env)
    try:
        shutil.rmtree("/tmp/.javapackages_cache/")
    except OSError:
        pass
    return ret


def osgiprov(*args, **kwargs):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            (stdout, stderr, return_value) = call_rpmgen("osgi.prov",
                                                         "data/osgi/",
                                                         *args, **kwargs)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator


def osgireq(*args, **kwargs):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            (stdout, stderr, return_value) = call_rpmgen("osgi.req",
                                                         "data/osgi/",
                                                         *args, **kwargs)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator


def mavenprov(*args, **kwargs):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            (stdout, stderr, return_value) = call_rpmgen("maven.prov",
                                                         "metadata/",
                                                         *args, **kwargs)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator


def mavenreq(*args, **kwargs):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            pargs, pkwargs = rpmgen_process_args(args, kwargs)
            (stdout, stderr, return_value) = call_rpmgen("maven.req",
                                                         "metadata/",
                                                         *pargs,
                                                         **pkwargs)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator


def javadocreq(*args, **kwargs):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            pargs, pkwargs = rpmgen_process_args(args, kwargs)
            (stdout, stderr, return_value) = call_rpmgen("javadoc.req",
                                                         "",
                                                         *pargs,
                                                         **pkwargs)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator


def rpmgen_process_args(args, kwargs):
    if "javaconfdirs" in kwargs:
        confdirs = [os.path.join(DIRPATH, "data", "config", conf) for conf in kwargs["javaconfdirs"]]
        try:
            env = kwargs["env"]
        except KeyError:
            env = {}
        env.update({"JAVACONFDIRS": os.pathsep.join(confdirs)})
        kwargs.update({"env": env})
        del kwargs["javaconfdirs"]
    else:
        env = {}
        env.update({"JAVACONFDIRS": os.path.abspath(os.path.join(DIRPATH, '..', 'etc'))})
        kwargs.update({"env": env})

    if "xmvnresolve_output" in kwargs:
        dest = "/tmp/"
        src = os.path.abspath(os.path.join("resolve", kwargs["xmvnresolve_output"]))
        shutil.copy(src, dest)
        try:
            env = kwargs["env"]
        except KeyError:
            env = {}
        env.update({"JAVAPACKAGES_XMVN_RESOLVE_TEST": os.path.join(dest, os.path.basename(src))})
        kwargs.update({"env": env})
        del kwargs["xmvnresolve_output"]
    return args, kwargs


def mvn_depmap(pom, jar=None, fnargs=None):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            os.chdir(self.workdir)
            buildroot = os.path.join(self.workdir, "builddir/build/BUILDROOT")
            env = {'RPM_BUILD_ROOT': buildroot}
            scriptpath = path.join(DIRPATH, '..', 'java-utils', 'maven_depmap.py')
            args = ['.fragment_data', pom]
            if jar:
                args.append(path.join(os.getcwd(), jar))
            args.extend(fnargs or [])
            (stdout, stderr, return_value) = call_script(scriptpath, args, extra_env=env)
            frag = None
            if return_value == 0:
                with open('.fragment_data','r') as frag_file:
                    frag = frag_file.read()
                os.remove('.fragment_data')
            fun(self, stdout, stderr, return_value, depmap=frag)
        return test_decorated
    return test_decorator

def mvn_artifact(pom, jar=None):
    def test_decorator(fun):
        @wraps(fun)
        def test_decorated(self):
            os.chdir(self.datadir)
            scriptpath = path.join(DIRPATH, '..', 'java-utils', 'mvn_artifact.py')
            os.chdir(self.workdir)
            args = [pom]
            if jar:
                args.append(path.join(os.getcwd(), jar))
            (stdout, stderr, return_value) = call_script(scriptpath, args)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

class WorkdirTestCase(unittest.TestCase):
    olddir = os.getcwd()
    WORKDIR = '.workdir'

    def setUp(self):
        self.olddir = os.getcwd()
        try:
            shutil.rmtree(self.WORKDIR)
        except OSError:
            pass
        os.mkdir(self.WORKDIR)
        os.chdir(self.WORKDIR)

    def tearDown(self):
        try:
            shutil.rmtree(self.WORKDIR)
        except OSError:
            pass
        os.chdir(self.olddir)

def exec_pom_macro(line, poms_tree, want_tree=None, filename='pom.xml'):
    """
    Parameters:
        line::
            A line of spec code injected to %prep
        poms_tree::
            dictionary that maps subpackage directory paths to input poms
        want_tree::
            dictionary that maps subpackage directory paths to wanted poms
            (in want directory)
    It creates a directory structure corresponding to keys in poms_tree and
    copies pom files into it. Then it executes prep and compares altered poms
    to wanted ones from want_tree (if not specified in want_tree it is assumed
    to remain unchanged and is compared with the original pom). Returns tuple
    of rpmbuild's return value, stderr and report of differences in xml files.
    """
    DATADIR = path.join(DIRPATH, 'data', 'pom_editor')
    pack = Package('test')
    pack.append_to_prep(line)
    for destpath, sourcepath in poms_tree.items():
        pack.add_source(path.join(DATADIR, sourcepath), path.join(destpath, filename))
    _, stderr, return_value = pack.run_prep()
    reports = []
    if return_value == 0:
        for filepath, pom in poms_tree.items():
            if want_tree and filepath in want_tree:
                expected_pom = path.join('want', want_tree[filepath])
            else:
                expected_pom = pom
            expected_pom = path.join(DATADIR, expected_pom)
            actual_pom = path.join(pack.buildpath, filepath, filename)
            reports.append(compare_xml_files(actual_pom, expected_pom))
    return return_value, stderr, '\n'.join(reports).strip()

def exec_pom_macro_simple(line, pom, want=None, filename='pom.xml'):
    return exec_pom_macro(line, {'': pom}, {'': want} if want else None, filename=filename)


def assertIn(obj, item, iterable):
    obj.assertTrue(item in iterable, msg="{item} not found in {iterable}"
                   .format(item=item, iterable=iterable))
