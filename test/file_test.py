import unittest
from test_common import *

class TestMvnfile(ScriptTest, unittest.TestCase):
    def path(self):
        return "../java-utils/mvn_file.py"

    def test_single(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['x', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @compareXmvnConfig([':x', 'file', ])
    def test_simple(self):
        pass

    @compareXmvnConfig([':guice', 'google/guice', 'guice', ])
    def test_symlink(self):
        pass

    @compareXmvnConfig(['a:b', 'file', ])
    def test_group(self):
        pass

    @compareXmvnConfig([':a:1.3', 'file', ])
    def test_version(self):
        pass

    @compareXmvnConfig(['a:b:c', 'file', ])
    def test_extension(self):
        pass

    @compareXmvnConfig(['*:a', 'file', ])
    def test_wildcard(self):
        pass

    def test_invalid1(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['a', 'file', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_invalid2(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['a:b:c:d:e:f', 'file', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @compareXmvnConfig([':a', 'file', 'sym1', 'sym2', 'sym3', ])
    def test_symlinks(self):
        pass

    @compareXmvnConfig(['a:b:c:d:1', 'sym', ])
    def test_classifier(self):
        pass

    @compareXmvnConfig(['a::c', 'sym', ])
    def test_wildcard2(self):
        pass

    @compareXmvnConfig(['a:b', 'sym1', 'sym2', 'sym3', 'sym4', 'sym5', 'sym6', 'sym7', 'sym8', 'sym9', 'sym10', 'sym11', 'sym12', 'sym13', 'sym14', 'sym15', 'sym16', 'sym17', 'sym18', 'sym19', 'sym20', 'sym21', ])
    def test_more_symlinks(self):
        pass

if __name__ == '__main__':
    unittest.main()
