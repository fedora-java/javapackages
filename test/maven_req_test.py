import os
import sys
import unittest

from test_common import *

class TestMavenReq(unittest.TestCase):

    def assertIn(self, item, iterable):
        self.assertTrue(item in iterable,
                        msg="{item} not found in {iterable}"
                             .format(item=item,
                                     iterable=iterable))

    @mavenreq(["invalid.xml"])
    def test_invalid(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenreq(["not_xml.xml"])
    def test_not_xml(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenreq(["nonexistent_file_blablabla"])
    def test_nonexistent(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenreq(["require1/require.xml"])
    def test_require1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 2)
        self.assertIn("jpackage-utils", sout)
        self.assertIn("mvn(org.apache.maven:maven-project)", sout)

    @mavenreq(["require-java/require.xml"])
    def test_require_java(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 3)
        self.assertIn("jpackage-utils", sout)
        self.assertIn("mvn(org.apache.maven:maven-project)", sout)
        self.assertIn("java-headless >= 1:1.6", sout)

    @mavenreq(["require-java-devel/require.xml"])
    def test_require_java_devel(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 3)
        self.assertIn("jpackage-utils", sout)
        self.assertIn("mvn(org.apache.maven:maven-project)", sout)
        self.assertIn("java-devel >= 1:1.6", sout)

    @mavenreq(["require-java-both/require.xml"])
    def test_require_java_both(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 4)
        self.assertIn("jpackage-utils", sout)
        self.assertIn("mvn(org.apache.maven:maven-project)", sout)
        self.assertIn("java-headless >= 1:1.6", sout)
        self.assertIn("java-devel >= 1:1.6", sout)

    @mavenreq(["require_parent/require.xml"])
    def test_require_parent(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 2)
        self.assertIn("ns-runtime", sout)
        self.assertIn("ns-mvn(org.codehaus.plexus:plexus-ant-factory)", sout)

    @mavenreq(["require_multi/require.xml"])
    def test_require_multi(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 4)
        self.assertIn("ns-runtime", sout)
        self.assertIn("ns-mvn(org.codehaus.plexus:plexus-ant-factory)", sout)
        self.assertIn("ns-mvn(codehaus:plexus-utils) = 1.2", sout)
        self.assertIn("mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)", sout)

    @mavenreq(["require_multi_namespaces/require.xml"])
    def test_require_multi_namespace(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 6)
        self.assertIn("jpackage-utils", sout)
        self.assertIn("ns-runtime", sout)
        self.assertIn("ns2-runtime", sout)
        self.assertIn("ns2-mvn(codehaus:plexus-cipher)", sout)
        self.assertIn("ns-mvn(codehaus:plexus-utils)", sout)
        self.assertIn("mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)", sout)

    @mavenreq(["require_multi_versioned/require.xml"])
    def test_require_multi_versioned(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 6)
        self.assertIn('ns-runtime', sout)
        self.assertIn('ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0', sout)
        self.assertIn('ns-mvn(codehaus:plexus-utils:1.2)', sout)
        self.assertIn('ns-mvn(codehaus:plexus-cipher:1.0) = 1.1', sout)
        self.assertIn('mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)', sout)
        self.assertIn('mvn(org.apache.maven.plugins:maven-idea-plugin:1.5) = 1.4', sout)


    @mavenreq(["require_mixed/require.xml"])
    def test_mixed(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 5)
        self.assertIn("ns-runtime", sout)
        self.assertIn("ns-mvn(org.codehaus.plexus:plexus-ant-factory)", sout)
        self.assertIn("ns-mvn(codehaus:plexus-utils) = 1.2", sout)
        self.assertIn("mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)", sout)
        self.assertIn("mvn(org.apache.maven.plugins:maven-idea-plugin)", sout)

    #test for rhbz#1012980
    @mavenreq(["require_skipped/require.xml"])
    def test_require_skipped(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')
        lines = stderr.split('\n');
        self.assertEquals(True, len(lines) > 1)
        print stderr
        self.assertEquals(lines[-5], 'org.codehaus.plexus:plexus-ant-factory:::1.0 ' \
                                     'required by org.apache.commons-lang:commons-lang')

    # rhbz#1017701 comment 2
    @mavenreq(["aether/require.xml"])
    def test_rhbz1017701_c2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEqual(len(sout), 2)
        self.assertIn("maven31-runtime", sout)
        self.assertIn("maven31-mvn(org.eclipse.aether:aether-api) = 0.9.0.M3", sout)


if __name__ == '__main__':
        unittest.main()
