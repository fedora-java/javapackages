import os
import unittest
from shutil import rmtree
import lxml.etree as ET

from javapackages.artifact import Artifact
from javapackages.xmvn_config import XMvnConfig


class TestXMvnConfig(unittest.TestCase):

    def __clean(self):
        rmtree(".xmvn", ignore_errors=True)

    def __find(self, elem, xpath):
        ret = None
        ret = elem.xpath(xpath, namespaces=dict(xmvn=XMvnConfig.XMLNS))
        if not ret:
            ret = elem.xpath(xpath.replace('xmvn:',XMvnConfig.XMLNS))[0]
        else:
            ret = ret[0]
        return ret

    def __findall(self, elem, xpath):
        ret = elem.xpath(xpath, namespaces=dict(xmvn=XMvnConfig.XMLNS))
        if not ret:
           ret = elem.xpath(xpath.replace('xmvn:',XMvnConfig.XMLNS))
        return ret

    def _read_current_conf(self):
        ind = self._read_index()

        fname = 'javapackages-config-{index:05d}.xml'.format(index=ind)
        confpath = os.path.join(".xmvn", "config.d", fname)
        parser = ET.XMLParser(remove_blank_text=True)
        et = ET.parse(confpath, parser)
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
        self.assertEqual(self.__find(aglob, "xmvn:groupId").text.strip(), "gId")
        self.assertEqual(self.__find(aglob,
                                     "xmvn:artifactId").text.strip(), "aId")

        aliases = self.__findall(rule, "xmvn:aliases/xmvn:alias")
        self.assertEqual(self.__find(aliases[0],
                                     "xmvn:groupId").text.strip(), "gIda1")
        self.assertEqual(self.__find(aliases[0],
                                     "xmvn:artifactId").text.strip(), "aIda1")

        self.assertEqual(self.__find(aliases[1], "xmvn:groupId").text.strip(), "gIda2")
        self.assertEqual(self.__find(aliases[1], "xmvn:artifactId").text.strip(), "aIda2")

    def test_file_mappings(self):
        xc = XMvnConfig()
        a = Artifact('gId', 'aId')
        xc.add_file_mapping(a, ['path1','path2'])

        et = self._read_current_conf()
        root = et.getroot()
        rule = self.__find(root, "xmvn:artifactManagement/xmvn:rule")

        aglob = self.__find(rule, "xmvn:artifactGlob")
        self.assertEqual(self.__find(aglob, "xmvn:groupId").text.strip(), "gId")
        self.assertEqual(self.__find(aglob, "xmvn:artifactId").text.strip(), "aId")

        files = self.__findall(rule, "xmvn:files/xmvn:file")
        self.assertEqual(files[0].text.strip(), "path1")
        self.assertEqual(files[1].text.strip(), "path2")

    def test_compat_versions(self):
        xc = XMvnConfig()
        a = Artifact('gId', 'aId')
        xc.add_compat_versions(a, ['version1','version2'])

        et = self._read_current_conf()
        root = et.getroot()
        rule = self.__find(root, "xmvn:artifactManagement/xmvn:rule")

        aglob = self.__find(rule, "xmvn:artifactGlob")
        self.assertEqual(self.__find(aglob, "xmvn:groupId").text.strip(), "gId")
        self.assertEqual(self.__find(aglob, "xmvn:artifactId").text.strip(), "aId")

        files = self.__findall(rule, "xmvn:versions/xmvn:version")
        self.assertEqual(files[0].text.strip(), "version1")
        self.assertEqual(files[1].text.strip(), "version2")

    def test_package_mappings(self):
        xc = XMvnConfig()
        a = Artifact('gId', 'aId')
        xc.add_package_mapping(a, 'package')

        et = self._read_current_conf()
        root = et.getroot()
        rule = self.__find(root, "xmvn:artifactManagement/xmvn:rule")

        aglob = self.__find(rule, "xmvn:artifactGlob")
        self.assertEqual(self.__find(aglob, "xmvn:groupId").text.strip(), "gId")
        self.assertEqual(self.__find(aglob, "xmvn:artifactId").text.strip(), "aId")

        self.assertEqual(self.__find(rule, "xmvn:targetPackage").text.strip(),
                         "package")

    def test_custom_config(self):
        xc = XMvnConfig()
        xc.add_custom_option("buildSettings/compilerSource", "1.5")
        et = self._read_current_conf()
        root = et.getroot()
        cs = self.__find(root, "xmvn:buildSettings/xmvn:compilerSource")
        self.assertEqual(cs.text.strip(), "1.5")

    def test_custom_config_xml(self):
        xc = XMvnConfig()
        xc.add_custom_option("buildSettings/compilerSource",
                """<versions>
                    <version>1.5</version>
                    <version>1.6</version>
                </versions>
                """)
        et = self._read_current_conf()
        root = et.getroot()
        versions = self.__find(root,
                "xmvn:buildSettings/xmvn:compilerSource/xmvn:versions")
        self.assertEqual(len(versions), 2)
        v1, v2 = self.__findall(versions, "xmvn:version")
        self.assertEqual(v1.text.strip(), "1.5")
        self.assertEqual(v2.text.strip(), "1.6")


if __name__ == '__main__':
    unittest.main()
