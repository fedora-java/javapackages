import unittest

from test_common import javadocreq, assertIn


class TestJavadocReq(unittest.TestCase):

    @javadocreq(["something", "that's ignored anyway"])
    def test_javadoc(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual("jpackage-utils\n", stdout)

    @javadocreq([], javaconfdirs=["javadoc/first", "javadoc/second"])
    def test_configuration(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEqual(len(sout), 1)
        assertIn(self, "SCL-jpackage-utils", sout)

    @javadocreq([], javaconfdirs=["non-existent"])
    def test_missing_configuration(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        self.assertEqual("", stdout)

if __name__ == '__main__':
    unittest.main()
