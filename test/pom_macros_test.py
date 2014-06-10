import unittest
import os

from shutil import copytree
from shutil import rmtree

from test_common import assertIn
from test_rpmbuild import Package
from xml_compare import compare_xml_files

DIRPATH = os.path.dirname(os.path.realpath(__file__))

DATADIR = os.path.join(DIRPATH, "data", "pom_macros")
WORKDIR = os.path.join(DATADIR, "..", 'pom_macros_workdir')


def exec_macro(command = "", pom = "pom.xml", tail=''):
    def test_decorator(function):
        def test_decorated(self, *args, **kwargs):
            pompath = os.path.join(WORKDIR, pom)
            pomname = os.path.basename(pom)
            package = Package(function.__name__)
            package.add_source(pompath)
            pomsourcepath = os.path.join(package.buildpath, pomname)
            package.append_to_prep('%{command} {pom} {tail}'.format(command=command,
                pom=pomname, tail=tail))
            stdin, stderr, return_value = package.run_prep()

            function(self, stdin, stderr, return_value, pomsourcepath)
        return test_decorated
    return test_decorator

def check_result(pom_path):
    wantpath = '{pom}-want'.format(pom=os.path.basename(pom_path))
    report = compare_xml_files(pom_path, wantpath)
    res = not report
    return report, res

def get_result_literally(pom_path):
    with open(pom_path, 'r') as gotfile:
        got = gotfile.read().split('\n')

    wantpath = '{pom}-want'.format(pom=os.path.basename(pom_path))
    with open(wantpath, 'r') as wantfile:
        want = wantfile.read().split('\n')
    return got, want


