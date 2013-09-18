import unittest
import shutil
from test_common import *

class TestMvnalias(unittest.TestCase):

    def setUp(self):
        try:
            shutil.rmtree(".xmvn/")
        except OSError:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(".xmvn/")
        except OSError:
            pass

    @xmvnconfig('alias', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('alias', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('alias',['aaa:bbb', 'xxx:yyy', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'simple'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'simple'))

    @xmvnconfig('alias',['aaa:bbb', 'xxx:yyy:1.2', ])
    def test_version(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'version'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'version'))

    @xmvnconfig('alias',['aaa:bbb', 'xxx:yyy:zzz:', ])
    def test_extension(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'extension'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'extension'))

    @xmvnconfig('alias',['aaa:bbb', 'xxx:yyy:zzz:www:', ])
    def test_classifier(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'classifier'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'classifier'))

    @xmvnconfig('alias',['aaa:bbb:3.1', 'xxx:yyy:zzz:3.0', ])
    def test_comb1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'comb1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'comb1'))

    @xmvnconfig('alias',['aaa:bbb:ccc:ddd:2.1', 'xxx:yyy:', ])
    def test_comb2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'comb2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'comb2'))

    @xmvnconfig('alias',['aaa:bbb:ccc:', 'xxx:yyy:zzz:www:2.1', ])
    def test_comb3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'comb3'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'comb3'))

    @xmvnconfig('alias',['aaa:bbb:ccc:4.1', 'xxx:yyy:zzz:', ])
    def test_comb4(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'comb4'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'comb4'))

    @xmvnconfig('alias',['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb:ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd:1111111111111111111111111111111111111', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy:zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz:wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww:33333333333333333333333333333333333333333333', ])
    def test_longopt(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'longopt'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'longopt'))

    @xmvnconfig('alias',['*:aaa', 'xxx:yyy', ])
    def test_wildcard1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'wildcard1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'wildcard1'))

    @xmvnconfig('alias',[':aaa', 'xxx:yyy', ])
    def test_wildcard2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'wildcard2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'wildcard2'))

    @xmvnconfig('alias',['aaa::ccc', 'xxx:yyy', ])
    def test_wildcard3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'wildcard3'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'wildcard3'))

    @xmvnconfig('alias',['aaa:bbb', ])
    def test_one_argument(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',['aaa:bbb', 'xxx', ])
    def test_invalid1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',['aaa', 'xxx:yyy', ])
    def test_invalid2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',['aaa:bbb', 'xxx:', ])
    def test_wildcard4(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'wildcard4'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'wildcard4'))

    @xmvnconfig('alias',['a:b:c:d:e:f', 'x:y', ])
    def test_invalid5(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',['a:b', 'x:y:z:w:1:e', ])
    def test_invalid6(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',['aaa:bbb', 'ccc:ddd', 'eee:fff', 'ggg:hhh', ])
    def test_multi(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'multi'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'multi'))

    @xmvnconfig('alias',['aaa:bbb', 'ccc:ddd', 'eee:fff', ])
    def test_odd(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'odd'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'odd'))

    @xmvnconfig('alias',[':', ':', ])
    def test_wildcard7(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',['x:y', 'a:b:c:*:1', ])
    def test_wildcard8(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',['x:y', 'a:b:c::1', ])
    def test_wildcard9(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'wildcard9'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'wildcard9'))

    @xmvnconfig('alias',['*:{aaa,bbb}*', ':@1', ])
    def test_backref(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'backref'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'backref'))

    @xmvnconfig('alias',['aaa', ':@1', ])
    def test_backref1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',['{aa,bb}:{cc,dd}', '@1:@2', ])
    def test_backref2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('alias', 'backref2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'alias', 'backref2'))

    @xmvnconfig('alias',[':{aaa,bbb}', '@1:@2', ])
    def test_backref3(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',[':{aaa,bbb', '@1', ])
    def test_odd_braces1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',[':{aaa,bbb}}', '@1', ])
    def test_odd_braces2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('alias',['{aaa:bbb}:ccc', '@1', ])
    def test_braces(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

if __name__ == '__main__':
    unittest.main()
