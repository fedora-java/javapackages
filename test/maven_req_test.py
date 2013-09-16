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

    @mavenreq(["require2/require.xml"])
    def test_require_java(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "jpackage-utils\nmvn(org.apache.maven:maven-project)\njava >= 1:1.6\n")
