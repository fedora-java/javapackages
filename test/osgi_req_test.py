import unittest

from test_common import *


class TestOSGiReq(unittest.TestCase):

    @osgireq(["basic/buildroot/usr/share/META-INF/MANIFEST.MF"])
    def test_basic(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        assertIn(self, "osgi(org.hamcrest.core)", sout)
        self.assertEqual(len(sout), 1)

    @osgireq(["basic_jar/buildroot/usr/lib/basic.jar"])
    def test_basic_jar(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        assertIn(self, "osgi(org.hamcrest.core)", sout)
        self.assertEqual(len(sout), 1)

    @osgireq(["symlink/buildroot/usr/share/java/foo/META-INF/MANIFEST.MF"])
    def test_symlink(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEqual(len(sout), 0)

    @osgireq(["symlink_jar/buildroot/usr/share/java/foo/basic.jar"])
    def test_symlink_jar(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEqual(len(sout), 0)

    @osgireq(["symlink_dir/buildroot/usr/share/java/foo/META-INF/MANIFEST.MF"])
    def test_symlink_dir(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEqual(len(sout), 0)

    @osgireq(["symlink_dir_jar/buildroot/usr/share/java/foo/basic.jar"])
    def test_symlink_dir_jar(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEqual(len(sout), 0)

    @osgireq(["empty/META-INF/MANIFEST.MF"])
    def test_empty(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEqual(len(sout), 0)

    @osgireq(["self_require/buildroot/usr/share/java/foo/META-INF/MANIFEST.MF"])
    def test_self_require(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        assertIn(self, "osgi(bar) = 4.5.6", sout)
        self.assertEqual(len(sout), 1, sout)

    @osgireq(["corrupt/buildroot/usr/share/java/corrupt.jar"])
    def test_corrupt(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEqual(len(sout), 0, sout)

if __name__ == '__main__':
    unittest.main()
