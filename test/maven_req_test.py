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

    @mavenreq(["require2/require.xml"])
    def test_require_parent(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "jpackage-utils\nns-mvn(org.codehaus.plexus:plexus-ant-factory) = 1.0\n")

    @mavenreq(["require3/require.xml"])
    def test_require_multi(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "jpackage-utils\nns-mvn(org.codehaus.plexus:plexus-ant-factory) = 1.0\nns-mvn(codehaus:plexus-utils) = 1.2\nmvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)\n")
