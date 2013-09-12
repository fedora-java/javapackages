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

    @xmvnconfig('config', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('config', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('config',['aaa', ])
    def test_single(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('config',['a', 'b', 'c', ])
    def test_more(self, stdout, stderr, return_value):
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
