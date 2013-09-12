import unittest
import shutil
from test_common import *

class TestMvnpackage(unittest.TestCase):

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

    @xmvnconfig('package', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('package', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('package',['aaa:bbb', 'pack', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'simple'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'simple'))

    @xmvnconfig('package',['aaa:bbb:1.2', 'pack', ])
    def test_version(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'version'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'version'))

    @xmvnconfig('package',['aaa:bbb:ccc', 'pack', ])
    def test_extension(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'extension'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'extension'))

    @xmvnconfig('package',['aaa:bbb:ccc:ddd', 'pack', ])
    def test_classifier(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'classifier'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'classifier'))

    @xmvnconfig('package',['aaa:bbb:ccc:ddd:21', 'pack', ])
    def test_all(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'all'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'all'))

    @xmvnconfig('package',[':bbb', 'pack', ])
    def test_wildcard1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'wildcard1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'wildcard1'))

    @xmvnconfig('package',[':', 'pack', ])
    def test_wildcard2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'wildcard2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'wildcard2'))

    @xmvnconfig('package',['*:*', 'pack', ])
    def test_wildcard3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'wildcard3'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'wildcard3'))

    @xmvnconfig('package',[':bbb-{a,b,c}', 'pack', ])
    def test_braces1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'braces1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'braces1'))

    @xmvnconfig('package',['a-{b,c}:{x,y}-z', 'pack', ])
    def test_braces2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'braces2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'braces2'))

    @xmvnconfig('package',['aaa:bbb', ])
    def test_single(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('package',['aaa:bbb', 'pack', 'evil', ])
    def test_more(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('package',[':bbb-{a,b', 'pack', ])
    def test_odd_braces(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('package',[':bb-a,b}', 'pack', ])
    def test_odd_braces1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('package',['a-{b,c}:{x,y}-z', '@2', ])
    def test_backref1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'backref1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'backref1'))

    @xmvnconfig('package',['a-{b,c}:{x,y}-z', '@1', ])
    def test_backref2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('package', 'backref2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'package', 'backref2'))

    @xmvnconfig('package',['a:b', '@1', ])
    def test_backref3(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('package',['a-{b,c}:x', '@3', ])
    def test_backref4(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

if __name__ == '__main__':
    unittest.main()
