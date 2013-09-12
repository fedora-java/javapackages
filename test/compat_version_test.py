import unittest
import shutil
from test_common import *

class TestMvncompat_version(unittest.TestCase):

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

    @xmvnconfig('compat_version', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('compat_version', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('compat_version',['aaa:bbb', '1', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('compat_version', 'simple'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'compat_version', 'simple'))

    @xmvnconfig('compat_version',['aaa:bbb', ])
    def test_single(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('compat_version',['aaa:bbb', '1', '2', '3', ])
    def test_more(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('compat_version', 'more'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'compat_version', 'more'))

    @xmvnconfig('compat_version',['aaa:bbb:ccc:ddd:1.2', '3.1', ])
    def test_version(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('compat_version', 'version'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'compat_version', 'version'))

    @xmvnconfig('compat_version',[':bbb', '2', ])
    def test_wildcard(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('compat_version', 'wildcard'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'compat_version', 'wildcard'))

    @xmvnconfig('compat_version',['aa:bb:{1,2}', '@1', ])
    def test_backref1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('compat_version', 'backref1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'compat_version', 'backref1'))

    @xmvnconfig('compat_version',['aaa:bb:{1,2}', '@3', ])
    def test_backref2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('compat_version',['aaa:bbb:{1,2', '@1', ])
    def test_odd_braces1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('compat_version',['aaa:bbb:1,2}', '@3', ])
    def test_odd_braces2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

if __name__ == '__main__':
    unittest.main()
