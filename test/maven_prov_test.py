import os
import sys
import unittest

from test_common import *

class TestMavenProv(unittest.TestCase):

    @mavenprov(["simple.xml"])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 2)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0", sout)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:pom:1.0) = 1.0", sout)

    @mavenprov(["invalid.xml"])
    def test_invalid(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenprov(["not_xml.xml"])
    def test_not_xml(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenprov(["nonexistent_file_blablabla"])
    def test_nonexistent(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenprov(["single_ns.xml"])
    def test_single_ns(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 4)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0", sout)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:pom:1.0) = 1.0", sout)
        assertIn(self, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:1.0) = 9.1.1.b60.25.p2", sout)
        assertIn(self, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:pom:1.0) = 9.1.1.b60.25.p2", sout)

    @mavenprov(["multi_ns.xml"])
    def test_multi_ns(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 4)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0", sout)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:pom:1.0) = 1.0", sout)
        assertIn(self, "ns2-mvn(org.mortbay.jetty:jsp-2.1-glassfish:1.0) = 9.1.1.b60.25.p2", sout)
        assertIn(self, "ns2-mvn(org.mortbay.jetty:jsp-2.1-glassfish:pom:1.0) = 9.1.1.b60.25.p2", sout)

    @mavenprov(["no_version.xml"])
    def test_no_version(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenprov(["simple.xml", "simple2.xml"])
    def test_more_files(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 4)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0", sout)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:pom:1.0) = 1.0", sout)
        assertIn(self, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:6.0.18) = 9.1.1.b60.25.p2", sout)
        assertIn(self, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:pom:6.0.18) = 9.1.1.b60.25.p2", sout)

    @mavenprov(["two_in_one.xml"])
    def test_two_in_one(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenprov(["non_compat.xml"])
    def test_non_compat(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 2)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory) = 1.0", sout)
        assertIn(self, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:pom:) = 1.0", sout)

    @mavenprov(["extension1.xml"])
    def test_extension1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 1)
        assertIn(self, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:war:6.0.18) = 9.1.1.B60.25.p2", sout)

    @mavenprov(["extension2.xml"])
    def test_extension2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 1)
        assertIn(self, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:6.0.18) = 9.1.1.B60.25.p2", sout)

    @mavenprov(["pom_extension.xml"])
    def test__pom_extension(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 1)
        assertIn(self, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:pom:) = 6.0.18", sout)

    @mavenprov(["pom_namespace.xml"])
    def test_namespace_rhbz1017271(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 1)
        assertIn(self, "maven31-mvn(org.apache.maven:apache-maven:pom:) = 3.1.1", sout)

    @mavenprov(["pom_compat.xml"])
    def test_compat_version_in_artifact(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 1)
        assertIn(self, "mvn(org.apache.maven:apache-maven:pom:3.1.1) = 3.1.1", sout)

    @mavenprov(["alias.xml"])
    def test_alias(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 2)
        assertIn(self, "mvn(jakarta-regexp:jakarta-regexp:pom:) = 1.0", sout)
        assertIn(self, "mvn(regexp:regexp:pom:) = 1.0", sout)

    @mavenprov(["alias2.xml"])
    def test_alias2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 4)
        assertIn(self, "mvn(jakarta-regexp:jakarta-regexp:pom:) = 1.0", sout)
        assertIn(self, "mvn(jakarta-regexp:jakarta-regexp) = 1.0", sout)
        assertIn(self, "mvn(regexp:regexp:pom:) = 1.0", sout)
        assertIn(self, "mvn(regexp:regexp) = 1.0", sout)

    @mavenprov(["compat_alias.xml"])
    def test_compat_alias(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 4)
        assertIn(self, "mvn(jakarta-regexp:jakarta-regexp:pom:1.1) = 1.0", sout)
        assertIn(self, "mvn(jakarta-regexp:jakarta-regexp:pom:1.1.1) = 1.0", sout)
        assertIn(self, "mvn(regexp:regexp:pom:1.1) = 1.0", sout)
        assertIn(self, "mvn(regexp:regexp:pom:1.1.1) = 1.0", sout)

if __name__ == '__main__':
    unittest.main()
