import unittest
import shutil
from test_common import *

class TestMvnconfig(unittest.TestCase):

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
        (out, err, ret) = call_script("config", [])
        self.assertNotEqual(ret, 0)
        self.assertEqual("Usage:", err[:6])

    def test_help(self):
        (out, err, ret) = call_script("config", ['-h'])
        self.assertTrue(out)

    def test_single(self):
        (stdout, stderr, return_value) = call_script('config', ['aaa', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_more(self):
        (stdout, stderr, return_value) = call_script('config', ['a', 'b', 'c', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('config',['aaa', 'bbb', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('config', 'simple'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'config', 'simple'))

    @xmvnconfig('config',['a/b/c', 'xxx', ])
    def test_path(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('config', 'path'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'config', 'path'))

if __name__ == '__main__':
    unittest.main()
