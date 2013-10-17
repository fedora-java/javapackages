import unittest
import shutil
import os
from test_common import xmvnconfig, get_config_file_list, \
        get_actual_config, get_expected_config, DIRPATH

from xml_compare import compare_xml_files

class TestMvnConfig(unittest.TestCase):

    maxDiff = 2048

    def setUp(self):
        self.olddir = os.getcwd()
        self.workdir = os.path.join(DIRPATH, 'workdir')
        os.mkdir(self.workdir)
        os.chdir(self.workdir)

    def tearDown(self):
        try:
            shutil.rmtree(self.workdir)
        except OSError:
            pass
        os.chdir(self.olddir)

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
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'simple'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a/b/c', 'xxx', ])
    def test_path(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'path'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b/>', ])
    def test_xml1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'xml1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b>c</b>', ])
    def test_xml2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'xml2'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b>c</b><d/>', ])
    def test_xml3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'xml3'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b>c</b><d>e</d>', ])
    def test_xml4(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'xml4'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b><c>d</c></b>', ])
    def test_nested_xml1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'nested_xml1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b><c>d</c>d</b>', ])
    def test_nested_xml2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'nested_xml2'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

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
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'entity'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', 'f<b>c</b>d', ])
    def test_mixed(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_config', 'mixed'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

if __name__ == '__main__':
    unittest.main()
