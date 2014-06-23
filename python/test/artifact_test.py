import os
import unittest
from lxml.etree import fromstring, parse

from javapackages.maven.artifact import Artifact, ArtifactFormatException

from misc import exception_expected

def artifactfile(fname):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            main_dir = os.path.dirname(os.path.realpath(__file__))
            fn(self, parse(os.path.join(main_dir, "data", fname)))
        return test_decorated

    return test_decorator

class TestArtifact(unittest.TestCase):

    def setUp(self):
        # intentional whitespaces
        self.gaArtifact = Artifact(' g', ' a')
        self.gavArtifact = Artifact(' g', ' a', ' ', ' ', ' v')
        self.gaeArtifact = Artifact(' g', ' a', 'e')
        self.gacArtifact = Artifact(' g', ' a', ' ', ' c')
        self.gaevArtifact = Artifact(' g', 'a', ' e', ' ', ' v')
        self.gacvArtifact = Artifact(' g', 'a', ' ', 'c', ' v')
        self.fullArtifact = Artifact(' g', ' a', ' e', ' c', ' v')

    def test_artifact_init(self):
        a = self.gaArtifact
        self.assertEqual(a.groupId, 'g')
        self.assertEqual(a.artifactId, 'a')
        self.assertEqual(a.classifier, '')
        self.assertEqual(a.extension, 'jar')
        self.assertEqual(a.version, '')

        a = self.fullArtifact
        self.assertEqual(a.groupId, 'g')
        self.assertEqual(a.artifactId, 'a')
        self.assertEqual(a.classifier, 'c')
        self.assertEqual(a.extension, 'e')
        self.assertEqual(a.version, 'v')

    def test_str(self):
        self.assertEqual(str(self.gaArtifact), "g:a")
        self.assertEqual(str(self.gavArtifact), "g:a:v")
        self.assertEqual(str(self.gacArtifact), "g:a::c:")
        self.assertEqual(str(self.gacvArtifact), "g:a::c:v")
        self.assertEqual(str(self.fullArtifact), "g:a:e:c:v")

    def test_rpm_str(self):
        self.assertEqual(self.gaArtifact.get_rpm_str(), "mvn(g:a)")
        self.assertEqual(self.gavArtifact.get_rpm_str(), "mvn(g:a)")
        self.assertEqual(self.gacArtifact.get_rpm_str(), "mvn(g:a::c:)")
        self.assertEqual(self.gacvArtifact.get_rpm_str(), "mvn(g:a::c:)")
        self.assertEqual(self.gaeArtifact.get_rpm_str(), "mvn(g:a:e:)")
        self.assertEqual(self.gaevArtifact.get_rpm_str(), "mvn(g:a:e:)")
        self.assertEqual(self.fullArtifact.get_rpm_str(), "mvn(g:a:e:c:)")

    def test_xml_str_ga(self):
        doc = fromstring(self.gaArtifact.get_xml_str())
        self.assertNotEqual(doc, None)
        self.assertEqual(len(doc), 2)
        item = doc.find('./groupId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'g')
        item = doc.find('./artifactId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'a')
        item = doc.find('./extension')
        self.assertEqual(item, None)
        item = doc.find('./classifier')
        self.assertEqual(item, None)
        item = doc.find('./version')
        self.assertEqual(item, None)

    def test_xml_str_gae(self):
        doc = fromstring(self.gaeArtifact.get_xml_str())
        self.assertNotEqual(doc, None)
        self.assertEqual(len(doc), 3)
        item = doc.find('./groupId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'g')
        item = doc.find('./artifactId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'a')
        item = doc.find('./extension')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'e')
        item = doc.find('./classifier')
        self.assertEqual(item, None)
        item = doc.find('./version')
        self.assertEqual(item, None)

    def test_xml_str_gac(self):
        doc = fromstring(self.gacArtifact.get_xml_str())
        self.assertNotEqual(doc, None)
        self.assertEqual(len(doc), 3)
        item = doc.find('./groupId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'g')
        item = doc.find('./artifactId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'a')
        item = doc.find('./extension')
        self.assertEqual(item, None)
        item = doc.find('./classifier')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'c')
        item = doc.find('./version')
        self.assertEqual(item, None)

    def test_xml_str_gav(self):
        doc = fromstring(self.gavArtifact.get_xml_str())
        self.assertNotEqual(doc, None)
        self.assertEqual(len(doc), 3)
        item = doc.find('./groupId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'g')
        item = doc.find('./artifactId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'a')
        item = doc.find('./extension')
        self.assertEqual(item, None)
        item = doc.find('./classifier')
        self.assertEqual(item, None)
        item = doc.find('./version')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'v')

    def test_xml_str_gaev(self):
        doc = fromstring(self.gaevArtifact.get_xml_str())
        self.assertNotEqual(doc, None)
        self.assertEqual(len(doc), 4)
        item = doc.find('./groupId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'g')
        item = doc.find('./artifactId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'a')
        item = doc.find('./extension')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'e')
        item = doc.find('./classifier')
        self.assertEqual(item, None)
        item = doc.find('./version')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'v')

    def test_xml_str_gacv(self):
        doc = fromstring(self.gacvArtifact.get_xml_str())
        self.assertNotEqual(doc, None)
        self.assertEqual(len(doc), 4)
        item = doc.find('./groupId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'g')
        item = doc.find('./artifactId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'a')
        item = doc.find('./extension')
        self.assertEqual(item, None)
        item = doc.find('./classifier')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'c')
        item = doc.find('./version')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'v')

    def test_xml_str_full(self):
        doc = fromstring(self.fullArtifact.get_xml_str())
        self.assertNotEqual(doc, None)
        self.assertEqual(len(doc), 5)
        item = doc.find('./groupId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'g')
        item = doc.find('./artifactId')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'a')
        item = doc.find('./extension')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'e')
        item = doc.find('./classifier')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'c')
        item = doc.find('./version')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'v')

    @exception_expected(ArtifactFormatException)
    @artifactfile("artifact-empty.xml")
    def test_from_xml_empty(self, doc):
        Artifact.from_xml_element(doc)

    @exception_expected(ArtifactFormatException)
    @artifactfile("artifact-nog.xml")
    def test_from_xml_nog(self, doc):
        Artifact.from_xml_element(doc)

    @exception_expected(ArtifactFormatException)
    @artifactfile("artifact-noa.xml")
    def test_from_xml_noa(self, doc):
        Artifact.from_xml_element(doc)

    @artifactfile("artifactga.xml")
    def test_from_xml_ga(self, doc):
        a = Artifact.from_xml_element(doc)
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "")

    @artifactfile("artifactgav.xml")
    def test_from_xml_gav(self, doc):
        a = Artifact.from_xml_element(doc)
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v")

    @artifactfile("artifactfull.xml")
    def test_from_xml_full(self, doc):
        a = Artifact.from_xml_element(doc)
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "v")

    @artifactfile("artifact-whitespace.xml")
    def test_from_xml_whitespace(self, doc):
        a = Artifact.from_xml_element(doc)
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "v")

    def test_from_mvn_str_ga(self):
        a = Artifact.from_mvn_str("g:a")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "")

    def test_from_mvn_str_gav(self):
        a = Artifact.from_mvn_str("g:a:v")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v")

    def test_from_mvn_str_gae(self):
        a = Artifact.from_mvn_str("g:a:e:")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "")

    def test_from_mvn_str_gaev(self):
        a = Artifact.from_mvn_str("g:a:e:v")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v")

    def test_from_mvn_str_gac(self):
        a = Artifact.from_mvn_str("g:a::c:")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "")

    def test_from_mvn_str_gacv(self):
        a = Artifact.from_mvn_str("g:a::c:v")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "v")

    def test_from_mvn_str_gaec(self):
        a = Artifact.from_mvn_str("g:a:e:c:")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "")

    def test_from_mvn_str_full(self):
        a = Artifact.from_mvn_str("g:a:e:c:v")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "v")

    def test_merge1(self):
        a = Artifact.from_mvn_str("g1:a1:v1")
        b = Artifact.from_mvn_str("g1:a1")
        a.merge_with(b)

        self.assertEqual(a.groupId, "g1")
        self.assertEqual(a.artifactId, "a1")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v1")

    def test_merge2(self):
        a = Artifact.from_mvn_str("g1:a1:v1")
        b = Artifact.from_mvn_str("g1:a1:v2")
        a.merge_with(b)

        self.assertEqual(a.groupId, "g1")
        self.assertEqual(a.artifactId, "a1")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v1")

    def test_merge3(self):
        # different artifacts won't be merged
        a = Artifact.from_mvn_str("g1:a1:v1")
        b = Artifact.from_mvn_str("g2:a2:e2::")
        a.merge_with(b)

        self.assertEqual(a.groupId, "g1")
        self.assertEqual(a.artifactId, "a1")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v1")

    def test_merge4(self):
        a = Artifact.from_mvn_str("g1:a1")
        b = Artifact.from_mvn_str("g1:a1:v1")
        a.merge_with(b)

        self.assertEqual(a.groupId, "g1")
        self.assertEqual(a.artifactId, "a1")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v1")

    def test_merge5(self):
        a = Artifact.from_mvn_str("g1:a1:war::")
        b = Artifact.from_mvn_str("g1:a1:v1")
        a.merge_with(b)

        self.assertEqual(a.groupId, "g1")
        self.assertEqual(a.artifactId, "a1")
        self.assertEqual(a.extension, "war")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "")

    def test_interpolation1(self):
        a = Artifact.from_mvn_str("${gid}:a1")
        props = {"gid": "g1"}
        res = a.interpolate(props)

        self.assertEqual(len(res), 0)
        self.assertEqual(a.groupId, "g1")
        self.assertEqual(a.artifactId, "a1")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "")

    def test_interpolation2(self):
        a = Artifact.from_mvn_str("${gid}:a1:${v.major}.${v.minor}")
        props = {"gid": "g1", "v.major": "4", "v.minor": "11"}
        res = a.interpolate(props)

        self.assertEqual(len(res), 0)
        self.assertEqual(a.groupId, "g1")
        self.assertEqual(a.artifactId, "a1")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "4.11")

    def test_interpolation3(self):
        a = Artifact.from_mvn_str("${gid}:a1")
        props = {"v.minor": "11"}
        res = a.interpolate(props)

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], "gid")
        self.assertEqual(a.groupId, "${gid}")
        self.assertEqual(a.artifactId, "a1")
        self.assertEqual(a.extension, "jar")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "")

if __name__ == '__main__':
    unittest.main()
