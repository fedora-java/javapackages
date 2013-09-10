import unittest
from test_common import *

class TestMvnpackage(ScriptTest, unittest.TestCase):
    def path(self):
        return "../java-utils/mvn_package.py"

    @compareXmvnConfig(['aaa:bbb', 'pack', ])
    def test_simple(self):
        pass

    @compareXmvnConfig(['aaa:bbb:1.2', 'pack', ])
    def test_version(self):
        pass

    @compareXmvnConfig(['aaa:bbb:ccc', 'pack', ])
    def test_extension(self):
        pass

    @compareXmvnConfig(['aaa:bbb:ccc:ddd', 'pack', ])
    def test_classifier(self):
        pass

    @compareXmvnConfig(['aaa:bbb:ccc:ddd:21', 'pack', ])
    def test_all(self):
        pass

    @compareXmvnConfig([':bbb', 'pack', ])
    def test_wildcard1(self):
        pass

    @compareXmvnConfig([':', 'pack', ])
    def test_wildcard2(self):
        pass

    @compareXmvnConfig(['*:*', 'pack', ])
    def test_wildcard3(self):
        pass

    @compareXmvnConfig([':bbb-{a,b,c}', 'pack', ])
    def test_braces1(self):
        pass

    @compareXmvnConfig(['a-{b,c}:{x,y}-z', 'pack', ])
    def test_braces2(self):
        pass

    def test_single(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['aaa:bbb', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_more(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['aaa:bbb', 'pack', 'evil', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

if __name__ == '__main__':
    unittest.main()
