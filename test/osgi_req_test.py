import unittest

from test_common import *


class TestOSGiReq(unittest.TestCase):

    def tearDown(self):
        try:
            shutil.rmtree("/tmp/.javapackages_cache/")
        except OSError:
            pass

    @osgireq(["data/osgi/basic/META-INF/MANIFEST.MF"])
    def test_basic(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        assertIn(self, "osgi(org.hamcrest.core)", sout)

    @osgireq(["data/osgi/basic_jar/basic.jar"])
    def test_basic_jar(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        assertIn(self, "osgi(org.hamcrest.core)", sout)

if __name__ == '__main__':
    unittest.main()
