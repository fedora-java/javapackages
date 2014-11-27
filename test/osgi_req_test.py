import unittest

from test_common import *


class TestOSGiReq(unittest.TestCase):

    def tearDown(self):
        try:
            shutil.rmtree("/tmp/.javapackages_cache/")
        except OSError:
            pass

    @osgireq(["data/osgi/basic/buildroot/usr/share/META-INF/MANIFEST.MF",
              "data/osgi/basic/buildroot/"])
    def test_basic(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        assertIn(self, "osgi(org.hamcrest.core)", sout)

    @osgireq(["data/osgi/basic_jar/buildroot/usr/lib/basic.jar",
              "data/osgi/basic_jar/buildroot/"])
    def test_basic_jar(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        assertIn(self, "osgi(org.hamcrest.core)", sout)

    @osgireq(["data/osgi/empty/META-INF/MANIFEST.MF"])
    def test_empty(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEqual(len(sout), 0)

if __name__ == '__main__':
    unittest.main()
