import os
import shutil
import unittest

from xml_compare import compare_xml_files
from test_common import DIRPATH
from test_rpmbuild import Package

WORKDIR = os.path.join(DIRPATH, '.workdir')

def rpm_test():
    def test_decorator(function):
        def test_decorated(self):
            pack = Package(function.__name__)
            function(self, pack)
        return test_decorated
    return test_decorator

class MvnMacrosTest(unittest.TestCase):
    maxDiff = 2048

    def setUp(self):
        self.olddir = os.getcwd()
        try:
            shutil.rmtree(WORKDIR)
        except OSError:
            pass
        try:
            os.mkdir(WORKDIR)
        except OSError:
            pass
        os.chdir(WORKDIR)

    def tearDown(self):
        try:
            shutil.rmtree(WORKDIR)
        except OSError:
            pass
        os.chdir(self.olddir)

    @rpm_test()
    def test_mvn_alias_simple(self, pack):
        pack.append_to_prep('%mvn_alias aaa:bbb xxx:yyy')
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEquals(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_alias', 'simple_00001.xml')
        report = compare_xml_files(actfile, expfile, ['artifactGlob'])
        self.assertEquals(report, '', report)

    @rpm_test()
    def test_mvn_alias_backref(self, pack):
        pack.append_to_prep("""%mvn_alias '*:{aaa,bbb}*' ':@1'""")
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEquals(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_alias',
                               'backref_00001.xml')
        report = compare_xml_files(actfile, expfile, ['artifactGlob'])
        self.assertEquals(report, '', report)

    @rpm_test()
    def test_mvn_alias_multi(self, pack):
        pack.append_to_prep('%mvn_alias "aaa:bbb" "ccc:ddd" \
                             "eee:fff" "ggg:hhh"')
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEquals(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_alias',
                               'multi_00001.xml')
        report = compare_xml_files(actfile, expfile, ['artifactGlob'])
        self.assertEquals(report, '', report)

    @rpm_test()
    def test_mvn_alias_no_args(self, pack):
        pack.append_to_prep('%mvn_alias')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_alias_single_arg(self, pack):
        pack.append_to_prep('%mvn_alias "aaa:bbb"')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_alias_more_invocations(self, pack):
        pack.append_to_prep('%mvn_alias "aaa:bbb" "ccc:ddd"')
        pack.append_to_prep('%mvn_alias "{xxx,yyy}:zzz" "qqq:@1"')
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEquals(len(filelist), 2)
        for i in range(2):
            actfile = os.path.join(confpath, filelist[i])
            filename = 'more_invocations-0000{i}.xml'.format(i=i + 1)
            expfile = os.path.join(DIRPATH, 'data', 'mvn_alias', filename)
            report = compare_xml_files(actfile, expfile, ['artifactGlob'])
            self.assertEquals(report, '', report)

