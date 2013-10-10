import os
import sys
import unittest

from test_common import *

class TestMavenProv(unittest.TestCase):

    @mavenprov(["simple.xml"])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0\n")

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
    def test_single_ns(self, stdout, stderrr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0\nns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:6.0.18) = 9.1.1.B60.25.p2\n")

    @mavenprov(["multi_ns.xml"])
    def test_multi_ns(self, stdout, stderrr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0\nns2-mvn(org.mortbay.jetty:jsp-2.1-glassfish:6.0.18) = 9.1.1.B60.25.p2\n")

    @mavenprov(["no_version.xml"])
    def test_no_version(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenprov(["simple.xml", "simple2.xml"])
    def test_more_files(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0\nns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:6.0.18) = 9.1.1.B60.25.p2\n")

    @mavenprov(["two_in_one.xml"])
    def test_two_in_one(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenprov(["skip_provides.xml"])
    def test_skip_provides(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0\n")

    @mavenprov(["non_compat.xml"])
    def test_non_compat(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-mvn(org.codehaus.plexus:plexus-ant-factory) = 1.0\n")

    @mavenprov(["extension1.xml"])
    def test_extension1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:war:6.0.18) = 9.1.1.B60.25.p2\n")

    @mavenprov(["extension2.xml"])
    def test_extension2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:war:6.0.18) = 9.1.1.B60.25.p2\n")

    @mavenprov(["pom_extension.xml"])
    def test__pom_extension(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "ns-mvn(org.mortbay.jetty:jsp-2.1-glassfish:6.0.18) = 9.1.1.B60.25.p2\n")

    @mavenprov(["pom_namespace.xml"])
    def test_namespace_rhbz1017271(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        self.assertEquals(stdout, "maven31-mvn(org.apache.maven:apache-maven:pom:) = 3.1.1\n"
                                  "maven31-mvn(org.apache.maven:apache-maven) = 3.1.1\n")

if __name__ == '__main__':
    unittest.main()
