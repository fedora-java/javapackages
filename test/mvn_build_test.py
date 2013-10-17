import unittest
import shutil
import os
from test_common import xmvnconfig, get_actual_args, get_expected_args, \
        get_config_file_list, get_actual_config, get_expected_config, DIRPATH
from xml_compare import compare_xml_files

class TestMvnBuild(unittest.TestCase):

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

    @xmvnconfig('mvn_build', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('mvn_build',[])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'run_no_args'))

    @xmvnconfig('mvn_build',['-b', ])
    def test_bootstrap(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'bootstrap'))

    @xmvnconfig('mvn_build',['-d', ])
    def test_xmvn_debug(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'xmvn_debug'))

    @xmvnconfig('mvn_build',['-d', ])
    def test_xmvn_debug1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 2)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_build', 'xmvn_debug1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_build',['-f', ])
    def test_force(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'force'))

    @xmvnconfig('mvn_build',['-f', ])
    def test_force1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_build', 'force1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_build',['-g', ])
    def test_goal_before(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'goal_before'))

    @xmvnconfig('mvn_build',['-G', ])
    def test_goal_after(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'goal_after'))

    @xmvnconfig('mvn_build',['-i', ])
    def test_skip_install(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'skip_install'))

    @xmvnconfig('mvn_build',['-j', ])
    def test_skip_javadoc(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'skip_javadoc'))

    @xmvnconfig('mvn_build',['-s', ])
    def test_singleton(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'singleton'))

    @xmvnconfig('mvn_build',['-s', ])
    def test_singleton1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 2)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_build', 'singleton1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_build',['-X', ])
    def test_debug(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'debug'))

    @xmvnconfig('mvn_build',['-X', ])
    def test_debug1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 2)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_build', 'debug1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_build',['-ji', ])
    def test_skip_both(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'skip_both'))

    @xmvnconfig('mvn_build',['-n', 'pkgname', ])
    def test_name(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_build', 'name'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_build',['-n', 'pkgname', ])
    def test_name1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'name1'))

    @xmvnconfig('mvn_build',['-dfijsX', ])
    def test_all(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(),
                get_expected_args('mvn_build', 'all'))

    @xmvnconfig('mvn_build',['-dfijsX', ])
    def test_all1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 5)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_build', 'all1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

if __name__ == '__main__':
    unittest.main()
