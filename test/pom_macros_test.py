import unittest
import subprocess
import os
from shutil import copyfile
from shutil import copytree
from shutil import rmtree
from lxml import etree

pe = '. ../java-utils/pom_editor.sh; '
ns = dict(a='http://maven.apache.org/POM/4.0.0')
data_dir = 'data/_pomtestdir/'

def exec_macro(command = "", pom = "pom.xml"):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            bash = subprocess.Popen(['bash'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)
            stdin, stderr = bash.communicate("%s %s %s%s" % (pe, command, data_dir, pom))

            fn(self, stdin, stderr, bash.returncode, os.path.join(data_dir, pom))
        return test_decorated
    return test_decorator


class PomMacrosTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        copytree('data/pom_macros', data_dir)

    @classmethod
    def tearDownClass(cls):
        rmtree('data/_pomtestdir')

    @exec_macro("ls", "pom_remove_dep.xml")
    def test_sanity(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

    @exec_macro("pom_remove_dep :commons-io", "pom_remove_dep.xml")
    def test_remove_dep(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_remove_dep commons-io:commons-io", "pom_remove_dep2.xml")
    def test_remove_deps(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 2)

    @exec_macro("pom_remove_dep junit:", "pom_remove_dep_nons.xml")
    def test_remove_dep_nons(self, stdin, stderr, returncode, pom_path):
        # no namespace
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_remove_dep not:there", "pom_remove_dep_ret1.xml")
    def test_remove_dep_no_effect(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 2)

    @exec_macro("pom_remove_plugin :my-plugin", "pom_remove_plugin.xml")
    def test_remove_plugin(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_remove_plugin my.group:my-plugin", "pom_remove_plugin2.xml")
    def test_remove_plugins(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_remove_plugin :my-plugin", "pom_remove_plugin_nons.xml")
    def test_remove_plugin_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_remove_plugin not:there", "pom_remove_plugin_ret1.xml")
    def test_remove_plugin_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 2)

    @exec_macro("pom_disable_module module", "pom_disable_module.xml")
    def test_disable_module(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:modules/a:module', namespaces=ns)
        self.assertEqual(len(r), 6)

    @exec_macro("pom_disable_module module", "pom_disable_module_nons.xml")
    def test_disable_module_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:modules/a:module', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_disable_module notthere", "pom_disable_module_ret1.xml")
    def test_disable_module_no_effect(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:modules/a:module', namespaces=ns)
        self.assertEqual(len(r), 7)

    @exec_macro("pom_add_dep gdep:adep:3.2:test", "pom_add_dep.xml")
    def test_add_dep(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_add_dep gdep:adep", "pom_add_dep2.xml")
    def test_add_dep2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 2)

    @exec_macro("pom_add_dep A:B::compile", "pom_add_dep_nons.xml")
    def test_add_dep_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_add_dep_mgmt gdep:adep:3.2:test", "pom_add_dep_mgmt.xml")
    def test_add_dep_mgmt(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencyManagement/a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 2)

    @exec_macro("pom_add_dep_mgmt gdep:adep", "pom_add_dep_mgmt2.xml")
    def test_add_dep_mgmt2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencyManagement/a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_add_dep_mgmt gdep:adep", "pom_add_dep_mgmt_nons.xml")
    def test_add_dep_mgmt_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:dependencyManagement/a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_add_plugin plugin:plug:3", "pom_add_plugin.xml")
    def test_add_plugin(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 3)

    @exec_macro("pom_add_plugin plug:plug", "pom_add_plugin2.xml")
    def test_add_plugin2(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_add_plugin g:a:15", "pom_add_plugin_nons.xml")
    def test_add_plugin_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 2)

    @exec_macro("pom_add_plugin :A-A", "pom_add_plugin_default_gid.xml")
    def test_add_plugin_default_gid(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)
        r = doc.xpath('./a:build/a:plugins/a:plugin/a:groupId', namespaces=ns)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].text, "org.apache.maven.plugins")

    @exec_macro("pom_remove_parent", "pom_remove_parent.xml")
    def test_remove_parent(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 0)

    @exec_macro("pom_remove_parent", "pom_remove_parent_nons.xml")
    def test_remove_parent_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 0)

    @exec_macro("pom_remove_parent", "pom_remove_parent_fail.xml")
    def test_remove_parent_fail(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1)

    @exec_macro("pom_add_parent pg:pa:21", "pom_add_parent.xml")
    def test_add_parent(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_add_parent pg:pa", "pom_add_parent_nons.xml")
    def test_add_parent_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_add_parent pg:p-a:1", "pom_add_parent_second.xml")
    def test_add_parent_second(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 2)

    @exec_macro("pom_set_parent pg:aa:5", "pom_set_parent.xml")
    def test_set_parent(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 1)
        r = doc.xpath('./a:parent/a:groupId', namespaces=ns)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].text, "pg")

    @exec_macro("pom_set_parent pg:aa", "pom_set_parent_nons.xml")
    def test_set_parent_nons(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 1)

    @exec_macro("pom_set_parent pg:aa", "pom_set_parent_fail.xml")
    def test_set_parent_fail(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 1, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 0)

    @exec_macro("pom_xpath_remove pom:maven-old", "pom_xpath_remove.xml")
    def test_xpath_remove(self, stdin, stderr, returncode, pom_path):
        self.assertEqual(returncode, 0, stderr)

        doc = etree.parse(pom_path)
        r = doc.xpath('./a:prerequisities/a:maven-old', namespaces=ns)
        self.assertEqual(len(r), 0)

if __name__ == '__main__':
    unittest.main()
