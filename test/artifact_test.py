import inspect
import os
import unittest
import shutil
from test_common import *
from lxml import etree
from formencode import doctest_xml_compare

class TestMvnArtifact(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        cls.datadir = os.path.join(dirpath, 'data', 'artifact')

        try:
            cls.olddir = os.getcwd()
            cls.workdir = os.path.join(dirpath, 'data', 'artifact_workdir')

            shutil.copytree(cls.datadir, cls.workdir)
            os.chdir(cls.workdir)
        except OSError:
            pass

        for dirname, dirnames, filenames in os.walk(cls.workdir):
            for filename in filenames:
                if filename.endswith("-want.xml"):
                    want_file = os.path.join(dirname, filename)
                    doc = etree.parse(want_file)
                    pom_paths = doc.xpath("./artifact/rawPomPath")
                    if len(pom_paths) > 0:
                        for pom_path in pom_paths:
                            pom_path.text = pom_path.text % (cls.workdir)
                    jar_paths = doc.xpath("./artifact/file")
                    if len(jar_paths) > 0:
                        for jar_path in jar_paths:
                            jar_path.text = jar_path.text % (cls.workdir)
                    with open(want_file, "w") as f:
                        f.write(etree.tostring(doc.getroot(), pretty_print=True))

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
        print report

    def check_result(self, test_name):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        got = etree.parse(".xmvn-reactor").getroot()
        want = etree.parse(os.path.join(self.workdir,
                                        test_name+"-want.xml")).getroot()
        res = doctest_xml_compare.xml_compare(got, want, self.xml_compare_reporter)
        return got, want, res

    @mvn_artifact('args4j.pom')
    def test_basic(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(res, True)

    @mvn_artifact('args4j.pom', 'maven-artifact.jar')
    def test_basic_jar(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(res, True)

    @mvn_artifact('args4j.pom', 'webapp.war')
    def test_artifact_war(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(res, True)

    @mvn_artifact('a:b:12', 'test.jar')
    def test_mvn_spec_jar(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(res, True)

    @mvn_artifact('a:b:12', 'test.war')
    def test_mvn_spec_war(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(res, True)

    @mvn_artifact('a:b:jar:12', 'test.jar')
    def test_mvn_spec_ext(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(res, True)

    @mvn_artifact('a:b:war:12', 'test.war')
    def test_mvn_spec_ext_war(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(res, True)

    @mvn_artifact('a:b::sources:12', 'test-sources.jar')
    def test_mvn_spec_classifier(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(res, True)

    @mvn_artifact('a:b:war:javadoc:12', 'test-javadoc.war')
    def test_mvn_spec_classifier_war(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        got, want, res = self.check_result(inspect.currentframe().f_code.co_name)
        self.assertEqual(res, True)

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

    @mvn_artifact('a:b::javadoc:12', 'test-javadoc.war')
    def test_extension_not_specified(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)


if __name__ == '__main__':
    unittest.main()