class PomMacrosTest(unittest.TestCase):
    olddir = os.getcwd()
    maxDiff = 2048

    @classmethod
    def setUpClass(cls):
        cls.tearDownClass()
        cls.olddir = os.getcwd()
        copytree(DATADIR, WORKDIR)
        os.chdir(WORKDIR)

    @classmethod
    def tearDownClass(cls):
        try:
            rmtree(WORKDIR)
        except OSError:
            pass
        os.chdir(cls.olddir)

    def test_usage(self):
        package = Package("usage")
        pompath = os.path.join(WORKDIR, "pom_remove_dep.xml")
        package.add_source(pompath, "pom.xml")
        package.append_to_prep('%pom_remove_dep')
        _, stderr, return_value = package.run_prep()
        self.assertEqual(return_value, 1)
        assertIn(self, "Usage: %pom_remove_dep "\
                      "[groupId]:[artifactId] [POM location]", stderr)

    @exec_macro("pom_remove_dep :commons-io", "pom_remove_dep.xml")
    def test_remove_dep(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_dep commons-io:commons-io", "pom_remove_dep2.xml")
    def test_remove_deps(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_dep :", "pom_remove_dep_wildcard.xml")
    def test_remove_wildcard(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_dep junit:", "pom_remove_dep_nons.xml")
    def test_remove_dep_nons(self, stdin, stderr, returncode, pom_path):
        # no namespace
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_dep not:there", "pom_remove_dep_ret1.xml")
    def test_remove_dep_no_effect(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Error in processing", stderr)

    @exec_macro("pom_remove_plugin :my-plugin", "pom_remove_plugin.xml")
    def test_remove_plugin(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_plugin my.group:my-plugin",
                "pom_remove_plugin2.xml")
    def test_remove_plugins(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_plugin :my-plugin", "pom_remove_plugin_nons.xml")
    def test_remove_plugin_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_plugin not:there", "pom_remove_plugin_ret1.xml")
    def test_remove_plugin_ret1(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1)
        assertIn(self, "Error in processing", stderr)

    @exec_macro("pom_disable_module module", "pom_disable_module.xml")
    def test_disable_module(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_disable_module module", "pom_disable_module_nons.xml")
    def test_disable_module_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_disable_module notthere", "pom_disable_module_ret1.xml")
    def test_disable_module_no_effect(self, stdin, stderr,
                                      returncode, pom_path):
        self.assertEqual(returncode, 1)
        assertIn(self, "Error in processing", stderr)

    @exec_macro("pom_add_dep gdep:adep:3.2:test", "pom_add_dep.xml")
    def test_add_dep(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_dep foo:bar:1.2", "pom_add_dep_extra.xml",
                "'<scope>test</scope>'")
    def test_add_dep_extra(self, stdout, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_dep_mgmt foo:bar:1.2", "pom_add_dep_mgmt_extra.xml",
                "'<scope>test</scope>'")
    def test_add_dep_mgmt_extra(self, stdout, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_dep gdep:adep:3.2:test", "pom_add_dep_whitespace.xml")
    def test_add_dep_whitespace(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        got, want = get_result_literally(pom_path)
        self.assertEqual(got, want)

    @exec_macro("pom_add_dep gdep:adep", "pom_add_dep2.xml")
    def test_add_dep2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_dep A:B::compile", "pom_add_dep_nons.xml")
    def test_add_dep_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_dep_mgmt gdep:adep:3.2:test", "pom_add_dep_mgmt.xml")
    def test_add_dep_mgmt(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_dep_mgmt gdep:adep", "pom_add_dep_mgmt2.xml")
    def test_add_dep_mgmt2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_dep_mgmt gdep:adep", "pom_add_dep_mgmt_nons.xml")
    def test_add_dep_mgmt_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_plugin plugin:plug:3", "pom_add_plugin.xml")
    def test_add_plugin(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_plugin plugin:plug:3", "pom_add_plugin_extra.xml",
                """'<executions>
                       <id>default-compile</id>
                       <goals>
                          <goal>testCompile</goal>
                       </goals>
                    </executions>
                   '""")
    def test_add_plugin_extra(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_plugin plug:plug", "pom_add_plugin2.xml")
    def test_add_plugin2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_plugin g:a:15", "pom_add_plugin_nons.xml")
    def test_add_plugin_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_plugin :A-A", "pom_add_plugin_default_gid.xml")
    def test_add_plugin_default_gid(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_parent", "pom_remove_parent.xml")
    def test_remove_parent(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_parent", "pom_remove_parent_nons.xml")
    def test_remove_parent_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_parent", "pom_remove_parent_fail.xml")
    def test_remove_parent_fail(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1)
        assertIn(self, "Error in processing", stderr)

    @exec_macro("pom_add_parent pg:pa:21", "pom_add_parent.xml")
    def test_add_parent(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_add_parent pg:pa", "pom_add_parent_nons.xml")
    def test_add_parent_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_set_parent pg:aa:5", "pom_set_parent.xml")
    def test_set_parent(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_set_parent pg:aa", "pom_set_parent_nons.xml")
    def test_set_parent_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_set_parent pg:aa", "pom_set_parent_fail.xml")
    def test_set_parent_fail(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Error in processing", stderr)

    @exec_macro("pom_xpath_remove pom:maven-old", "pom_xpath_remove.xml")
    def test_xpath_remove(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_remove 'pom:modules/node()'", "pom_xpath_remove_generic.xml")
    def test_xpath_remove_generic(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_remove \
                 \"pom:dependency[pom:artifactId[text()='m-m']]\"",
                "pom_xpath_remove2.xml")
    def test_xpath_remove2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_remove pom:dependencies",
                "pom_xpath_remove_nons.xml")
    def test_xpath_remove_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_remove pom:not/pom:there",
                "pom_xpath_remove_fail.xml")
    def test_xpath_remove_fail(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Error in processing", stderr)

    @exec_macro("pom_xpath_inject pom:parent '<version>1.2</version>'",
                "pom_xpath_inject.xml")
    def test_xpath_inject(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_inject pom:dependencies/pom:dependency "
                "'<classifier>test</classifier>'",
                "pom_xpath_inject_multiple.xml")
    def test_xpath_inject_multiple(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_inject pom:parent '<version>1.2</version>'",
                "pom_xpath_inject_whitespace.xml")
    def test_xpath_inject_whitespace(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        got, want = get_result_literally(pom_path)
        self.assertEqual(got, want)

    @exec_macro("pom_xpath_inject pom:parent '<version>1.2</version>'",
                "pom_xpath_inject_whitespace1.xml")
    def test_xpath_inject_whitespace1(self, stdin, stderr,
                                      returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        got, want = get_result_literally(pom_path)
        self.assertEqual(got, want)

    @exec_macro("pom_xpath_inject pom:build/pom:plugins '<plugin>\
                 <groupId>some</groupId>\
                 <artifactId>plugin</artifactId></plugin>'",
                "pom_xpath_inject2.xml")
    def test_xpath_inject2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_inject pom:project '<name>Commons Lang</name>'",
                "pom_xpath_inject_nons.xml")
    def test_xpath_inject_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_inject pom:project '<name>Commons Lang<name>'",
            "pom_xpath_inject_fail.xml")
    def test_xpath_inject_fail(self, stdin, stderr, returncode, pom_path):
        # invalid XML code
        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Error in processing", stderr)

    @exec_macro("pom_xpath_replace pom:parent/pom:groupId \
                 '<groupId>commons</groupId>'",
                "pom_xpath_replace.xml")
    def test_xpath_replace(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_replace //pom:dependency/pom:groupId "
                "'<groupId>a</groupId>'",
                "pom_xpath_replace_multiple.xml")
    def test_xpath_replace_multiple(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_replace //pom:dependency/pom:groupId "
                "'<groupId>a/groupId>'",
                "pom_xpath_replace_multiple.xml")
    def test_xpath_replace_invalid(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1)
        assertIn(self, "Error in processing", stderr)

    @exec_macro("pom_xpath_replace pom:parent/pom:groupId \
                 '<groupId>commons</groupId>'",
                "pom_xpath_replace_whitespace.xml")
    def test_xpath_replace_whitespace(self, stdin, stderr,
                                      returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        got, want = get_result_literally(pom_path)
        self.assertEqual(got, want)

    @exec_macro("pom_xpath_replace \
                 \"pom:dependency[pom:artifactId[text()='junit']]/pom:version\"\
                 '<version>commons</version>'", "pom_xpath_replace2.xml")
    def test_xpath_replace2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_replace pom:parent \
                 '<groupId>org.apache.commons</groupId>'",
                "pom_xpath_replace_nons.xml")
    def test_xpath_replace_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_replace pom:project/pom:not/pom:there \
                 '<groupId>commons</groupId>'",
                "pom_xpath_replace_fail.xml")
    def test_xpath_replace_fail(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Error in processing", stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_replace pom:project/pom:groupId \
                 '<groupId>commons<groupId>'",
                "pom_xpath_replace_invalid.xml")
    def test_xpath_replace_invalid_xml(self, stdin, stderr,
                                       returncode, pom_path):
        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Error in processing", stderr)

    @exec_macro("pom_xpath_set pom:project/pom:groupId 'commons'",
            "pom_xpath_set.xml")
    def test_xpath_set(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_set pom:groupId 'commons'",
            "pom_xpath_set_multiple.xml")
    def test_xpath_set_multiple(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_set \"pom:build/pom:plugins/pom:plugin[pom:groupId\
                 [text()='org.codehaus.mojo']]/pom:version\" 2",
                "pom_xpath_set2.xml")
    def test_xpath_set2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_set pom:parent/pom:artifactId 'a-Id'",
                "pom_xpath_set_nons.xml")
    def test_xpath_set_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_xpath_set pom:project/pom:parent/pom:notThere Project",
                "pom_xpath_set_fail.xml")
    def test_xpath_set_fail(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Error in processing", stderr)

        report, res = check_result(pom_path)
        self.assertEqual(res, True, report)

    @exec_macro("pom_remove_parent", "unparsable_xml.pom")
    def test_unparsable_xml(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Error in processing", stderr)

    def test_no_pom(self):
        package = Package("nonexistent_pom")
        package.append_to_prep('%pom_remove_parent')
        _, stderr, returncode = package.run_prep()

        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Couldn't locate ", stderr)

    def test_no_pom_explicit(self):
        package = Package("nonexistent_pom_explicit")
        package.append_to_prep('%pom_remove_parent nonexistent_pom.xml')
        _, stderr, returncode = package.run_prep()

        self.assertEqual(returncode, 1, stderr)
        assertIn(self, "Couldn't locate ", stderr)

if __name__ == '__main__':
    unittest.main()
