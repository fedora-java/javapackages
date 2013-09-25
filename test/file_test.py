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

    @xmvnconfig('file', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('file', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('file',['x', ])
    def test_single(self, stdout, stderr, return_value):
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

    @xmvnconfig('file',['a:b:c:', 'file', ])
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

    @xmvnconfig('file',['a', 'file', ])
    def test_invalid1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('file',['a:b:c:d:e:f', 'file', ])
    def test_invalid2(self, stdout, stderr, return_value):
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

    @xmvnconfig('file',['a::c:', 'sym', ])
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

    @xmvnconfig('file',[':{aa,bb}', '@1', ])
    def test_backref(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'backref'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'backref'))

    @xmvnconfig('file',['{aa,bb}:{cc,dd}', '@2', '@1', ])
    def test_backref1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'backref1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'backref1'))

    @xmvnconfig('file',[':a', '@1', ])
    def test_backref2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('file',[':{a,b}', '@1', '@4', ])
    def test_backref3(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('file',['{aa,bb}:{x,y', '@1', ])
    def test_odd_braces1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('file',['{aa,bb}:{x,y}}', '@1', ])
    def test_odd_braces2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('file',['a:b', 'a/file1', ])
    def test_relative1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'relative1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'relative1'))

    @xmvnconfig('file',['a:b', '../file1', ])
    def test_relative2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'relative2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'relative2'))

    @xmvnconfig('file',['a:{bb,cc}', 'a/@1', ])
    def test_relative3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'relative3'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'relative3'))

    @xmvnconfig('file',['a:b', '/usr/share/java/sym', ])
    def test_absolute1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'absolute1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'absolute1'))

    @xmvnconfig('file',['-p', '/usr/share/', 'a:b', '/usr/share/sym', ])
    def test_prefix1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'prefix1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'prefix1'))

    @xmvnconfig('file',['-p', '/usr', 'a:b', '/usr/share/sym', ])
    def test_prefix2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('file', 'prefix2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'file', 'prefix2'))

if __name__ == '__main__':
    unittest.main()
