import os
import re
import shutil
import subprocess
import sys
import unittest

import javapackages.metadata as m
from os import path
from test_rpmbuild import Package
from xml_compare import compare_xml_files

DIRPATH = path.dirname(path.realpath(__file__))
PYTHONPATH = path.join(DIRPATH, '../python')
sys.path.append(PYTHONPATH)
SCRIPT_ENV = {'PATH':'{mock}:{real}'.format(mock=DIRPATH,
                                            real=os.environ['PATH']),
              'PYTHONPATH':PYTHONPATH}

def call_script(name, args, stdin = None, wrapped = False, extra_env = {}):
    outfile = open("tmpout", 'w')
    errfile = open("tmperr", 'w')
    procargs = [sys.executable, path.join(DIRPATH, 'wrapper.py'), name]
    env = dict(SCRIPT_ENV.items() + extra_env.items())
    proc = subprocess.Popen(procargs + args, shell = False,
        stdout = outfile, stderr = errfile, env = env,
        stdin = subprocess.PIPE)
    proc.communicate(stdin)
    ret = proc.wait()
    outfile = open("tmpout", 'r+')
    errfile = open("tmperr", 'r+')
    out = outfile.read()
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
    return open('.xmvn/out').read()

def get_expected_args(scriptname, testname):
    return open(path.join(DIRPATH, 'data', scriptname,
       "{name}_out".format(name=testname))).read()

def preload_xmvn_config(name, filename, dstname=None, update_index=False):
    def test_decorator(fun):
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
                metadata = m.CreateFromDocument(open(want_file).read())
                for a in metadata.artifacts.artifact:
                    if '%' in a.path:
                        a.path = a.path % (metadata_dir)
                with open(want_file, "w") as f:
                    dom = metadata.toDOM(None)
                    f.write(dom.toprettyxml(indent="   "))


def xmvnconfig(name, fnargs):
    def test_decorator(fun):
        def test_decorated(self):
            scriptpath = path.join(DIRPATH, '..', 'java-utils', name + '.py')
            (stdout, stderr, return_value) = call_script(scriptpath, fnargs)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

def build_depmap_paths(filelist):
    paths = []
    for filename in filelist:
        paths.append(os.path.join(DIRPATH, 'metadata', filename))
    return '\n'.join(paths)

def mavenprov(filelist):
    def test_decorator(fun):
        def test_decorated(self):
            scriptpath = path.join(DIRPATH, '..', 'depgenerators', 'maven.prov')
            stdin = build_depmap_paths(filelist)
            (stdout, stderr, return_value) = call_script(scriptpath,
                    [], stdin=stdin, wrapped=True)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

def osgiprov(filelist):
    def test_decorator(fun):
        def test_decorated(self):
            scriptpath = path.join(DIRPATH, '..', 'depgenerators', 'osgi.prov')
            #stdin = build_depmap_paths(filelist)
            stdin = "\n".join(filelist)
            (stdout, stderr, return_value) = call_script(scriptpath,
                    [], stdin=stdin, wrapped=True)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

def mavenreq(filelist, config='default'):
    def test_decorator(fun):
        def test_decorated(self):
            scriptpath = path.join(DIRPATH, '..', 'depgenerators', 'maven.req')
            stdin = build_depmap_paths(filelist)
            config_path = os.path.join(DIRPATH, 'data', 'config', config + '.json')
            env = {'JAVAPACKAGES_CONFIG': config_path}
            (stdout, stderr, return_value) = call_script(scriptpath,
                    [], stdin=stdin, wrapped=True, extra_env=env)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

def mvn_depmap(pom, jar=None, fnargs=None):
    def test_decorator(fun):
        def test_decorated(self):
            os.chdir(self.workdir)
            buildroot = os.path.join(self.workdir, "builddir/build/BUILDROOT")
            env = {'RPM_BUILD_ROOT': buildroot}
            scriptpath = path.join(DIRPATH, '..', 'java-utils', 'maven_depmap.py')
            args = ['.fragment_data', pom]
            if jar:
                args.append(path.join(os.getcwd(), jar))
            args.extend(fnargs or [])
            (stdout, stderr, return_value) = call_script(scriptpath, args, extra_env = env)
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
    for destpath, sourcepath in poms_tree.iteritems():
        pack.add_source(path.join(DATADIR, sourcepath), path.join(destpath, filename))
    _, stderr, return_value = pack.run_prep()
    reports = []
    if return_value == 0:
        for filepath, pom in poms_tree.iteritems():
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
