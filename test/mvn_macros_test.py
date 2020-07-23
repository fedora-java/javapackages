import os
import re
import shutil
import unittest

from xml_compare import compare_xml_files
from test_common import DIRPATH
from test_rpmbuild import Package

WORKDIR = os.path.join(DIRPATH, '.workdir')

unordered = ['artifactGlob', 'alias', 'compatVersions']


def rpm_test():
    def test_decorator(function):
        def test_decorated(self):
            pack = Package(function.__name__)
            function(self, pack)
        return test_decorated
    return test_decorator

class MvnMacrosTest(unittest.TestCase):
    maxDiff = 2048

    def setUp(self):
        self.olddir = os.getcwd()
        try:
            shutil.rmtree(WORKDIR)
        except OSError:
            pass
        try:
            os.mkdir(WORKDIR)
        except OSError:
            pass
        os.chdir(WORKDIR)

    def tearDown(self):
        try:
            shutil.rmtree(WORKDIR)
        except OSError:
            pass
        os.chdir(self.olddir)

    # FIXME: aliases cause trouble
    #@rpm_test()
    #def test_mvn_alias_simple(self, pack):
    #    pack.append_to_prep('%mvn_alias aaa:bbb xxx:yyy')
    #    _, stderr, return_value = pack.run_prep()
    #    self.assertEqual(return_value, 0, stderr)
    #    confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
    #    filelist = os.listdir(confpath)
    #    self.assertEqual(len(filelist), 1)
    #    actfile = os.path.join(confpath, filelist[0])
    #    expfile = os.path.join(DIRPATH, 'data', 'mvn_alias', 'simple_00001.xml')
    #    report = compare_xml_files(actfile, expfile, unordered)
    #    self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_alias_backref(self, pack):
        pack.append_to_prep("""%mvn_alias '*:{aaa,bbb}*' ':@1'""")
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEqual(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_alias',
                               'backref_00001.xml')
        report = compare_xml_files(actfile, expfile, unordered)
        self.assertEqual(report, '', report)

    #@rpm_test()
    #def test_mvn_alias_multi(self, pack):
    #    pack.append_to_prep('%mvn_alias "aaa:bbb" "ccc:ddd" \
    #                         "eee:fff" "ggg:hhh"')
    #    _, stderr, return_value = pack.run_prep()
    #    self.assertEqual(return_value, 0, stderr)
    #    confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
    #    filelist = os.listdir(confpath)
    #    self.assertEqual(len(filelist), 1)
    #    actfile = os.path.join(confpath, filelist[0])
    #    expfile = os.path.join(DIRPATH, 'data', 'mvn_alias',
    #                           'multi_00001.xml')
    #    report = compare_xml_files(actfile, expfile, unordered)
    #    self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_alias_no_args(self, pack):
        pack.append_to_prep('%mvn_alias')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_alias_single_arg(self, pack):
        pack.append_to_prep('%mvn_alias "aaa:bbb"')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    #@rpm_test()
    #def test_mvn_alias_more_invocations(self, pack):
    #    pack.append_to_prep('%mvn_alias "aaa:bbb" "ccc:ddd"')
    #    pack.append_to_prep('%mvn_alias "{xxx,yyy}:zzz" "qqq:@1"')
    #    _, stderr, return_value = pack.run_prep()
    #    self.assertEqual(return_value, 0, stderr)
    #    confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
    #    filelist = sorted(os.listdir(confpath))
    #    self.assertEqual(len(filelist), 2)
    #    for i in range(2):
    #        actfile = os.path.join(confpath, filelist[i])
    #        filename = 'more_invocations-0000{i}.xml'.format(i=i + 1)
    #        expfile = os.path.join(DIRPATH, 'data', 'mvn_alias', filename)
    #        report = compare_xml_files(actfile, expfile, unordered)
    #        self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_file_simple(self, pack):
        pack.append_to_prep('%mvn_file :x file')
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEqual(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_file', 'simple_00001.xml')
        report = compare_xml_files(actfile, expfile, unordered)
        self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_file_symlinks(self, pack):
        pack.append_to_prep('%mvn_file :a file sym1 sym2 sym3')
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEqual(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_file',
                               'symlinks_00001.xml')
        report = compare_xml_files(actfile, expfile, unordered)
        self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_file_no_args(self, pack):
        pack.append_to_prep('%mvn_file')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_file_single_arg(self, pack):
        pack.append_to_prep('%mvn_file "aaa:bbb"')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_compat_version_simple(self, pack):
        pack.append_to_prep('%mvn_compat_version aaa:bbb 1')
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEqual(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_compat_version',
                               'simple_00001.xml')
        report = compare_xml_files(actfile, expfile, unordered)
        self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_compat_version_no_args(self, pack):
        pack.append_to_prep('%mvn_compat_version')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_compat_version_single(self, pack):
        pack.append_to_prep('%mvn_compat_version "aaa:bbb"')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_package_simple(self, pack):
        pack.append_to_prep('%mvn_package aaa:bbb pack')
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEqual(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_package',
                               'simple_00001.xml')
        report = compare_xml_files(actfile, expfile, unordered)
        self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_package_no_args(self, pack):
        pack.append_to_prep('%mvn_package')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_package_single(self, pack):
        pack.append_to_prep('%mvn_package aaa:bbb')
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEqual(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_package',
                               'single_00001.xml')
        report = compare_xml_files(actfile, expfile, unordered)
        self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_config_no_args(self, pack):
        pack.append_to_prep('%mvn_config')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_config_single(self, pack):
        pack.append_to_prep('%mvn_config')
        _, stderr, return_value = pack.run_prep()
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')

    @rpm_test()
    def test_mvn_config_path(self, pack):
        pack.append_to_prep('%mvn_config a/b/c xxx')
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEqual(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_config',
                               'path_00001.xml')
        report = compare_xml_files(actfile, expfile, unordered)
        self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_config_multiline(self, pack):
        pack.append_to_prep("""%mvn_config a/b/c "
            <bla>
                bla
            </bla>
        " """)
        _, stderr, return_value = pack.run_prep()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = os.listdir(confpath)
        self.assertEqual(len(filelist), 1)
        actfile = os.path.join(confpath, filelist[0])
        expfile = os.path.join(DIRPATH, 'data', 'mvn_config',
                               'multiline_00001.xml')
        report = compare_xml_files(actfile, expfile, unordered)
        self.assertEqual(report, '', report)

    @rpm_test()
    def test_mvn_build_no_args(self, pack):
        pack.append_to_build('%mvn_build')

        _, stderr, return_value = pack.run_build()
        self.assertEqual(return_value, 0, stderr)
        argspath = os.path.join(pack.buildpath, '.xmvn', 'out')
        with open(argspath, 'r') as argsfile:
            exp = '--batch-mode --offline ' + \
                  'verify org.fedoraproject.xmvn:xmvn-mojo:install ' + \
                  'org.fedoraproject.xmvn:xmvn-mojo:javadoc ' + \
                  'org.fedoraproject.xmvn:xmvn-mojo:builddep\n'
            self.assertEqual(argsfile.read(), exp)

    @rpm_test()
    def test_mvn_build_singleton(self, pack):
        pack.append_to_build('%mvn_build -s')
        _, stderr, return_value = pack.run_build()
        self.assertEqual(return_value, 0, stderr)
        confpath = os.path.join(pack.buildpath, '.xmvn', 'config.d')
        filelist = sorted(os.listdir(confpath))
        self.assertEqual(len(filelist), 2)
        for i in range(2):
            actfile = os.path.join(confpath, filelist[i])
            filename = 'singleton_0000{i}.xml'.format(i=i + 1)
            expfile = os.path.join(DIRPATH, 'data', 'mvn_build', filename)
            report = compare_xml_files(actfile, expfile, unordered)
            self.assertEqual(report, '', report)

        expfile = os.path.join(pack.buildpath, '.xmvn', 'out')
        actfile = os.path.join(DIRPATH, 'data', 'mvn_build',
                                   'singleton_out_rpm')
        with open(actfile, 'r') as act:
            with open(expfile, 'r') as exp:
                self.assertEqual(act.read(), exp.read())

    @rpm_test()
    def test_mvn_build_environment(self, pack):
        pack.append_to_build('export MAVEN_OPTS="-Xmx1024M"')
        pack.append_to_build('%mvn_build')
        _, stderr, return_value = pack.run_build()
        self.assertEqual(return_value, 0, stderr)
        envpath = os.path.join(pack.buildpath, '.xmvn', 'env')
        with open(envpath, 'r') as envfile:
            for line in envfile:
                if line == 'MAVEN_OPTS=-Xmx1024M\n':
                    break
            else:
                self.assertTrue(False, 'Environment varible not passed to XMvn')

    @rpm_test()
    def test_mvn_build_pass_args(self, pack):
        pack.append_to_build('%mvn_build -s -- --log-file "/var/log/xmvn"')
        _, stderr, return_value = pack.run_build()
        self.assertEqual(return_value, 0, stderr)
        argspath = os.path.join(pack.buildpath, '.xmvn', 'out')
        with open(argspath, 'r') as argsfile:
            exp = '--batch-mode --offline --log-file /var/log/xmvn ' + \
                  'verify org.fedoraproject.xmvn:xmvn-mojo:install ' + \
                  'org.fedoraproject.xmvn:xmvn-mojo:javadoc ' + \
                  'org.fedoraproject.xmvn:xmvn-mojo:builddep\n'
            self.assertEqual(argsfile.read(), exp)

    @rpm_test()
    def test_mvn_build_bootstrap(self, pack):
        pack.append_to_build('%define xmvn_bootstrap true')
        pack.append_to_build('%mvn_build')

        _, stderr, return_value = pack.run_build()
        self.assertEqual(return_value, 0, stderr)
        argspath = os.path.join(pack.buildpath, '.xmvn', 'out')
        with open(argspath, 'r') as argsfile:
            exp = '--batch-mode ' + \
                  'verify org.fedoraproject.xmvn:xmvn-mojo:install ' + \
                  'org.fedoraproject.xmvn:xmvn-mojo:javadoc ' + \
                  'org.fedoraproject.xmvn:xmvn-mojo:builddep\n'
            self.assertEqual(argsfile.read(), exp)

    @rpm_test()
    def test_mvn_build_skip_javadoc(self, pack):
        pack.prepend('%bcond_without javadoc')
        pack.append_to_build('%mvn_build')

        _, stderr, return_value = pack.run_build(['--without', 'javadoc'])
        self.assertEqual(return_value, 0, stderr)
        argspath = os.path.join(pack.buildpath, '.xmvn', 'out')
        with open(argspath, 'r') as argsfile:
            exp = '--batch-mode --offline ' + \
                  'verify org.fedoraproject.xmvn:xmvn-mojo:install ' + \
                  'org.fedoraproject.xmvn:xmvn-mojo:builddep\n'
            self.assertEqual(argsfile.read(), exp)

    @rpm_test()
    def test_mvn_build_skip_test(self, pack):
        pack.prepend('%bcond_without tests')
        pack.append_to_build('%mvn_build')

        _, stderr, return_value = pack.run_build(['--without', 'tests'])
        self.assertEqual(return_value, 0, stderr)
        argspath = os.path.join(pack.buildpath, '.xmvn', 'out')
        with open(argspath, 'r') as argsfile:
            exp = '--batch-mode --offline -Dmaven.test.skip=true ' + \
                  'package org.fedoraproject.xmvn:xmvn-mojo:install ' + \
                  'org.fedoraproject.xmvn:xmvn-mojo:javadoc ' + \
                  'org.fedoraproject.xmvn:xmvn-mojo:builddep\n'
            self.assertEqual(argsfile.read(), exp)

    @rpm_test()
    def test_mvn_install(self, pack):
        pack.append_to_install('%mvn_install')

        _, stderr, return_value = pack.run_install()
        self.assertEqual(return_value, 0, stderr)

        argspath = os.path.join('rpmbuild', 'BUILD', '.xmvn', 'install-out')
        with open(argspath, 'r') as argsfile:
            args = argsfile.read()
            self.assertTrue(re.match(r'-R \.xmvn-reactor -n \S+ -d \S+\n',
                                     args), args)

    @rpm_test()
    def test_mvn_install_debug(self, pack):
        pack.append_to_install('%mvn_install -X')

        _, stderr, return_value = pack.run_install()
        self.assertEqual(return_value, 0, stderr)

        argspath = os.path.join('rpmbuild', 'BUILD', '.xmvn', 'install-out')
        with open(argspath, 'r') as argsfile:
            args = argsfile.read()
            self.assertTrue(re.match(r'-X -R \.xmvn-reactor -n \S+ -d \S+\n',
                                     args), args)

    @rpm_test()
    def test_mvn_install_directory(self, pack):
        pack.append_to_build('mkdir ../doc')
        pack.append_to_build('touch ../doc/file')
        pack.append_to_install('%mvn_install -J doc')
        pack.append_to_install('%files -f .mfiles-javadoc')

        _, stderr, return_value = pack.run_install()
        self.assertEqual(return_value, 0, stderr)

        argspath = os.path.join('rpmbuild', 'BUILD', '.xmvn', 'install-out')
        with open(argspath, 'r') as argsfile:
            args = argsfile.read()
            self.assertTrue(re.match(r'-R \.xmvn-reactor -n \S+ -d \S+\n',
                                     args), args)

        mfilespath = os.path.join('rpmbuild', 'BUILD', '.mfiles-javadoc')
        with open(mfilespath, 'r') as mfiles:
            self.assertEqual(mfiles.read(),
                             '/usr/share/javadoc/test_mvn_install_directory\n')

if __name__ == '__main__':
    unittest.main()
