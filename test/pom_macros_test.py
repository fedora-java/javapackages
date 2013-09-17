import unittest
import subprocess
import os
from shutil import copyfile
from shutil import copytree
from shutil import rmtree
from lxml import etree

def bash():
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            bash = subprocess.Popen(['bash'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)
            fn(self, bash)
        return test_decorated
    return test_decorator


pe = '. ../java-utils/pom_editor.sh; '
ns = dict(a='http://maven.apache.org/POM/4.0.0')

class PomMacrosTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        copytree('data/pom_macros', 'data/_pomtestdir')

    @classmethod
    def tearDownClass(cls):
        rmtree('data/_pomtestdir')

    @bash()
    def test_sanity(self, bash):
        stdin, stderr = bash.communicate(pe)
        self.assertEqual(bash.returncode, 0, stderr)

    @bash()
    def test_remove_dep(self, bash):
        data = "data/_pomtestdir/pom_remove_dep.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_dep :commons-io %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_remove_deps(self, bash):
        data = "data/_pomtestdir/pom_remove_dep2.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_dep commons-io:commons-io %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 2)

    @bash()
    def test_remove_dep_nons(self, bash):
        # no namespace
        data = "data/_pomtestdir/pom_remove_dep_nons.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_dep junit: %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_remove_dep_no_effect(self, bash):
        data = "data/_pomtestdir/pom_remove_dep_ret1.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_dep not:there %s" % data)
        self.assertEqual(bash.returncode, 1, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 2)

    @bash()
    def test_remove_plugin(self, bash):
        data = "data/_pomtestdir/pom_remove_plugin.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_plugin :my-plugin %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_remove_plugins(self, bash):
        data = "data/_pomtestdir/pom_remove_plugin2.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_plugin my.group:my-plugin %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_remove_plugin_nons(self, bash):
        data = "data/_pomtestdir/pom_remove_plugin_nons.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_plugin :my-plugin %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_remove_plugin_nons(self, bash):
        data = "data/_pomtestdir/pom_remove_plugin_ret1.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_plugin not:there %s" % data)
        self.assertEqual(bash.returncode, 1)

        doc = etree.parse(data)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 2)

    @bash()
    def test_disable_module(self, bash):
        data = "data/_pomtestdir/pom_disable_module.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_disable_module module %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:modules/a:module', namespaces=ns)
        self.assertEqual(len(r), 6)

    @bash()
    def test_disable_module_nons(self, bash):
        data = "data/_pomtestdir/pom_disable_module_nons.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_disable_module module %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:modules/a:module', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_disable_module_no_effect(self, bash):
        data = "data/_pomtestdir/pom_disable_module_ret1.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_disable_module notthere %s" % data)
        self.assertEqual(bash.returncode, 1)

        doc = etree.parse(data)
        r = doc.xpath('./a:modules/a:module', namespaces=ns)
        self.assertEqual(len(r), 7)

    @bash()
    def test_add_dep(self, bash):
        data = "data/_pomtestdir/pom_add_dep.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_dep gdep:adep:3.2:test %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_add_dep2(self, bash):
        data = "data/_pomtestdir/pom_add_dep2.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_dep gdep:adep %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 2)

    @bash()
    def test_add_dep_nons(self, bash):
        data = "data/_pomtestdir/pom_add_dep_nons.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_dep A:B::compile %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_add_dep_mgmt(self, bash):
        data = "data/_pomtestdir/pom_add_dep_mgmt.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_dep_mgmt gdep:adep:3.2:test %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencyManagement/a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 2)

    @bash()
    def test_add_dep_mgmt2(self, bash):
        data = "data/_pomtestdir/pom_add_dep_mgmt2.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_dep_mgmt gdep:adep %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencyManagement/a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_add_dep_mgmt_nons(self, bash):
        data = "data/_pomtestdir/pom_add_dep_mgmt_nons.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_dep_mgmt gdep:adep %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:dependencyManagement/a:dependencies/a:dependency', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_add_plugin(self, bash):
        data = "data/_pomtestdir/pom_add_plugin.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_plugin plugin:plug:3 %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 3)

    @bash()
    def test_add_plugin2(self, bash):
        data = "data/_pomtestdir/pom_add_plugin2.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_plugin plug:plug %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_add_plugin_nons(self, bash):
        data = "data/_pomtestdir/pom_add_plugin_nons.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_plugin g:a:15 %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 2)

    @bash()
    def test_add_plugin_default_gid(self, bash):
        data = "data/_pomtestdir/pom_add_plugin_default_gid.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_plugin :A-A %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:build/a:plugins/a:plugin', namespaces=ns)
        self.assertEqual(len(r), 1)
        r = doc.xpath('./a:build/a:plugins/a:plugin/a:groupId', namespaces=ns)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].text, "org.apache.maven.plugins")

    @bash()
    def test_remove_parent(self, bash):
        data = "data/_pomtestdir/pom_remove_parent.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_parent %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 0)

    @bash()
    def test_remove_parent_nons(self, bash):
        data = "data/_pomtestdir/pom_remove_parent_nons.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_parent %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 0)

    @bash()
    def test_remove_parent_fail(self, bash):
        data = "data/_pomtestdir/pom_remove_parent_fail.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_remove_parent %s" % data)
        self.assertEqual(bash.returncode, 1)

    @bash()
    def test_add_parent(self, bash):
        data = "data/_pomtestdir/pom_add_parent.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_parent pg:pa:21 %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_add_parent_nons(self, bash):
        data = "data/_pomtestdir/pom_add_parent_nons.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_parent pg:pa %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_add_parent_second(self, bash):
        data = "data/_pomtestdir/pom_add_parent_second.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_add_parent pg:p-a:1 %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 2)

    @bash()
    def test_set_parent(self, bash):
        data = "data/_pomtestdir/pom_set_parent.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_set_parent pg:aa:5 %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 1)
        r = doc.xpath('./a:parent/a:groupId', namespaces=ns)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].text, "pg")

    @bash()
    def test_set_parent_nons(self, bash):
        data = "data/_pomtestdir/pom_set_parent_nons.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_set_parent pg:aa %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 1)

    @bash()
    def test_set_parent_fail(self, bash):
        data = "data/_pomtestdir/pom_set_parent_fail.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_set_parent pg:aa %s" % data)
        self.assertEqual(bash.returncode, 1, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:parent', namespaces=ns)
        self.assertEqual(len(r), 0)

    @bash()
    def test_xpath_remove(self, bash):
        data = "data/_pomtestdir/pom_xpath_remove.xml"
        stdin, stderr = bash.communicate(pe +
                "pom_xpath_remove pom:maven-old %s" % data)
        self.assertEqual(bash.returncode, 0, stderr)

        doc = etree.parse(data)
        r = doc.xpath('./a:prerequisities/a:maven-old', namespaces=ns)
        self.assertEqual(len(r), 0)

if __name__ == '__main__':
    unittest.main()
