import unittest

from javapackages.common.osgi import OSGiRequire, OSGiBundle


class TestOSGi(unittest.TestCase):

    def test_bundle_simple(self):
        b = OSGiBundle.from_string("bundle.name 1")
        self.assertEqual(b.bundle, "bundle.name")
        self.assertEqual(b.version, "1")
        self.assertEqual(b.namespace, "")
        self.assertEqual(b.get_rpm_str(), "osgi(bundle.name) = 1")

    def test_bundle_namespace(self):
        b = OSGiBundle.from_string("bundle.name(ns) 1")
        self.assertEqual(b.bundle, "bundle.name")
        self.assertEqual(b.version, "1")
        self.assertEqual(b.namespace, "ns")
        self.assertEqual(b.get_rpm_str(), "ns-osgi(bundle.name) = 1")

    def test_bundle_requires(self):
        b = OSGiBundle.from_string("bundle.name() 1 req1.abc,req2(ns)")
        self.assertEqual(b.bundle, "bundle.name")
        self.assertEqual(b.version, "1")
        self.assertEqual(b.namespace, "")
        self.assertEqual(b.get_rpm_str(), "osgi(bundle.name) = 1")
        self.assertEqual(len(b.requires), 2)

    def test_bundle_whitespaces(self):
        b = OSGiBundle.from_string("  bundle.name()   1 req1.abc,req2(ns) ")
        self.assertEqual(b.bundle, "bundle.name")
        self.assertEqual(b.version, "1")
        self.assertEqual(b.namespace, "")
        self.assertEqual(b.get_rpm_str(), "osgi(bundle.name) = 1")
        self.assertEqual(len(b.requires), 2)

    def test_require(self):
        r = OSGiRequire.from_string("osgi.req")
        self.assertEqual(r.bundle, "osgi.req")
        self.assertEqual(r.namespace, "")
        self.assertEqual(r.get_rpm_str(), "osgi(osgi.req)")
        self.assertEqual(r.get_rpm_str("1"), "osgi(osgi.req) = 1")

    def test_require_namespace(self):
        r = OSGiRequire.from_string("osgi.req(ns)")
        self.assertEqual(r.bundle, "osgi.req")
        self.assertEqual(r.namespace, "ns")
        self.assertEqual(r.get_rpm_str(), "ns-osgi(osgi.req)")
        self.assertEqual(r.get_rpm_str("1"), "ns-osgi(osgi.req) = 1")


if __name__ == '__main__':
    unittest.main()
