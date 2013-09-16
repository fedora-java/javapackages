import os
import sys
import subprocess
import unittest
import re

from lxml import etree

dirpath = os.path.dirname(os.path.realpath(__file__))
pythonpath = os.path.join(dirpath, '../python')
sys.path.append(pythonpath)
script_env = {'PATH':'.', 'PYTHONPATH':pythonpath}

def call_script(name, args, stdin = None, wrapped = False):
    outfile = open("tmpout", 'w')
    errfile = open("tmperr", 'w')
    if wrapped:
        procargs = [sys.executable, os.path.join(dirpath, 'wrapper.py'), name]
    else:
        procargs = [sys.executable, name]
    proc = subprocess.Popen(procargs + args, shell = False, 
        stdout = outfile, stderr = errfile, env = script_env, stdin = subprocess.PIPE)
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
    actfile = open('.xmvn/config.d/' + filename)
    return etree.tostring(etree.parse(actfile), pretty_print=True)

def get_expected_config(filename, scriptname, testname):
    expfname = '{}_{}_{}.xml'.format(scriptname, testname, re.findall('[0-9]+', filename)[-1])
    expfile =  open(os.path.join(dirpath, 'data', expfname))
    return etree.tostring(etree.parse(expfile), pretty_print=True)

def get_expected_file_count(scriptname, testname):
    filelist = os.listdir(os.path.join(dirpath, 'data'))
    return len([file for file in filelist if file.startswith("{}_{}_".format(scriptname, testname))])

def get_actual_args():
    return open('.xmvn/out').read()

def get_expected_args(scriptname, testname):
   return open(os.path.join(dirpath, 'data', "{}_{}_out".format(scriptname, testname))).read()


def xmvnconfig(name, fnargs):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            path = os.path.join(dirpath, '..', 'java-utils', 'mvn_' + name + '.py')
            (stdout, stderr, return_value) = call_script(path, fnargs)
            fn(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

def mavenprov(filelist):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            path = os.path.join(dirpath, '..', 'depgenerators', 'maven.prov')
            input = '\n'.join([os.path.join(dirpath, 'depmaps', filename) for filename in filelist])
            (stdout, stderr, return_value) = call_script(path, [], stdin=input, wrapped=True)
            fn(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

def mavenreq(filelist):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            path = os.path.join(dirpath, '..', 'depgenerators', 'maven.req')
            input = '\n'.join([os.path.join(dirpath, 'depmaps', filename) for filename in filelist])
            (stdout, stderr, return_value) = call_script(path, [], stdin=input, wrapped=True)
            fn(self, stdout, stderr, return_value)
        return test_decorated
    return test_decorator

