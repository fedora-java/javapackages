import os
import unittest
from lxml.etree import fromstring, parse

from javapackages.artifact import Artifact, ArtifactFormatException

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
        self.namespaceArtifact = Artifact(' g', ' a', ' e', ' c', ' v', ' n')

    def test_artifact_init(self):
        a = self.gaArtifact
        self.assertEqual(a.groupId, 'g')
        self.assertEqual(a.artifactId, 'a')
        self.assertEqual(a.classifier, '')
        self.assertEqual(a.extension, '')
        self.assertEqual(a.version, '')
        self.assertEqual(a.namespace, '')

        a = self.fullArtifact
        self.assertEqual(a.groupId, 'g')
        self.assertEqual(a.artifactId, 'a')
        self.assertEqual(a.classifier, 'c')
        self.assertEqual(a.extension, 'e')
        self.assertEqual(a.version, 'v')
        self.assertEqual(a.namespace, '')

        a = self.namespaceArtifact
        self.assertEqual(a.groupId, 'g')
        self.assertEqual(a.artifactId, 'a')
        self.assertEqual(a.classifier, 'c')
        self.assertEqual(a.extension, 'e')
        self.assertEqual(a.version, 'v')
        self.assertEqual(a.namespace, 'n')

    def test_str(self):
        self.assertEqual(str(self.gaArtifact), "g:a:::")
        self.assertEqual(str(self.gavArtifact), "g:a:::v")
        self.assertEqual(str(self.gacArtifact), "g:a::c:")
        self.assertEqual(str(self.gacvArtifact), "g:a::c:v")
        self.assertEqual(str(self.fullArtifact), "g:a:e:c:v")
        self.assertEqual(str(self.namespaceArtifact), "g:a:e:c:v")

    def test_rpm_str(self):
        self.assertEqual(self.gaArtifact.get_rpm_str(), "mvn(g:a)")
        self.assertEqual(self.gavArtifact.get_rpm_str(), "mvn(g:a)")
        self.assertEqual(self.gacArtifact.get_rpm_str(), "mvn(g:a::c:)")
        self.assertEqual(self.gacvArtifact.get_rpm_str(), "mvn(g:a::c:)")
        self.assertEqual(self.gaeArtifact.get_rpm_str(), "mvn(g:a:e:)")
        self.assertEqual(self.gaevArtifact.get_rpm_str(), "mvn(g:a:e:)")
        self.assertEqual(self.fullArtifact.get_rpm_str(), "mvn(g:a:e:c:)")
        self.assertEqual(self.namespaceArtifact.get_rpm_str(), "n-mvn(g:a:e:c:)")

        self.assertEqual(self.gavArtifact.get_rpm_str(True), "mvn(g:a:v)")
        self.assertEqual(self.gacvArtifact.get_rpm_str(True), "mvn(g:a::c:v)")
        self.assertEqual(self.gaevArtifact.get_rpm_str(True), "mvn(g:a:e:v)")
        self.assertEqual(self.fullArtifact.get_rpm_str(True), "mvn(g:a:e:c:v)")
        self.assertEqual(self.namespaceArtifact.get_rpm_str(True), "n-mvn(g:a:e:c:v)")

        # These should fail, can't ask for versioned string out of unversioned artifact
        self.assertRaises(ArtifactFormatException, self.gaArtifact.get_rpm_str, True)
        self.assertRaises(ArtifactFormatException, self.gaeArtifact.get_rpm_str, True)
        self.assertRaises(ArtifactFormatException, self.gacArtifact.get_rpm_str, True)

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

    def test_xml_str_namespace(self):
        doc = fromstring(self.namespaceArtifact.get_xml_str())
        self.assertNotEqual(doc, None)
        self.assertEqual(len(doc), 6)
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
        item = doc.find('./namespace')
        self.assertNotEqual(item, None)
        self.assertEquals(item.text, 'n')

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
        self.assertEqual(a.extension, "")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "")
        self.assertEqual(a.namespace, "")

    @artifactfile("artifactgav.xml")
    def test_from_xml_gav(self, doc):
        a = Artifact.from_xml_element(doc)
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v")
        self.assertEqual(a.namespace, "")

    @artifactfile("artifactfull.xml")
    def test_from_xml_full(self, doc):
        a = Artifact.from_xml_element(doc)
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "v")
        self.assertEqual(a.namespace, "n")

    @artifactfile("artifact-whitespace.xml")
    def test_from_xml_whitespace(self, doc):
        a = Artifact.from_xml_element(doc)
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "v")
        self.assertEqual(a.namespace, "n")

    def test_from_mvn_str_ga(self):
        a = Artifact.from_mvn_str("g:a")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "")
        self.assertEqual(a.namespace, "")

    def test_from_mvn_str_gav(self):
        a = Artifact.from_mvn_str("g:a:v")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v")
        self.assertEqual(a.namespace, "")

    def test_from_mvn_str_gae(self):
        a = Artifact.from_mvn_str("g:a:e:")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "")
        self.assertEqual(a.namespace, "")

    def test_from_mvn_str_gaev(self):
        a = Artifact.from_mvn_str("g:a:e:v")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "")
        self.assertEqual(a.version, "v")
        self.assertEqual(a.namespace, "")

    def test_from_mvn_str_gac(self):
        a = Artifact.from_mvn_str("g:a::c:")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "")
        self.assertEqual(a.namespace, "")

    def test_from_mvn_str_gacv(self):
        a = Artifact.from_mvn_str("g:a::c:v")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "v")
        self.assertEqual(a.namespace, "")

    def test_from_mvn_str_gaec(self):
        a = Artifact.from_mvn_str("g:a:e:c:")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "")
        self.assertEqual(a.namespace, "")

    def test_from_mvn_str_full(self):
        a = Artifact.from_mvn_str("g:a:e:c:v")
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "v")
        self.assertEqual(a.namespace, "")

    def test_from_mvn_str_namespace(self):
        a = Artifact.from_mvn_str("g:a:e:c:v", 'n')
        self.assertEqual(a.groupId, "g")
        self.assertEqual(a.artifactId, "a")
        self.assertEqual(a.extension, "e")
        self.assertEqual(a.classifier, "c")
        self.assertEqual(a.version, "v")
        self.assertEqual(a.namespace, "n")

    def test_merge(self):
        a = Artifact.from_mvn_str("g1:a1:v1", 'n')
        b = Artifact.from_mvn_str("g2:a2:e2::", 'n2')
        m = Artifact.merge_artifacts(a, b)

        self.assertEqual(m.groupId, "g1")
        self.assertEqual(m.artifactId, "a1")
        self.assertEqual(m.extension, "e2")
        self.assertEqual(m.classifier, "")
        self.assertEqual(m.version, "v1")
        self.assertEqual(m.namespace, "n")


if __name__ == '__main__':
    unittest.main()
