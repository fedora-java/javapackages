import inspect
import os
import unittest
import shutil
from test_common import *
from lxml import etree
from xml_compare import compare_lxml_etree


class TestMvnArtifact(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        cls.datadir = os.path.join(dirpath, 'data', 'mvn_artifact')

        try:
            cls.olddir = os.getcwd()
            cls.workdir = os.path.join(dirpath, 'data', 'artifact_workdir')

            shutil.copytree(cls.datadir, cls.workdir)
            os.chdir(cls.workdir)
        except OSError:
            pass

        prepare_metadata(cls.workdir)

    @classmethod
    def tearDownClass(cls):
        try:
            shutil.rmtree(cls.workdir)
            os.chdir(cls.olddir)
        except OSError:
            pass

    def tearDown(self):
        try:
            os.remove('.xmvn-reactor')
        except OSError:
            pass

    def xml_compare_reporter(self, report):
        print(report)

    def check_result(self, test_name):
        got = etree.parse(".xmvn-reactor").getroot()
        want = etree.parse(os.path.join(self.workdir,
                                        test_name+"-want.xml")).getroot()
        report = compare_lxml_etree(got, want, unordered=['dependencies'])
        if report:
            report = '\n' + report
        return report

    @mvn_artifact('args4j.pom')
    def test_basic(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

    @mvn_artifact('args4j.pom', 'maven-artifact.jar')
    def test_basic_jar(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

    @mvn_artifact('args4j.pom', 'webapp.war')
    def test_artifact_war(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

    @mvn_artifact('a:b:12', 'test.jar')
    def test_mvn_spec_jar(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

    @mvn_artifact('a:b:war:12', 'test.war')
    def test_mvn_spec_war(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

    @mvn_artifact('a:b:jar:12', 'test.jar')
    def test_mvn_spec_ext(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

    @mvn_artifact('a:b:war:12', 'test.war')
    def test_mvn_spec_ext_war(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

    @mvn_artifact('a:b::sources:12', 'test-sources.jar')
    def test_mvn_spec_classifier(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

    @mvn_artifact('a:b:war:javadoc:12', 'test-javadoc.war')
    def test_mvn_spec_classifier_war(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

    @mvn_artifact('a:b:12')
    def test_mvn_spec_nojar(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mvn_artifact('a:b:tar:javadoc:12', 'test-javadoc.war')
    def test_extensions_dont_match(self, stdout, stderr, return_value):
        # different extensions
        self.assertNotEqual(return_value, 0, stderr)

    @mvn_artifact('a:b:jar:javadoc:12', 'test-javadoc.war')
    def test_extensions_dont_match2(self, stdout, stderr, return_value):
        # jar != war
        self.assertNotEqual(return_value, 0, stderr)

    @mvn_artifact('a:b::javadoc:12', 'test-javadoc.jar')
    def test_extension_not_specified(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)

    #@mvn_artifact('args4j-deps.pom')
    #def test_dependencies_1(self, stdout, stderr, return_value):
    #    self.assertEqual(return_value, 0, stderr)
    #    report = self.check_result(inspect.currentframe().f_code.co_name)
    #    self.assertEqual(report, '', report)

    #@mvn_artifact('args4j-deps.pom', 'some.jar')
    #def test_dependencies_2(self, stdout, stderr, return_value):
    #    self.assertEqual(return_value, 0, stderr)
    #    report = self.check_result(inspect.currentframe().f_code.co_name)
    #    self.assertEqual(report, '', report)

    #@mvn_artifact('args4j-exclusions.pom', 'some.jar')
    #def test_dependencies_exclusions(self, stdout, stderr, return_value):
    #    self.assertEqual(return_value, 0, stderr)
    #    report = self.check_result(inspect.currentframe().f_code.co_name)
    #    self.assertEqual(report, '', report)

    #@mvn_artifact('asm-analysis-5.0.2.pom')
    #def test_missing_version(self, stdout, stderr, return_value):
    #    self.assertNotEqual(return_value, 0, stderr)

    @mvn_artifact('merge_sections/child/child/pom.xml')
    def test_merge_sections(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        report = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(report, '', report)

if __name__ == '__main__':
    unittest.main()
