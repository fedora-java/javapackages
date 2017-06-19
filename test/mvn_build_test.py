import unittest
import shutil
import os
import sys
import subprocess
from test_common import javautils_script, get_actual_args, get_expected_args, \
        get_config_file_list, get_actual_config, get_expected_config, DIRPATH
from xml_compare import compare_xml_files

class TestMvnBuild(unittest.TestCase):

    maxDiff = 2048

    def setUp(self):
        self.olddir = os.getcwd()
        self.workdir = os.path.join(DIRPATH, 'workdir')
        os.mkdir(self.workdir)
        os.chdir(self.workdir)

        # copy the xml file for test_builddep_compression test case
        builddep_xml = os.path.join(DIRPATH, 'data', 'mvn_build', 'xmvn-builddep.xml')
        builddep_file = os.path.join(self.workdir, '.xmvn-builddep')
        shutil.copy(builddep_xml, builddep_file)

        # copy xmvn-builddep script and replace '@' denoted variables
        # with correct path to the resources
        original_script = os.path.join(DIRPATH, '..', 'bin', 'xmvn-builddep')
        self.script = os.path.join(self.workdir, 'script')
        shutil.copy2(original_script, self.script) # used so file is still executable
        builddep_py = os.path.join(DIRPATH, '..', 'java-utils', 'builddep.py')
        with open(self.script, "wt") as wf: 
            with open(original_script, "rt") as rf: 
                for line in rf:
                    if (line.find('@') > -1): 
                        line.replace("@{pyinterpreter}", sys.executable)
                        line.replace("@{javadir}-utils/builddep.py", builddep_py)
                    wf.write(line)

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

    @javautils_script('mvn_build',[])
    def test_builddep_compression(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual(get_actual_args(),
                get_expected_args('mvn_build', 'run_no_args'))

        log_path = os.path.join(self.workdir, "tmpbuild.log")
        with open(log_path, 'w') as outfile:
            outfile.write(stdout)

        with open("tmpout", 'w') as outfile:
            with open("tmperr", 'w') as errfile:
                p = subprocess.Popen([self.script, log_path],
                                     shell=True,
                                     stdout=outfile,
                                     stderr=errfile,
                                     universal_newlines=True)
                return_value = p.wait()

        with open("tmpout", 'r') as outfile:
            out = outfile.read()
        with open("tmperr", 'r') as errfile:
            err = errfile.read()
        os.remove('tmpout')
        os.remove('tmperr')

        builddep_res = os.path.join(DIRPATH, 'data', 'mvn_build', 'builddep.result')
        result = ""
        with open(builddep_res, 'rt') as rf:
            result = rf.read()

        self.assertEqual(return_value, 0, err)
        self.assertEqual(out, result,
                          "expected:\n---\n" 
                        + result + "\ngained:\n---\n"
                        + out + "\nparsed from output:\n---\n"
                        + stdout)
        self.assertEqual(err, "", err)

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

if __name__ == '__main__':
    unittest.main()
