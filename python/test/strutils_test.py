import unittest

from javapackages.common.strutils import get_mvn_str, get_rpm_str


class TestStrUtils(unittest.TestCase):

    def test_get_mvn_str(self):
        s = get_mvn_str("g", "a")
        self.assertEqual("g:a", s)
        s = get_mvn_str("g", "a", ext="jar")
        self.assertEqual("g:a", s)
        s = get_mvn_str("g", "a", ext="hpi")
        self.assertEqual("g:a:hpi:", s)
        s = get_mvn_str("g", "a", cla="test")
        self.assertEqual("g:a::test:", s)
        s = get_mvn_str("g", "a", ver="1.0")
        self.assertEqual("g:a:1.0", s)
        s = get_mvn_str("g", "a", ext="zip", cla="sources", ver="2")
        self.assertEqual("g:a:zip:sources:2", s)

    def test_get_rpm_str_basic(self):
        s = get_rpm_str("g", "a")
        self.assertEqual("mvn(g:a)", s)
        s = get_rpm_str("g", "a", ext="jar")
        self.assertEqual("mvn(g:a)", s)
        s = get_rpm_str("g", "a", ext="hpi")
        self.assertEqual("mvn(g:a:hpi:)", s)
        s = get_rpm_str("g", "a", cla="test")
        self.assertEqual("mvn(g:a::test:)", s)

    def test_get_rpm_str_compat(self):
        s = get_rpm_str("g", "a", compat_ver="1.0")
        self.assertEqual("mvn(g:a:1.0)", s)
        s = get_rpm_str("g", "a", compat_ver="1-SNAPSHOT")
        self.assertEqual("mvn(g:a:1-SNAPSHOT)", s)
        s = get_rpm_str("g", "a", ext="zip", compat_ver="1.0")
        self.assertEqual("mvn(g:a:zip:1.0)", s)

    def test_get_rpm_str_versioned(self):
        s = get_rpm_str("g", "a", pkg_ver="1.0")
        self.assertEqual("mvn(g:a) = 1.0", s)
        s = get_rpm_str("g", "a", pkg_ver="1-SNAPSHOT")
        self.assertEqual("mvn(g:a) = 1.SNAPSHOT", s)
        s = get_rpm_str("g", "a", ext="zip", pkg_ver="1.0")
        self.assertEqual("mvn(g:a:zip:) = 1.0", s)

    def test_get_rpm_str_namespace(self):
        s = get_rpm_str("g", "a", namespace="ns1")
        self.assertEqual("ns1-mvn(g:a)", s)


if __name__ == '__main__':
    unittest.main()
