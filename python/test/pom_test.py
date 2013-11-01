import os
import unittest
import lxml

from javapackages.pom import POM, PomLoadingException

from misc import exception_expected

def pomfile(fname):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            main_dir = os.path.dirname(os.path.realpath(__file__))
            fn(self, POM(os.path.join(main_dir, "data", fname)))
        return test_decorated

    return test_decorator

class TestPOM(unittest.TestCase):

    @exception_expected(IOError)
    @pomfile("NULL_FILE.pom.xml")
    def test_nonexisting_pom(self, p):
        self.assertTrue(False, "IOError was expected!")

    @pomfile("commons-lang.pom")
    def test_loading(self, p):
        self.assertTrue(True)

    @pomfile("commons-lang.pom")
    def test_with_parent(self, p):
        self.assertEqual(p.artifactId, "commons-lang")
        self.assertEqual(p.groupId, "commons-lang")
        self.assertEqual(p.version, "2.6")
        self.assertNotEqual(p.artifactId, "commons-parent")
        self.assertNotEqual(p.groupId, "org.apache.commons")
        self.assertNotEqual(p.version, "17")
        self.assertEqual(p.packaging, None)

    @pomfile("xmlrpc.pom")
    def test_parent_pom(self, p):
        self.assertEqual(p.packaging, "pom")
        self.assertEqual(p.groupId, "org.apache.xmlrpc")
        self.assertEqual(p.artifactId, "xmlrpc")
        self.assertEqual(p.version, "3.1.3")

    @pomfile("xmlrpc-nons.pom")
    def test_no_xmlns(self, p):
        self.assertEqual(p.packaging, "pom")
        self.assertEqual(p.groupId, "org.apache.xmlrpc")
        self.assertEqual(p.artifactId, "xmlrpc")
        self.assertEqual(p.version, "3.1.3")

    @pomfile("parent-version.pom")
    def test_parent_version(self, p):
        self.assertEqual(p.packaging, None)
        self.assertEqual(p.groupId, "commons-lang")
        self.assertEqual(p.artifactId, "commons-lang")
        self.assertEqual(p.version, "17")

    @exception_expected(lxml.etree.XMLSyntaxError)
    @pomfile("unparsable_xml.pom")
    def test_unparsable_xml(self, p):
        self.fail("Unparsable xml successfully parsed")

    @exception_expected(PomLoadingException)
    @pomfile("junit-broken-subnode.pom")
    def test_pom_broken_subnode(self, p):
        p.version
        self.fail("Broken POM succesfully loaded")

    @pomfile("junit-comments.pom")
    def test_pom_comments(self, p):
        self.assertEqual(p.packaging, None)
        self.assertEqual(p.groupId, "junit")
        self.assertEqual(p.artifactId, "junit")
        self.assertEqual(p.version, "4.11")

    @pomfile("ivy-simple.xml")
    def test_ivy_module(self, p):
        self.assertEqual(p.packaging, "ivy")
        self.assertEqual(p.groupId, "org.apache")
        self.assertEqual(p.artifactId, "hello-ivy")
        self.assertEqual(p.version, "1.2.3")


if __name__ == '__main__':
    unittest.main()
