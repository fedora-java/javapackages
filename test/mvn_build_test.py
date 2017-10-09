import unittest
import shutil
import os
from test_common import javautils_script, get_actual_args, get_expected_args, \
        get_config_file_list, get_actual_config, get_expected_config, DIRPATH, \
        get_actual_env
from xml_compare import compare_xml_files
from textwrap import dedent

class TestMvnBuild(unittest.TestCase):

    maxDiff = 2048

    def setUp(self):
        self.olddir = os.getcwd()
        self.workdir = os.path.join(DIRPATH, 'workdir')
        shutil.rmtree(self.workdir, ignore_errors=True)
        os.mkdir(self.workdir)
        os.chdir(self.workdir)
        with open('gradle.properties', 'w') as props:
            props.write(dedent('''
                groovyVersion=2.4.8
                org.gradle.jvmargs=-Xmx1G -XX:asf \\
                        -XX:+\\\\asdf
            '''))


    def tearDown(self):
        try:
            shutil.rmtree(self.workdir)
        except OSError:
            pass
        os.chdir(self.olddir)

    @javautils_script('mvn_build', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @javautils_script('mvn_build',[])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'run_no_args'))

    @javautils_script('mvn_build',['-b', ])
    def test_bootstrap(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'bootstrap'))

    @javautils_script('mvn_build',['-d', ])
    def test_xmvn_debug(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'xmvn_debug'))

    @javautils_script('mvn_build',['-f', ])
    def test_force(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'force'))

    @javautils_script('mvn_build',['-f', ])
    def test_force1(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 1)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_build', 'force1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_build',['-g', 'validate'])
    def test_goal_before(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'goal_before'))

    @javautils_script('mvn_build',['-G', 'integration-test'])
    def test_goal_after(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'goal_after'))

    @javautils_script('mvn_build',['-i', ])
    def test_skip_install(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'skip_install'))

    @javautils_script('mvn_build',['-j', ])
    def test_skip_javadoc(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'skip_javadoc'))

    @javautils_script('mvn_build',['-s', ])
    def test_singleton(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'singleton'))

    @javautils_script('mvn_build',['-s', ])
    def test_singleton1(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 2)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_build', 'singleton1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_build',['-X', ])
    def test_debug(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'debug'))

    @javautils_script('mvn_build',['-ji', ])
    def test_skip_both(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'skip_both'))

    @javautils_script('mvn_build',['-dfijsX', ])
    def test_all(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'all'))

    @javautils_script('mvn_build',['-dfijsX', ])
    def test_all1(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        filelist = get_config_file_list()
        self.assertEqual(len(filelist), 3)
        for filename in filelist:
            report = compare_xml_files(get_actual_config(filename),
                 get_expected_config(filename, 'mvn_build', 'all1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @javautils_script('mvn_build',['-g', 'validate', 'compile', '-G',
                             'integration-test', 'verify'])
    def test_more_goals(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'more_goals'))

    @javautils_script('mvn_build',['--gradle'])
    def test_gradle(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual('--no-daemon --offline build xmvnInstall',
                         get_actual_args().strip())
        self.assertEqual('-Xmx1G -XX:asf -XX:+\\asdf',
                         get_actual_env('GRADLE_OPTS'))

if __name__ == '__main__':
    unittest.main()
