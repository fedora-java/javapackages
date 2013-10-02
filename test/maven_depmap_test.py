import inspect
from zipfile import ZipFile
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

    def check_result(self, test_name, depmap):
        got = etree.fromstring(depmap)
        want = etree.parse(os.path.join(self.workdir,
                                        test_name+"-want.xml")).getroot()
        report = []
        res = doctest_xml_compare.xml_compare(got, want, lambda x: report.append(x))
        return got, want, res, report

    def check_archive(self, test_name, archive_path, keep_comments=False):
        with ZipFile(archive_path, 'r') as got:
            with ZipFile('{name}-want.{ext}'.format(name=test_name,
                            ext=archive_path.split('.')[-1])) as want:
                if got.testzip() is not None: return ("Not valid zip file", "")
                got_mf = self.read_archive(got, keep_comments)
                want_mf = self.read_archive(want, keep_comments)
                return (got_mf, want_mf)

    def read_archive(self, archive, keep_comments=False):
        res = {}
        for f in archive.namelist():
            with archive.open(f) as mf_file:
                if (keep_comments):
                    res[f] = mf_file.readlines()
                else:
                    res[f] = [line for line in mf_file.readlines() if not line.startswith('#')]
        return res

    @mvn_depmap('JPP-bndlib.pom', 'usr/share/java/bndlib.jar')
    def test_basic(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('JPP-aqute-bndlib.pom', 'usr/share/java/aqute-bndlib.jar')
    def test_different_artifactId(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('JPP-commons-io.pom')
    def test_missing_jar_arg(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 1, stderr)

    @mvn_depmap('JPP-apache-commons-io.pom')
    def test_packaging_pom_no_jar(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('JPP-noversion.pom')
    def test_missing_version(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 1, stderr)

    @mvn_depmap('JPP-commons-war.pom', 'usr/share/java/commons-war.war')
    def test_war(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('JPP-commons-weird.pom', 'usr/share/java/commons-weird.war')
    def test_weird_packaging(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('JPP-packaging-pom.pom', 'usr/share/java/packaging-pom.jar')
    def test_packaging_pom_and_jar(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('JPP.commons-io-commons-io.pom', 'usr/share/java/commons-io/commons-io.jar')
    def test_subdirectory(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('JPP-commons-io-commons-io.pom', '/usr/share/java/commons-io.jar')
    def test_incorrect_subdir1(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 1, stderr)

    @mvn_depmap('JPP-commons-io.pom', '/usr/share/java/commons-io/commons-io.jar')
    def test_incorrect_subdir2(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 1, stderr)

    @mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar')
    def test_mvn_spec(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('a:b:war::1', 'usr/share/java/commons-war.war')
    def test_mvn_spec_war(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('/builddir/build/BUILDROOT/pkg-2.5.2-2.fc21.x86_64/a:b:war::1', 'usr/share/java/commons-war.war')
    def test_mvn_spec_buildroot(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar', ['-a', 'x:y'])
    def test_append(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar', ['-a', 'x:y,z:w'])
    def test_append_multiple(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar', ['-n', 'myns'])
    def test_namespace(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar', ['--namespace=myns', '--append=x:y'])
    def test_append_and_namespace(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('a:b:12', 'usr/foo/share/java/foo.jar', ['-p', 'usr/foo'])
    def test_prefix(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want, res, report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, [])
        self.assertEqual(res, True)

    @mvn_depmap('a:b:12', 'usr/foo/share/java/.out_archive.jar')
    def test_compare_jar(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want = self.check_archive(inspect.currentframe().f_code.co_name,
                'usr/foo/share/java/.out_archive.jar')
        self.assertEqual(got, want)

    @mvn_depmap('a:b:12', 'usr/share/java/already-has-pom-properties.jar')
    def test_compare_jar_unmodified(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want = self.check_archive(inspect.currentframe().f_code.co_name,
                'usr/share/java/already-has-pom-properties.jar', keep_comments=True)
        self.assertEqual(got, want)

    @mvn_depmap('x:y:0.1', 'usr/share/java/already-has-pom-properties.jar')
    def test_compare_jar_modified(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want = self.check_archive(inspect.currentframe().f_code.co_name,
                'usr/share/java/already-has-pom-properties.jar')
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
