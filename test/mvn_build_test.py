import unittest
import shutil
from test_common import *

class TestMvnmvn_build(unittest.TestCase):

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

    @xmvnconfig('mvn_build', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('mvn_build', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('mvn_build',[])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'run_no_args'))

    @xmvnconfig('mvn_build',['-b', ])
    def test_bootstrap(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'bootstrap'))

    @xmvnconfig('mvn_build',['-d', ])
    def test_xmvn_debug(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'xmvn_debug'))

    @xmvnconfig('mvn_build',['-d', ])
    def test_xmvn_debug1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_build', 'xmvn_debug1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_build', 'xmvn_debug1'))

    @xmvnconfig('mvn_build',['-f', ])
    def test_force(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'force'))

    @xmvnconfig('mvn_build',['-f', ])
    def test_force1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_build', 'force1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_build', 'force1'))

    @xmvnconfig('mvn_build',['-g', ])
    def test_goal_before(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'goal_before'))

    @xmvnconfig('mvn_build',['-G', ])
    def test_goal_after(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'goal_after'))

    @xmvnconfig('mvn_build',['-i', ])
    def test_skip_install(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'skip_install'))

    @xmvnconfig('mvn_build',['-j', ])
    def test_skip_javadoc(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'skip_javadoc'))

    @xmvnconfig('mvn_build',['-s', ])
    def test_singleton(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'singleton'))

    @xmvnconfig('mvn_build',['-s', ])
    def test_singleton1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_build', 'singleton1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_build', 'singleton1'))

    @xmvnconfig('mvn_build',['-X', ])
    def test_debug(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'debug'))

    @xmvnconfig('mvn_build',['-X', ])
    def test_debug1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_build', 'debug1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_build', 'debug1'))

    @xmvnconfig('mvn_build',['-ji', ])
    def test_skip_both(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'skip_both'))

    @xmvnconfig('mvn_build',['-n', 'pkgname', ])
    def test_name(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_build', 'name'))

        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_build', 'name'))


    @xmvnconfig('mvn_build',['-dfijsX', ])
    def test_all(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('mvn_build', 'all'))

    @xmvnconfig('mvn_build',['-dfijsX', ])
    def test_all1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('mvn_build', 'all1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'mvn_build', 'all1'))

if __name__ == '__main__':
    unittest.main()
