import unittest
import shutil
from test_common import *

class TestMvnmvn_package(unittest.TestCase):

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

    @xmvnconfig('mvn_package', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('mvn_package', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('mvn_package',['aaa:bbb', 'pack', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'simple'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'simple'))

    @xmvnconfig('mvn_package',['aaa:bbb:1.2', 'pack', ])
    def test_version(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'version'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'version'))

    @xmvnconfig('mvn_package',['aaa:bbb:ccc:', 'pack', ])
    def test_extension(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'extension'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'extension'))

    @xmvnconfig('mvn_package',['aaa:bbb:ccc:ddd:', 'pack', ])
    def test_classifier(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'classifier'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'classifier'))

    @xmvnconfig('mvn_package',['aaa:bbb:ccc:ddd:21', 'pack', ])
    def test_all(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'all'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'all'))

    @xmvnconfig('mvn_package',[':bbb', 'pack', ])
    def test_wildcard1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'wildcard1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'wildcard1'))

    @xmvnconfig('mvn_package',[':', 'pack', ])
    def test_wildcard2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'wildcard2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'wildcard2'))

    @xmvnconfig('mvn_package',['*:*', 'pack', ])
    def test_wildcard3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'wildcard3'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'wildcard3'))

    @xmvnconfig('mvn_package',[':bbb-{a,b,c}', 'pack', ])
    def test_braces1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'braces1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'braces1'))

    @xmvnconfig('mvn_package',['a-{b,c}:{x,y}-z', 'pack', ])
    def test_braces2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'braces2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'braces2'))

    @xmvnconfig('mvn_package',['aaa:bbb', ])
    def test_single(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_package',['aaa:bbb', 'pack', 'evil', ])
    def test_more(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_package',[':bbb-{a,b', 'pack', ])
    def test_odd_braces(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_package',[':bb-a,b}', 'pack', ])
    def test_odd_braces1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_package',['a-{b,c}:{x,y}-z', '@2', ])
    def test_backref1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'backref1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'backref1'))

    @xmvnconfig('mvn_package',['a-{b,c}:{x,y}-z', '@1', ])
    def test_backref2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'backref2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'backref2'))

    @xmvnconfig('mvn_package',['a:b', '@1', ])
    def test_backref3(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_package',['a-{b,c}:x', '@3', ])
    def test_backref4(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_package',['aaa:bbb', '__noinstall', ])
    def test_noinstall(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_package', 'noinstall'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_package', 'noinstall'))

if __name__ == '__main__':
    unittest.main()
