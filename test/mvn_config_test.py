import unittest
import shutil
from test_common import *

class TestMvnmvn_config(unittest.TestCase):

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

    @xmvnconfig('mvn_config', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('mvn_config', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('mvn_config',['aaa', ])
    def test_single(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', 'b', 'c', ])
    def test_more(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['aaa', 'bbb', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'simple'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'simple'))

    @xmvnconfig('mvn_config',['a/b/c', 'xxx', ])
    def test_path(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'path'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'path'))

    @xmvnconfig('mvn_config',['a', '<b/>', ])
    def test_xml1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'xml1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'xml1'))

    @xmvnconfig('mvn_config',['a', '<b>c</b>', ])
    def test_xml2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'xml2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'xml2'))

    @xmvnconfig('mvn_config',['a', '<b>c</b><d/>', ])
    def test_xml3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'xml3'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'xml3'))

    @xmvnconfig('mvn_config',['a', '<b>c</b><d>e</d>', ])
    def test_xml4(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'xml4'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'xml4'))

    @xmvnconfig('mvn_config',['a', '<b><c>d</c></b>', ])
    def test_nested_xml1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'nested_xml1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'nested_xml1'))

    @xmvnconfig('mvn_config',['a', '<b><c>d</c>d</b>', ])
    def test_nested_xml2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'nested_xml2'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'nested_xml2'))

    @xmvnconfig('mvn_config',['a', '<b', ])
    def test_invalid_xml1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', '<b>', ])
    def test_invalid_xml2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', '<b><c></b>', ])
    def test_invalid_xml3(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', '<b></c></b>', ])
    def test_invalid_xml4(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', '<b>c&lt;d</b>', ])
    def test_entity(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'entity'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'entity'))

    @xmvnconfig('mvn_config',['a', 'f<b>c</b>d', ])
    def test_mixed(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_config', 'mixed'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_config', 'mixed'))

if __name__ == '__main__':
    unittest.main()
