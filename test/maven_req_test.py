import os
import sys
import unittest

from test_common import *

class TestMavenReq(unittest.TestCase):

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
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "jpackage-utils\nmvn(org.apache.maven:maven-project)\n")

    @mavenreq(["require-java/require.xml"])
    def test_require_java(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "jpackage-utils\nmvn(org.apache.maven:maven-project)\njava >= 1:1.6\n")

    @mavenreq(["require-java-devel/require.xml"])
    def test_require_java_devel(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "jpackage-utils\nmvn(org.apache.maven:maven-project)\njava-devel >= 1:1.6\n")

    @mavenreq(["require-java-both/require.xml"])
    def test_require_java_both(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "jpackage-utils\nmvn(org.apache.maven:maven-project)\njava >= 1:1.6\njava-devel >= 1:1.6\n")

    @mavenreq(["require_parent/require.xml"])
    def test_require_parent(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-runtime\nns-mvn(org.codehaus.plexus:plexus-ant-factory)\n")

    @mavenreq(["require_multi/require.xml"])
    def test_require_multi(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-runtime\nns-mvn(org.codehaus.plexus:plexus-ant-factory)\nns-mvn(codehaus:plexus-utils) = 1.2\nmvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)\n")

    @mavenreq(["require_multi_namespaces/require.xml"])
    def test_require_multi_namespace(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "jpackage-utils\nns-runtime\nns2-runtime\nns2-mvn(codehaus:plexus-cipher)\nns-mvn(codehaus:plexus-utils)\nmvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)\n")

    @mavenreq(["require_multi_versioned/require.xml"])
    def test_require_multi_versioned(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-runtime\nns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0\nns-mvn(codehaus:plexus-utils:1.2)\nns-mvn(codehaus:plexus-cipher:1.0) = 1.1\nmvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)\nmvn(org.apache.maven.plugins:maven-idea-plugin:1.5) = 1.4\n")


    @mavenreq(["require_mixed/require.xml"])
    def test_mixed(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-runtime\nns-mvn(org.codehaus.plexus:plexus-ant-factory)\nns-mvn(codehaus:plexus-utils) = 1.2\nmvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)\nmvn(org.apache.maven.plugins:maven-idea-plugin)\n")

    #test for rhbz#1012980
    @mavenreq(["require_skipped/require.xml"])
    def test_require_skipped(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')
        lines = stderr.split('\n');
        self.assertEquals(True, len(lines) > 1)
        self.assertEquals(lines[-2], '%mvn_package org.codehaus.plexus:plexus-ant-factory:::1.0 <package_name>')

    # rhbz#1017701 comment 2
    @mavenreq(["aether/require.xml"])
    def test_rhbz1017701_c2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "maven31-runtime\nmaven31-mvn(org.eclipse.aether:aether-api) = 0.9.0.M3\n")


if __name__ == '__main__':
        unittest.main()
