import os
import unittest
from shutil import rmtree
import xml.etree.ElementTree as ET

from javapackages.artifact import Artifact
from javapackages.xmvn_config import XMvnConfig


class TestXMvnConfig(unittest.TestCase):

    def __clean(self):
        rmtree(".xmvn", ignore_errors=True)

    def __find(self, elem, xpath):
        return elem.find(xpath, namespaces=dict(xmvn=XMvnConfig.XMLNS))

    def __findall(self, elem, xpath):
        return elem.findall(xpath, namespaces=dict(xmvn=XMvnConfig.XMLNS))

    def _read_current_conf(self):
        ind = self._read_index()

        fname = 'javapackages-config-{index:05d}.xml'.format(index=ind)
        confpath = os.path.join(".xmvn", "config.d", fname)
        ET.register_namespace('xmvn', XMvnConfig.XMLNS)
        et = ET.parse(confpath)
        return et


    def _read_index(self):
        with open(".xmvn/javapackages-rule-index") as jin:
            return int(jin.read())

    def setUp(self):
        self.origDir = os.getcwd()
        os.mkdir("TestXMvnConfig-run")
        os.chdir("TestXMvnConfig-run")

    def tearDown(self):
        os.chdir(self.origDir)
        rmtree("TestXMvnConfig-run")

    def test_index_init(self):
        self.__clean()
        xc = XMvnConfig()
        a = Artifact('gId', 'aId')
        a1 = Artifact('agId', 'aaId')
        xc.add_aliases(a, [a1])
        ind = self._read_index()
        self.assertEqual(ind, 1)

        xc.add_aliases(a, [a1])
        ind = self._read_index()
        self.assertEqual(ind, 2)

    def test_aliases(self):
        xc = XMvnConfig()
        a = Artifact('gId', 'aId')
        a1 = Artifact('gIda1', 'aIda1')
        a2 = Artifact('gIda2', 'aIda2')
        xc.add_aliases(a, [a1, a2])

        et = self._read_current_conf()
        root = et.getroot()
        rule = self.__find(root, "xmvn:artifactManagement/xmvn:rule")

        aglob = self.__find(rule, "xmvn:artifactGlob")
        self.assertEqual(self.__find(aglob, "xmvn:groupId").text, "gId")
        self.assertEqual(self.__find(aglob,
                                     "xmvn:artifactId").text, "aId")

        aliases = self.__findall(rule, "xmvn:aliases/xmvn:alias")
        self.assertEqual(self.__find(aliases[0],
                                     "xmvn:groupId").text, "gIda1")
        self.assertEqual(self.__find(aliases[0],
                                     "xmvn:artifactId").text, "aIda1")

        self.assertEqual(self.__find(aliases[1], "xmvn:groupId").text, "gIda2")
        self.assertEqual(self.__find(aliases[1], "xmvn:artifactId").text, "aIda2")

    def test_file_mappings(self):
        xc = XMvnConfig()
        a = Artifact('gId', 'aId')
        xc.add_file_mapping(a, ['path1','path2'])

        et = self._read_current_conf()
        root = et.getroot()
        rule = self.__find(root, "xmvn:artifactManagement/xmvn:rule")

        aglob = self.__find(rule, "xmvn:artifactGlob")
        self.assertEqual(self.__find(aglob, "xmvn:groupId").text, "gId")
        self.assertEqual(self.__find(aglob, "xmvn:artifactId").text, "aId")

        files = self.__findall(rule, "xmvn:files/xmvn:file")
        self.assertEqual(files[0].text, "path1")
        self.assertEqual(files[1].text, "path2")

    def test_package_mappings(self):
        xc = XMvnConfig()
        a = Artifact('gId', 'aId')
        xc.add_package_mapping(a, 'package')

        et = self._read_current_conf()
        root = et.getroot()
        rule = self.__find(root, "xmvn:artifactManagement/xmvn:rule")

        aglob = self.__find(rule, "xmvn:artifactGlob")
        self.assertEqual(self.__find(aglob, "xmvn:groupId").text, "gId")
        self.assertEqual(self.__find(aglob, "xmvn:artifactId").text, "aId")

        self.assertEqual(self.__find(rule, "xmvn:targetPackage").text,
                         "package")

    def test_custom_config(self):
        xc = XMvnConfig()
        xc.add_custom_option("buildSettings/compilerSource", "1.5")
        et = self._read_current_conf()
        root = et.getroot()
        cs = self.__find(root, "xmvn:buildSettings/xmvn:compilerSource")
        self.assertEqual(cs.text, "1.5")


if __name__ == '__main__':
    unittest.main()
