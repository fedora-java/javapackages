import unittest

from test_common import javadocreq

class TestJavadocReq(unittest.TestCase):

    @javadocreq(["something", "that's ignored anyway"])
    def test_javadoc(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual('jpackage-utils\n', stdout)
