import inspect
import os
import unittest
import shutil

from test_common import (DIRPATH, install_pom, call_script, assertIn)

from lxml import etree
from xml_compare import compare_lxml_etree


class TestInstallPom(unittest.TestCase):

    maxDiff = 2048

    def setUp(self):
        try:
            self.olddir = os.getcwd()
            self.datadir = os.path.join(DIRPATH,
                                        'data',
                                        'install_pom')
            self.workdir = os.path.realpath(os.path.join(self.datadir, "..",
                                            "install_pom_workdir"))

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

    def check_result(self, test_name, result):
        got = etree.parse(result).getroot()
        want = etree.parse(os.path.join(self.workdir,
                                        test_name+"-want.xml")).getroot()
        report = compare_lxml_etree(got, want)
        if report:
            report = '\n' + report
        return report

    @install_pom('JPP-bndlib.pom')
    def test_basic(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom('JPP-apache-commons-io.pom')
    def test_packaging_pom(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom('JPP-noversion.pom')
    def test_missing_version(self, stdout, stderr, return_value, result):
        self.assertNotEqual(return_value, 0)

    @install_pom('JPP-noversion-pom.pom')
    def test_packaging_pom_missing_version(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom('JPP-parent-version.pom')
    def test_parent_version(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom(os.path.join('cglib', 'pom.xml'))
    def test_parent_install(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom(os.path.join('cglib', 'cglib', 'pom.xml'))
    def test_interpolate_from_parent(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom(os.path.join('cglib', 'cglib-integration-test', 'pom.xml'))
    def test_interpolate_from_model(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom(os.path.join('xmvn', 'xmvn-mojo', 'pom.xml'))
    def test_parent_relpath(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom(os.path.join('xmvn', 'xmvn-tools', 'xmvn-install', 'pom.xml'))
    def test_parent_chain(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom(os.path.join('xmvn', 'xmvn-tools', 'xmvn-resolve', 'pom.xml'))
    def test_any_not_final(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom(os.path.join('languagetool', 'languagetool-standalone', 'pom.xml'))
    def test_dep_type(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom(os.path.join('languagetool', 'languagetool-language-modules', 'ja', 'pom.xml'))
    def test_dep_classifier(self, stdout, stderr, return_value, result):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           result)
        self.assertEqual(report, '', report)

    @install_pom('a_binary_file.pom')
    def test_not_pom(self, stdout, stderr, return_value, result):
        self.assertNotEqual(return_value, 0)

    @install_pom('a_file_that_does_not_exist.pom')
    def test_no_pom(self, stdout, stderr, return_value, result):
        self.assertNotEqual(return_value, 0)

    def test_no_args(self):
        stdout, stderr, return_value = call_script(os.path.join(DIRPATH, '..',
            'java-utils', 'install_pom.py'), [])
        self.assertNotEqual(return_value, 0)

    def test_no_directory(self):
        stdout, stderr, return_value = call_script(os.path.join(DIRPATH, '..',
            'java-utils', 'install_pom.py'),
                ['JPP-bndlib.pom', os.path.join('missingdir', 'JPP-bndlib.pom')])
        self.assertNotEqual(return_value, 0)

    def test_not_directory(self):
        stdout, stderr, return_value = call_script(os.path.join(DIRPATH, '..',
            'java-utils', 'install_pom.py'),
                ['JPP-bndlib.pom', os.path.join('fakedir', 'JPP-bndlib.pom')])
        self.assertNotEqual(return_value, 0)

    def test_no_overwrite(self):
        stdout, stderr, return_value = call_script(os.path.join(DIRPATH, '..',
            'java-utils', 'install_pom.py'),
                ['JPP-bndlib.pom', 'fakedir'])
        self.assertNotEqual(return_value, 0)

if __name__ == '__main__':
    unittest.main()
