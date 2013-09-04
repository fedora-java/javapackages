import unittest
from test_common import *

class TestMvnalias(ScriptTest, unittest.TestCase):
    def path(self):
        return "../java-utils/mvn_alias.py"

    @compareXmvnConfig(['aaa:bbb', 'xxx:yyy', ])
    def test_simple(self):
        pass

    @compareXmvnConfig(['aaa:bbb', 'xxx:yyy:1.2', ])
    def test_version(self):
        pass

    @compareXmvnConfig(['aaa:bbb', 'xxx:yyy:zzz', ])
    def test_extension(self):
        pass

    @compareXmvnConfig(['aaa:bbb', 'xxx:yyy:zzz:www', ])
    def test_classifier(self):
        pass

    @compareXmvnConfig(['aaa:bbb:3.1', 'xxx:yyy:zzz:3.0', ])
    def test_comb1(self):
        pass

    @compareXmvnConfig(['aaa:bbb:ccc:ddd:2.1', 'xxx:yyy', ])
    def test_comb2(self):
        pass

    @compareXmvnConfig(['aaa:bbb:ccc', 'xxx:yyy:zzz:www:2.1', ])
    def test_comb3(self):
        pass

    @compareXmvnConfig(['aaa:bbb:ccc:4.1', 'xxx:yyy:zzz', ])
    def test_comb4(self):
        pass

    @compareXmvnConfig(['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb:ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd:1111111111111111111111111111111111111', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy:zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz:wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww:33333333333333333333333333333333333333333333', ])
    def test_longopt(self):
        pass

    @compareXmvnConfig(['*:aaa', 'xxx:yyy', ])
    def test_wildcard1(self):
        pass

    @compareXmvnConfig([':aaa', 'xxx:yyy', ])
    def test_wildcard2(self):
        pass

    @compareXmvnConfig(['aaa::ccc', 'xxx:yyy', ])
    def test_wildcard3(self):
        pass

    def test_one_argument(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['aaa:bbb', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_invalid1(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['aaa:bbb', 'xxx', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_invalid2(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['aaa', 'xxx:yyy', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_wildcard4(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['aaa:bbb', 'xxx:', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_invalid5(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['a:b:c:d:e:f', 'x:y', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_invalid6(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['a:b', 'x:y:z:w:1:e', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @compareXmvnConfig(['aaa:bbb', 'ccc:ddd', 'eee:fff', 'ggg:hhh', ])
    def test_multi(self):
        pass

    @compareXmvnConfig(['aaa:bbb', 'ccc:ddd', 'eee:fff', ])
    def test_odd(self):
        pass

    def test_wildcard7(self):
        (stdout, stderr, return_value) = callScript(self.path(), [':', ':', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_wildcard8(self):
        (stdout, stderr, return_value) = callScript(self.path(), ['x:y', 'a:b:c:*:1', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

if __name__ == '__main__':
    unittest.main()
