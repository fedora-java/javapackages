import unittest
from test_common import *

class TestMvncompat_version(ScriptTest, unittest.TestCase):
    def path(self):
        return "../java-utils/mvn_compat_version.py"

    @compareXmvnConfig(['aaa:bbb', '1', ])
    def test_simple(self):
        pass

    def test_single(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['aaa:bbb', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @compareXmvnConfig(['aaa:bbb', '1', '2', '3', ])
    def test_more(self):
        pass

    @compareXmvnConfig(['aaa:bbb:ccc:ddd:1.2', '3.1', ])
    def test_version(self):
        pass

    @compareXmvnConfig([':bbb', '2', ])
    def test_wildcard(self):
        pass

if __name__ == '__main__':
    unittest.main()
