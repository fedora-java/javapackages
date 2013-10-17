import os
import shutil
import sys
import subprocess
import re

DIRPATH = os.path.dirname(os.path.realpath(__file__))
PYTHONPATH = os.path.join(DIRPATH, '../python')
sys.path.append(PYTHONPATH)
SCRIPT_ENV = {'PATH':DIRPATH, 'PYTHONPATH':PYTHONPATH}

def call_script(name, args, stdin = None, wrapped = False):
    outfile = open("tmpout", 'w')
    errfile = open("tmperr", 'w')
    if wrapped:
        procargs = [sys.executable, os.path.join(DIRPATH, 'wrapper.py'), name]
    else:
        procargs = [sys.executable, name]
    proc = subprocess.Popen(procargs + args, shell = False,
        stdout = outfile, stderr = errfile, env = SCRIPT_ENV,
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
    return os.path.join('.xmvn', 'config.d', filename)

def get_expected_config(filename, scriptname, testname):
    fileno = re.findall('[0-9]+', filename)
    if fileno:
        expfname = '{name}_{idx}.xml'.format(name=testname, idx=fileno[-1])
    else:
        expfname = filename
    return os.path.join(DIRPATH, 'data', scriptname, expfname)

def get_actual_args():
    return open('.xmvn/out').read()

def get_expected_args(scriptname, testname):
    return open(os.path.join(DIRPATH, 'data', scriptname,
       "{name}_out".format(name=testname))).read()

def preload_xmvn_config(name, filename, dstname=None, update_index=False):
    def test_decorator(fun):
        def test_decorated(self):
            src = os.path.join(DIRPATH, 'data', name, filename)
            os.mkdir('.xmvn')
            os.mkdir('.xmvn/config.d')
            dst = os.path.join('.xmvn', 'config.d', dstname or filename)
            shutil.copy(src, dst)
            if update_index:
                idx = 1
                if os.path.exists('.xmvn/javapackages-rule-index'):
                    with open('.xmvn/javapackages-rule-index', 'r') as index:
                        idx = int(index.read())
                with open('.xmvn/javapackages-rule-index', 'w') as index:
                    index.write(str(idx))
            fun(self)
        return test_decorated
    return test_decorator

def xmvnconfig(name, fnargs):
    def test_decorator(fun):
        def test_decorated(self):
            path = os.path.join(DIRPATH, '..', 'java-utils', name + '.py')
            (stdout, stderr, return_value) = call_script(path, fnargs)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

def build_depmap_paths(filelist):
    paths = []
    for filename in filelist:
        paths.append(os.path.join(DIRPATH, 'depmaps', filename))
    return '\n'.join(paths)

def mavenprov(filelist):
    def test_decorator(fun):
        def test_decorated(self):
            path = os.path.join(DIRPATH, '..', 'depgenerators', 'maven.prov')
            stdin = build_depmap_paths(filelist)
            (stdout, stderr, return_value) = call_script(path,
                    [], stdin=stdin, wrapped=True)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

def mavenreq(filelist):
    def test_decorator(fun):
        def test_decorated(self):
            path = os.path.join(DIRPATH, '..', 'depgenerators', 'maven.req')
            stdin = build_depmap_paths(filelist)
            (stdout, stderr, return_value) = call_script(path,
                    [], stdin=stdin, wrapped=True)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

def mvn_depmap(pom, jar=None, fnargs=None):
    def test_decorator(fun):
        def test_decorated(self):
            os.chdir(self.workdir)
            path = os.path.join(DIRPATH, '..', 'java-utils', 'maven_depmap.py')
            args = ['.fragment_data', pom]
            if jar:
                args.append(os.path.join(os.getcwd(), jar))
            args.extend(fnargs or [])
            (stdout, stderr, return_value) = call_script(path, args)
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
            path = os.path.join(DIRPATH, '..', 'java-utils', 'mvn_artifact.py')
            os.chdir(self.workdir)
            args = [pom]
            if jar:
                args.append(os.path.join(os.getcwd(), jar))
            (stdout, stderr, return_value) = call_script(path, args)
            fun(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator
