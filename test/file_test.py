import unittest
import shutil
from test_common import *

class TestMvnfile(unittest.TestCase):

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
        (out, err, ret) = call_script("file", [])
        self.assertNotEqual(ret, 0)
        self.assertEqual("Usage:", err[:6])

    def test_help(self):
        (out, err, ret) = call_script("file", ['-h'])
        self.assertTrue(out)

    def test_single(self):
        (stdout, stderr, return_value) = call_script('file', ['x', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('file',[':x', 'file', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'simple'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'simple'))

    @xmvnconfig('file',[':guice', 'google/guice', 'guice', ])
    def test_symlink(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'symlink'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'symlink'))

    @xmvnconfig('file',['a:b', 'file', ])
    def test_group(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'group'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'group'))

    @xmvnconfig('file',[':a:1.3', 'file', ])
    def test_version(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'version'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'version'))

    @xmvnconfig('file',['a:b:c', 'file', ])
    def test_extension(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'extension'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'extension'))

    @xmvnconfig('file',['*:a', 'file', ])
    def test_wildcard(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'wildcard'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'wildcard'))

    def test_invalid1(self):
        (stdout, stderr, return_value) = call_script('file', ['a', 'file', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    def test_invalid2(self):
        (stdout, stderr, return_value) = call_script('file', ['a:b:c:d:e:f', 'file', ])
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('file',[':a', 'file', 'sym1', 'sym2', 'sym3', ])
    def test_symlinks(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'symlinks'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'symlinks'))

    @xmvnconfig('file',['a:b:c:d:1', 'sym', ])
    def test_classifier(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'classifier'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'classifier'))

    @xmvnconfig('file',['a::c', 'sym', ])
    def test_wildcard2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'wildcard2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'wildcard2'))

    @xmvnconfig('file',['a:b', 'sym1', 'sym2', 'sym3', 'sym4', 'sym5', 'sym6', 'sym7', 'sym8', 'sym9', 'sym10', 'sym11', 'sym12', 'sym13', 'sym14', 'sym15', 'sym16', 'sym17', 'sym18', 'sym19', 'sym20', 'sym21', ])
    def test_more_symlinks(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'more_symlinks'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'more_symlinks'))

if __name__ == '__main__':
    unittest.main()
