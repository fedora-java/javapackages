import unittest
import shutil
from test_common import *

class TestMvnbuild(unittest.TestCase):

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

    @xmvnconfig('build', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('build', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('build',[])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'run_no_args'))

    @xmvnconfig('build',['-b', ])
    def test_bootstrap(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'bootstrap'))

    @xmvnconfig('build',['-d', ])
    def test_xmvn_debug(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'xmvn_debug'))

    @xmvnconfig('build',['-d', ])
    def test_xmvn_debug1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('build', 'xmvn_debug1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'build', 'xmvn_debug1'))

    @xmvnconfig('build',['-f', ])
    def test_force(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'force'))

    @xmvnconfig('build',['-f', ])
    def test_force1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('build', 'force1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'build', 'force1'))

    @xmvnconfig('build',['-g', ])
    def test_goal_before(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'goal_before'))

    @xmvnconfig('build',['-G', ])
    def test_goal_after(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'goal_after'))

    @xmvnconfig('build',['-i', ])
    def test_skip_install(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'skip_install'))

    @xmvnconfig('build',['-j', ])
    def test_skip_javadoc(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'skip_javadoc'))

    @xmvnconfig('build',['-s', ])
    def test_singleton(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'singleton'))

    @xmvnconfig('build',['-s', ])
    def test_singleton1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('build', 'singleton1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'build', 'singleton1'))

    @xmvnconfig('build',['-X', ])
    def test_debug(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(get_actual_args(), get_expected_args('build', 'debug'))

    @xmvnconfig('build',['-X', ])
    def test_debug1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), get_expected_file_count('build', 'debug1'))
        for file in filelist:
            self.assertEquals(get_actual_config(file), get_expected_config(file, 'build', 'debug1'))

if __name__ == '__main__':
    unittest.main()
