import os
import sys
import subprocess
import shutil
import unittest

import lxml.etree as etree

script_env = dict()
script_env['PYTHONPATH'] = os.environ['PYTHONPATH']
script_env['PATH'] = '.'

def callScript(name, args):
    outfile = open("tmpout", 'w')
    errfile = open("tmperr", 'w')
    proc = subprocess.Popen([sys.executable, name] + args, shell = False, 
        stdout = outfile, stderr = errfile, env = script_env)
    ret = proc.wait()
    outfile = open("tmpout", 'r+')
    errfile = open("tmperr", 'r+')
    out = outfile.read()
    err = errfile.read()
    os.remove('tmpout')
    os.remove('tmperr')
    return (out, err, ret)

def getScriptOutput(testclass, args):
    (stdout, stderr, return_value) = callScript(testclass.path(), args)
    testclass.assertEqual("", stderr)
    testclass.assertEqual(0, return_value)
    testclass.assertTrue(os.path.exists(".xmvn/config.d/"))
    filenames = os.listdir(".xmvn/config.d/")
    testclass.assertEquals(1, len(filenames))
    return open(".xmvn/config.d/" + filenames[0], 'r')

def compareXmvnConfig(args):
    def test_decorator(fn):
        def test_decorated(self):
            (stdout, stderr, return_value) = callScript(self.path(), args)
            self.assertEqual("", stderr)
            self.assertEqual(0, return_value)
            self.assertTrue(os.path.exists(".xmvn/config.d/"))
            filenames = os.listdir(".xmvn/config.d/")
            for i in range(len(filenames)):
                exppath = 'data/{}_{}_{:05d}.xml'.format(self.path()[18:-3], fn.__name__[5:], i + 1) 
                expfile = open(exppath, 'r')
                actfile = open(".xmvn/config.d/" + filenames[i], 'r')
                actual = etree.tostring(etree.parse(actfile), pretty_print=True)
                expected = etree.tostring(etree.parse(expfile), pretty_print=True)
                self.assertEquals(expected, actual)
        return test_decorated
    return test_decorator

def compareXmvnArgs(args):
    def test_decorator(fn):
        def test_decorated(self):
            (stdout, stderr, return_value) = callScript(self.path(), args)
            self.assertEqual("", stderr)
            self.assertEqual(0, return_value)
            self.assertTrue(os.path.exists(".xmvn/out"))
            actfile = open(".xmvn/out", 'r');
            expfile = open("data/" + self.path()[18:-3] + '_' + fn.__name__[5:] + '_out')
            self.assertEquals(expfile.read(), actfile.read())
        return test_decorated
    return test_decorator

class ScriptTest:
    def setUp(self):
        try:
            shutil.rmtree(".xmvn/")
        except OSError:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(".xmvn/")
        except OSError:
            pass

    def test_run_no_args(self):
        (out, err, ret) = callScript(self.path(), [])
        self.assertNotEqual(ret, 0)
        self.assertEqual("Usage:", err[:6])

    def test_help(self):
        (out, err, ret) = callScript(self.path(), ['-h'])
        self.assertTrue(out)

