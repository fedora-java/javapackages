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

    def test_run_no_args(self):
        (out, err, ret) = call_script("compat_version", [])
        self.assertNotEqual(ret, 0)
        self.assertEqual("Usage:", err[:6])

    def test_help(self):
        (out, err, ret) = call_script("compat_version", ['-h'])
        self.assertTrue(out)

    @xmvnconfig('compat_version',['aaa:bbb', '1', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('compat_version', 'simple'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'compat_version', 'simple'))

    def test_single(self):
        (stdout, stderr, return_value) = call_script('compat_version', ['aaa:bbb', ])
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

if __name__ == '__main__':
    unittest.main()
