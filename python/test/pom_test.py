import os
import unittest

from javapackages import POM

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
        self.assertIsNone(p.packaging)

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



if __name__ == '__main__':
    unittest.main()
