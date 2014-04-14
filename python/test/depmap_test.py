import os
import unittest

from javapackages.depmap import Depmap, DepmapInvalidException
from javapackages.artifact import Artifact

from misc import exception_expected

def depmapfile(fname):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            main_dir = os.path.dirname(os.path.realpath(__file__))
            fn(self, Depmap(os.path.join(main_dir, "data/metadata", fname)))
        return test_decorated

    return test_decorator

class TestDepmap(unittest.TestCase):

    @exception_expected(IOError)
    @depmapfile("NULL_FILE.xml")
    def test_nonexisting_depmap(self, d):
        self.assertTrue(False, "IOError was expected!")

    @depmapfile("depmap_compat_new.xml")
    def test_compat_new(self, d):
        pa = d.get_provided_artifacts()
        self.assertEqual(len(pa), 2)
        for a in pa:
            self.assertTrue(a.is_compat())

    @depmapfile("depmap_compat_new.xml")
    def test_java_requires(self, d):
        self.assertEqual(d.get_java_requires(), "1.5")

    @depmapfile("depmap_java_devel.xml")
    def test_java_devel_requires(self, d):
        self.assertEqual(d.get_java_requires(), None)
        self.assertEqual(d.get_java_devel_requires(), "1.5")

    @depmapfile("depmap_compat_new.xml")
    def test_single_provides(self, d):
        self.assertEqual(len(d.get_provided_artifacts()), 2)

    @depmapfile("depmap_new_versioned.xml")
    def test_provided_mappings(self, d):
        artifacts = d.get_provided_mappings()
        self.assertEqual(len(artifacts), 2)
        for a in artifacts:
            self.assertEqual(a.groupId, "org.apache.maven.plugins")
            self.assertEqual(a.artifactId, "maven-idea-plugin")
            self.assertEqual(a.version, "2.2")
            self.assertFalse(a.is_compat())

    @depmapfile("depmap_new_versioned_compressed.xml.gz")
    def test_compressed_depmap(self, d):
        pa = d.get_provided_artifacts()
        self.assertEqual(len(pa), 2)
        for a in pa:
            self.assertFalse(a.is_compat())
            self.assertEqual(a.groupId, "org.apache.maven.plugins")
            self.assertEqual(a.artifactId, "maven-idea-plugin")
            self.assertEqual(a.version, "2.2")

    @depmapfile("depmap_new_compat.xml")
    def test_provided_versioned(self, d):
        artifacts = d.get_provided_mappings()
        self.assertEqual(len(artifacts), 4)
        for a in artifacts:
            self.assertEqual(a.groupId, "org.apache.maven.plugins")
            self.assertEqual(a.artifactId, "maven-idea-plugin")
            self.assertEqual(a.version, "1.4")
            self.assertTrue(a.is_compat())

    @exception_expected(DepmapInvalidException)
    @depmapfile("depmap_invalid_nover.xml")
    def test_no_maven_version(self, d):
        d.get_provided_artifacts()

    @exception_expected(DepmapInvalidException)
    @depmapfile("depmap_invalid_nover.xml")
    def test_no_maven_version_mappings(self, d):
        d.get_provided_mappings()

    @depmapfile("depmap_compat_new.xml")
    def test_multiple_requires(self, d):
        reqs = d.get_required_artifacts()
        self.assertEqual(len(reqs), 4)

        self.assertNotEqual(reqs[0].version, None)
        self.assertEqual(reqs[0].extension, "")
        self.assertEqual(reqs[0].classifier, "")
        self.assertEqual(reqs[0].groupId, "org.codehaus.plexus")
        self.assertEqual(reqs[0].artifactId, "plexus-container-default")

        self.assertEqual(reqs[1].version, "")
        self.assertEqual(reqs[1].extension, "")
        self.assertNotEqual(reqs[1].classifier, None)
        self.assertEqual(reqs[1].groupId, "org.apache.maven.wagon")
        self.assertEqual(reqs[1].artifactId, "wagon-provider-api")
        self.assertEqual(reqs[1].classifier, "test-jar")

        self.assertEqual(reqs[2].version, "")
        self.assertEqual(reqs[2].classifier, "")
        self.assertNotEqual(reqs[2].extension, None)
        self.assertEqual(reqs[2].groupId, "org.codehaus.plexus")
        self.assertEqual(reqs[2].artifactId, "plexus-utils")
        self.assertEqual(reqs[2].extension, "war")

        self.assertEqual(reqs[3].version, "")
        self.assertEqual(reqs[3].classifier, "")
        self.assertEqual(reqs[3].extension, "")
        self.assertEqual(reqs[3].groupId, "org.apache.maven")
        self.assertEqual(reqs[3].artifactId, "maven-project")


    @depmapfile("depmap_namespace.xml")
    def test_namespace(self, d):
        artifacts = d.get_provided_mappings()
        for a in artifacts:
            self.assertEqual(a.namespace, "ns")

    @depmapfile("depmap_multiple_namespaces.xml")
    def test_multiple_namespaces(self, d):
        prov = d.get_provided_artifacts()

        self.assertEqual(len(prov), 6)
        self.assertEqual(prov[0].namespace, "codehaus-plexus")
        self.assertEqual(prov[1].namespace, "codehaus-plexus")
        self.assertEqual(prov[2].namespace, "plexus")
        self.assertEqual(prov[3].namespace, "plexus")
        self.assertEqual(prov[4].namespace, "codehaus")
        self.assertEqual(prov[5].namespace, "codehaus")

    @depmapfile("depmap_namespace_requires.xml")
    def test_requires_namespace(self, d):
        reqs = d.get_required_artifacts()

        self.assertTrue(len(reqs), 5)
        self.assertEqual(reqs[0].namespace, "test")
        self.assertEqual(reqs[1].namespace, "")
        self.assertEqual(reqs[2].namespace, "plexus")
        self.assertEqual(reqs[3].namespace, "codehaus")
        self.assertEqual(reqs[4].namespace, "")

    @exception_expected(DepmapInvalidException)
    @depmapfile("depmap_incorrect_provides.xml")
    def test_incorrect_provides(self, d):
        pass

if __name__ == '__main__':
    unittest.main()
