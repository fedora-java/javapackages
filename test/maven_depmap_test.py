import inspect
import os
import unittest
import shutil
from test_common import *


from lxml import etree
from formencode import doctest_xml_compare

class TestMavenDepmap(unittest.TestCase):

    def setUp(self):
        try:
            dirpath = os.path.dirname(os.path.realpath(__file__))
            self.olddir = os.getcwd()
            self.datadir = os.path.join(dirpath,
                                        'data',
                                        'maven_depmap')
            self.workdir = os.path.join(self.datadir, "..",
                                        "maven_depmap_workdir")

            shutil.copytree(self.datadir, self.workdir)
            os.chdir(self.workdir)
        except OSError:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(self.workdir)
            os.chdir(self.olddir)
        except OSError:
            pass

    def xml_compare_reporter(self, report):
        print report

    def check_result(self, test_name, depmap):
        got = etree.fromstring(depmap)
        want = etree.parse(os.path.join(self.workdir,
                                        test_name+"-want.xml")).getroot()
        res = doctest_xml_compare.xml_compare(got, want, self.xml_compare_reporter)
        return got, want, res

    @mvn_depmap('JPP-bndlib.pom', 'usr/share/java/bndlib.jar')
    def test_basic(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(res, True)

    @mvn_depmap('JPP-aqute-bndlib.pom', 'usr/share/java/aqute-bndlib.jar')
    def test_different_artifactId(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(res, True)

if __name__ == '__main__':
    unittest.main()
