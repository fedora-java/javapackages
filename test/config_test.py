import unittest
from test_common import *

class TestMvnconfig(ScriptTest, unittest.TestCase):
    def path(self):
        return "../java-utils/mvn_config.py"

    def test_single(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['aaa', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_more(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['a', 'b', 'c', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @compareXmvnConfig(['aaa', 'bbb', ])
    def test_simple(self):
        pass

    @compareXmvnConfig(['a/b/c', 'xxx', ])
    def test_path(self):
        pass

if __name__ == '__main__':
    unittest.main()
