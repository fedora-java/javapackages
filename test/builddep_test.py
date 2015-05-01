import unittest
from test_common import javautils_script


class TestBuilddep(unittest.TestCase):

    cmd = "builddep"
    p = "../test/builddep/"

    @javautils_script(cmd, [p + "compat"])
    def test_compat(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0)
        sout = [x for x in stdout.split('\n') if x]
        want = ("mvn(org.codehaus.groovy:groovy:1.8.9)",)
        self.assertEqual(set(want), set(sout))


if __name__ == '__main__':
    unittest.main()
