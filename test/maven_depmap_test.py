import inspect
from zipfile import ZipFile
import pyxb.utils.six as six
import os
import unittest
import shutil
from test_common import DIRPATH, mvn_depmap, call_script, prepare_metadata


from lxml import etree
from xml_compare import compare_lxml_etree

class TestMavenDepmap(unittest.TestCase):

    maxDiff = 2048

    def setUp(self):
        try:
            self.olddir = os.getcwd()
            self.datadir = os.path.join(DIRPATH,
                                        'data',
                                        'maven_depmap')
            self.workdir = os.path.realpath(os.path.join(self.datadir, "..",
                                            "maven_depmap_workdir"))

            shutil.copytree(self.datadir, self.workdir)
            os.chdir(self.workdir)
        except OSError:
            pass

        prepare_metadata(self.workdir)

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
        report = compare_lxml_etree(got, want, unordered=['jpp', 'maven'])
        if report:
            report = '\n' + report
        return report

    def check_archive(self, test_name, archive_path, keep_comments=False):
        got = ZipFile(archive_path, 'r')
        want = ZipFile('{name}-want.{ext}'.format(name=test_name,
                       ext=archive_path.split('.')[-1]))
        try:
            if got.testzip() is not None:
                return ("Not valid zip file", "")
            got_mf = self.read_archive(got, keep_comments)
            want_mf = self.read_archive(want, keep_comments)
        finally:
            got.close()
            want.close()
        return (got_mf, want_mf)

    def read_archive(self, archive, keep_comments=False):
        res = {}
        for filename in archive.namelist():
            mf_file = archive.open(filename)
            try:
                if (keep_comments):
                    res[six.text_type(filename)] = mf_file.readlines()
                else:
                    res[six.text_type(filename)] = \
                            [line for line in mf_file.readlines()
                                    if not line.startswith(b'#')]
            finally:
                mf_file.close()
        return res

    @mvn_depmap('JPP-bndlib.pom', 'usr/share/java/bndlib.jar')
    def test_basic(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('JPP-commons-io.pom')
    def test_missing_jar_arg(self, stdout, stderr, return_value, depmap):
        self.assertNotEqual(return_value, 0)

    @mvn_depmap('JPP-apache-commons-io.pom')
    def test_packaging_pom_no_jar(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('JPP-noversion.pom')
    def test_missing_version(self, stdout, stderr, return_value, depmap):
        self.assertNotEqual(return_value, 0)

    @mvn_depmap('JPP-parent-version.pom')
    def test_parent_version(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('JPP-commons-war.pom', 'usr/share/java/commons-war.war')
    def test_war(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    def test_not_pom(self):
        stdout, stderr, return_value = call_script(os.path.join(DIRPATH, '..',
            'java-utils', 'maven_depmap.py'),
                ['.out', 'usr/share/java/commons-io.jar',
                    'usr/share/java/commons-io.jar'])
        self.assertNotEqual(return_value, 0)

    def test_no_pom(self):
        stdout, stderr, return_value = call_script(os.path.join(DIRPATH, '..',
            'java-utils', 'maven_depmap.py'),
                ['.out'])
        self.assertNotEqual(return_value, 0)

    def test_no_args(self):
        stdout, stderr, return_value = call_script(os.path.join(DIRPATH, '..',
            'java-utils', 'maven_depmap.py'),
                [])
        self.assertNotEqual(return_value, 0)

    @mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar')
    def test_mvn_spec(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('a:b:war::1', 'usr/share/java/commons-war.war')
    def test_mvn_spec_war(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('/builddir/build/BUILDROOT/pkg-2.5.2-2.fc21.x86_64/a:b:war::1',
            'usr/share/java/commons-war.war')
    def test_mvn_spec_buildroot(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('builddir/build/BUILDROOT/usr/share/maven-poms/JPP-commons-war.pom',
                'usr/share/java/commons-war.war')
    def test_buildroot(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                   depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar', ['-a', 'x:y'])
    def test_append(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    # FIXME: aliases cause trouble
    #@mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar', ['-a', 'x:y,z:w'])
    #def test_append_multiple(self, stdout, stderr, return_value, depmap):
    #    self.assertEqual(return_value, 0, stderr)
    #    report = self.check_result(inspect.currentframe().f_code.co_name,
    #                                       depmap)
    #    self.assertEqual(report, '', report)

    @mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar', ['-n', 'myns'])
    def test_namespace(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('a:b:12', 'usr/share/java/commons-io.jar', ['--namespace=myns',
        '--append=x:y'])
    def test_append_and_namespace(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('a:b:12', 'usr/foo/share/java/compare_jar.jar')
    def test_compare_jar(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want = self.check_archive(inspect.currentframe().f_code.co_name,
                'usr/foo/share/java/compare_jar.jar')
        self.assertEqual(got, want)

    #test case for rhbz#1012982
    @mvn_depmap('x:y:war:z:0.1', 'usr/foo/share/java/compare_jar_class_ext.war')
    def test_compare_jar_class_ext(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want = self.check_archive(inspect.currentframe().f_code.co_name,
                'usr/foo/share/java/compare_jar_class_ext.war')
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

    @mvn_depmap('/builddir/build/BUILDROOT/pkg-2.5.2-2.fc21.x86_64/x:y:0.1',
            'usr/share/java/already-has-pom-properties.jar')
    def test_rhbz1012245(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        got, want = self.check_archive('test_compare_jar_modified',
                'usr/share/java/already-has-pom-properties.jar')
        self.assertEqual(got, want)

    @mvn_depmap('x:y:jar:z:0.1', 'usr/share/java/commons-io-z.jar',
            ['-a', 'a:b:jar:c:12'])
    def test_classifier(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('x:y:0.1', 'usr/share/java/commons-io.jar', ['-r', '1,2,3'])
    def test_version(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('JPP/x:y:0.1', 'usr/share/java/commons-io.jar',
            ['--versions', '1,2,3'])
    def test_version2(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result('test_version', depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('x:y:0.1', 'usr/share/java/commons-io.jar',
            ['-r', '1,2,3', '-a', 'a:b:32'])
    def test_version_append(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('x:y:0.1', 'usr/share/java/commons-io.jar',
            ['-r', '1,2,3', '-n', 'ns', '-a', 'a:b:32'])
    def test_version_namespace(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('x:y', 'usr/share/java/commons-io.jar')
    def test_missing_version2(self, stdout, stderr, return_value, depmap):
        self.assertNotEqual(return_value, 0)

    @mvn_depmap('x:y:war:1', 'usr/share/java/commons-io.jar')
    def test_incorrect_extension(self, stdout, stderr, return_value, depmap):
        self.assertNotEqual(return_value, 0)

    @mvn_depmap('evil:', 'usr/share/java/commons-io.jar')
    def test_incorrect_artifact(self, stdout, stderr, return_value, depmap):
        self.assertNotEqual(return_value, 0)

    @mvn_depmap('JPP-cdata.pom')
    def test_cdata(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

    @mvn_depmap('g:a:war:1.2.3', 'usr/share/java/versioned.war', ['-r', '2.0.0'])
    def test_versioned(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)
        self.assertEqual(False, os.path.exists('usr/share/java/versioned.war'))
        self.assertEqual(True, os.path.exists('usr/share/java/versioned-2.0.0.war'))

    @mvn_depmap('g:a:1.2', 'usr/share/java/versioned2.jar', ['-r', '1.2'])
    def test_versioned2(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)
        self.assertEqual(False, os.path.exists('usr/share/java/versioned2.jar'))
        self.assertEqual(True, os.path.exists('usr/share/java/versioned2-1.2.jar'))

    @mvn_depmap('g:a:jar:tests:1', 'usr/share/java/versioned-3-tests.jar', ['-r', '1,1.2'])
    def test_versioned_classifier(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)
        self.assertEqual(False, os.path.exists('usr/share/java/versioned-3-tests.jar'))
        self.assertEqual(True, os.path.exists('usr/share/java/versioned-3-tests-1.jar'))
        self.assertEqual(True, os.path.exists('usr/share/java/versioned-3-tests-1.2.jar'))

    @mvn_depmap('JPP-testversioned.pom', 'usr/share/java/testversioned.jar', ['-r', '2013.10'])
    def test_versioned_with_pom(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)
        self.assertEqual(False, os.path.exists('usr/share/java/testversioned.jar'))
        self.assertEqual(True, os.path.exists('usr/share/java/testversioned-2013.10.jar'))

    @mvn_depmap('JPP-alias.pom', 'usr/share/java/commons-io.jar', ['-a', 'a:b'])
    def test_alias_extension(self, stdout, stderr, return_value, depmap):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name,
                                           depmap)
        self.assertEqual(report, '', report)

if __name__ == '__main__':
    unittest.main()
