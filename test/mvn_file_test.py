import unittest
import shutil
import os
from test_common import xmvnconfig, get_config_file_list, \
        get_actual_config, get_expected_config, DIRPATH

from xml_compare import compare_xml_files

class TestMvnFile(unittest.TestCase):

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

    @xmvnconfig('mvn_file', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('mvn_file', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('mvn_file',['x', ])
    def test_single(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_file',[':x', 'file', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'simple'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',[':guice', 'google/guice', 'guice', ])
    def test_symlink(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'symlink'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['a:b', 'file', ])
    def test_group(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'group'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',[':a:1.3', 'file', ])
    def test_version(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'version'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['a:b:c:', 'file', ])
    def test_extension(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'extension'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['*:a', 'file', ])
    def test_wildcard(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'wildcard'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['a', 'file', ])
    def test_invalid1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_file',['a:b:c:d:e:f', 'file', ])
    def test_invalid2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_file',[':a', 'file', 'sym1', 'sym2', 'sym3', ])
    def test_symlinks(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'symlinks'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['a:b:c:d:1', 'sym', ])
    def test_classifier(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'classifier'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['a::c:', 'sym', ])
    def test_wildcard2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'wildcard2'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['a:b', 'sym1', 'sym2', 'sym3', 'sym4', 'sym5',
        'sym6', 'sym7', 'sym8', 'sym9', 'sym10', 'sym11', 'sym12', 'sym13',
        'sym14', 'sym15', 'sym16', 'sym17', 'sym18', 'sym19', 'sym20', 'sym21'])
    def test_more_symlinks(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'more_symlinks'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',[':{aa,bb}', '@1', ])
    def test_backref(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'backref'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['{aa,bb}:{cc,dd}', '@2', '@1', ])
    def test_backref1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'backref1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',[':a', '@1', ])
    def test_backref2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_file',[':{a,b}', '@1', '@4', ])
    def test_backref3(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_file',['{aa,bb}:{x,y', '@1', ])
    def test_odd_braces1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_file',['{aa,bb}:{x,y}}', '@1', ])
    def test_odd_braces2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_file',['a:b', 'a/file1', ])
    def test_relative1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'relative1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['a:b', '../file1', ])
    def test_relative2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'relative2'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['a:{bb,cc}', 'a/@1', ])
    def test_relative3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'relative3'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['a:b', '/usr/share/java/sym', ])
    def test_absolute1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'absolute1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['-p', '/usr/share/', 'a:b', '/usr/share/sym', ])
    def test_prefix1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'prefix1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_file',['-p', '/usr', 'a:b', '/usr/share/sym', ])
    def test_prefix2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_file', 'prefix2'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

if __name__ == '__main__':
    unittest.main()
