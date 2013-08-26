import os
import unittest

from javapackages import Depmap

from misc import exception_expected

def depmapfile(fname):
    def test_decorator(fn):
        def test_decorated(self, *args, **kwargs):
            main_dir = os.path.dirname(os.path.realpath(__file__))
            fn(self, Depmap(os.path.join(main_dir, "data", fname)))
        return test_decorated

    return test_decorator

class TestDepmap(unittest.TestCase):

    @exception_expected(IOError)
    @depmapfile("NULL_FILE.xml")
    def test_nonexisting_depmap(self, d):
        self.assertTrue(False, "IOError was expected!")

    @depmapfile("depmap_compat_old")
    def test_compat_old(self, d):
        self.assertTrue(d.is_compat())

    @depmapfile("depmap_compat_new.xml")
    def test_compat_new(self, d):
        self.assertTrue(d.is_compat())

    @depmapfile("depmap_compat_old")
    def test_missing_java_requires(self, d):
        self.assertIsNone(d.get_java_requires())

    @depmapfile("depmap_compat_new.xml")
    def test_java_requires(self, d):
        self.assertEqual(d.get_java_requires(), "1.5")

    @depmapfile("depmap_compat_new.xml")
    def test_single_provides(self, d):
        self.assertEqual(len(d.get_provided_artifacts()), 1)

    @depmapfile("depmap_compat_old")
    def test_multiple_provides(self, d):
        prov = d.get_provided_artifacts()
        self.assertEqual(len(prov), 5)
        for p in prov:
            self.assertEqual(p.groupId, "org.apache.maven")
            self.assertEqual(p.artifactId, "maven-artifact")
        self.assertEqual(prov[0].version, "2.2.1")
        self.assertEqual(prov[1].version, "2.0.2")
        self.assertEqual(prov[2].version, "2.0.6")
        self.assertEqual(prov[3].version, "2.0.7")
        self.assertEqual(prov[4].version, "2.0.8")

    @depmapfile("depmap_new_nover.xml")
    def test_no_version(self, d):
        prov = d.get_provided_artifacts()
        self.assertEqual(len(prov), 1)
        self.assertEqual(prov[0].version, "")
        self.assertEqual(prov[0].groupId, "org.apache.maven.plugins")
        self.assertEqual(prov[0].artifactId, "maven-idea-plugin")

    @depmapfile("depmap_compat_old")
    def test_no_requires(self, d):
        reqs = d.get_required_artifacts()
        self.assertIsInstance(reqs, list)
        self.assertEqual(len(reqs), 0)

    @depmapfile("depmap_compat_new.xml")
    def test_multiple_requires(self, d):
        reqs = d.get_required_artifacts()
        self.assertEqual(len(reqs), 4)

        self.assertEqual(reqs[0].version, "")
        self.assertEqual(reqs[0].classifier, "")
        self.assertEqual(reqs[0].extension, "")
        self.assertEqual(reqs[0].groupId, "org.apache.maven")
        self.assertEqual(reqs[0].artifactId, "maven-project")

        self.assertEqual(reqs[1].version, "")
        self.assertEqual(reqs[1].extension, "")
        self.assertIsNotNone(reqs[1].classifier)
        self.assertEqual(reqs[1].groupId, "org.apache.maven.wagon")
        self.assertEqual(reqs[1].artifactId, "wagon-provider-api")
        self.assertEqual(reqs[1].classifier, "test-jar")

        self.assertIsNotNone(reqs[2].version)
        self.assertEqual(reqs[2].extension, "")
        self.assertEqual(reqs[2].classifier, "")
        self.assertEqual(reqs[2].groupId, "org.codehaus.plexus")
        self.assertEqual(reqs[2].artifactId, "plexus-container-default")
        self.assertEqual(reqs[2].version, "1.0-alpha-7")

        self.assertEqual(reqs[3].version, "")
        self.assertEqual(reqs[3].classifier, "")
        self.assertIsNotNone(reqs[3].extension)
        self.assertEqual(reqs[3].groupId, "org.codehaus.plexus")
        self.assertEqual(reqs[3].artifactId, "plexus-utils")
        self.assertEqual(reqs[3].extension, "war")



if __name__ == '__main__':
    unittest.main()
