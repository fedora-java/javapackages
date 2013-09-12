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

    @mavenprov(["nonexistent_file_blablabla"])
    def test_nonexistent(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

