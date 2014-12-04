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

    def test_bundle_from_properties(self):
        props = {"osgi.id": "bundle.name", "osgi.version": "1"}
        b = OSGiBundle.from_properties(props)
        self.assertEqual(b.bundle, "bundle.name")
        self.assertEqual(b.version, "1")
        self.assertEqual(b.namespace, "")
        self.assertEqual(b.get_rpm_str(), "osgi(bundle.name) = 1")
        self.assertEqual(len(b.requires), 0)

    def test_bundle_from_properties_complex(self):
        props = {"osgi.id": "bundle.name",
                 "osgi.version": "1",
                 "osgi.requires": "req1.abc,req2(ns2)",
                 "osgi.namespace": "ns1"
                 }
        b = OSGiBundle.from_properties(props)
        self.assertEqual(b.bundle, "bundle.name")
        self.assertEqual(b.version, "1")
        self.assertEqual(b.namespace, "ns1")
        self.assertEqual(b.get_rpm_str(), "ns1-osgi(bundle.name) = 1")
        self.assertEqual(len(b.requires), 2)

        self.assertEqual(b.requires[0].bundle, "req1.abc")
        self.assertEqual(b.requires[0].namespace, "")
        self.assertEqual(b.requires[0].get_rpm_str(), "osgi(req1.abc)")

        self.assertEqual(b.requires[1].bundle, "req2")
        self.assertEqual(b.requires[1].namespace, "ns2")
        self.assertEqual(b.requires[1].get_rpm_str(), "ns2-osgi(req2)")

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
