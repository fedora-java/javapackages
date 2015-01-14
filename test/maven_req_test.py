import unittest
import shutil

from test_common import mavenreq, assertIn


class TestMavenReq(unittest.TestCase):

    #@mavenreq(["invalid.xml"])
    #def test_invalid(self, stdout, stderr, return_value):
    #    self.assertNotEqual(return_value, 0)

    #@mavenreq(["not_xml.xml"])
    #def test_not_xml(self, stdout, stderr, return_value):
    #    self.assertNotEqual(return_value, 0)

    #@mavenreq(["nonexistent_file_blablabla"])
    #def test_nonexistent(self, stdout, stderr, return_value):
    #    self.assertNotEqual(return_value, 0)

    @mavenreq(["require1/buildroot/usr/share/maven-metadata/require.xml"])
    def test_require1(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-project)")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require-java/buildroot/usr/share/maven-metadata/require.xml"])
    def test_require_java(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "mvn(org.apache.maven:maven-project)",
                "java-headless >= 1:1.6")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require-java-devel/buildroot/usr/share/maven-metadata/require.xml"])
    def test_require_java_devel(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-project)", "java-devel >= 1:1.6")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require-java-both/buildroot/usr/share/maven-metadata/require.xml"])
    def test_require_java_both(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "mvn(org.apache.maven:maven-project)",
                "java-headless >= 1:1.6", "java-devel >= 1:1.6")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require_parent/buildroot/usr/share/maven-metadata/require.xml"])
    def test_require_parent(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "ns-mvn(org.codehaus.plexus:plexus-ant-factory)")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require_multi/buildroot/usr/share/maven-metadata/require.xml"])
    def test_require_multi(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "ns-mvn(org.codehaus.plexus:plexus-ant-factory)",
                "ns-mvn(codehaus:plexus-utils) = 1.2", "java-headless",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require_multi_namespaces/buildroot/usr/share/maven-metadata/require.xml"])
    def test_require_multi_namespace(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "ns2-mvn(codehaus:plexus-cipher)", "ns-mvn(codehaus:plexus-utils)",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require_multi_versioned/buildroot/usr/share/maven-metadata/require.xml"])
    def test_require_multi_versioned(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("java-headless", "jpackage-utils",
                "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0",
                "ns-mvn(codehaus:plexus-utils:1.2)",
                "ns-mvn(codehaus:plexus-cipher:1.0) = 1.1",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "mvn(org.apache.maven.plugins:maven-idea-plugin:1.5) = 1.4")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require_mixed/buildroot/usr/share/maven-metadata/require.xml"])
    def test_mixed(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "ns-mvn(org.codehaus.plexus:plexus-ant-factory)",
                "ns-mvn(codehaus:plexus-utils) = 1.2",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "mvn(org.apache.maven.plugins:maven-idea-plugin)")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["requires_simple_subpackages/buildroot/usr/share/maven-metadata/require.xml"])
    def test_simple_subpackage(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-plugin-api) = 3.2.1")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["requires_simple_subpackages2/buildroot/usr/share/maven-metadata/require.xml"])
    def test_simple_subpackage2(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-plugin-api) = 3.2.1",
                "mvn(org.codehaus.plexus:plexus-utils)")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["requires_simple_subpackages2_compat/buildroot/usr/share/maven-metadata/require.xml"])
    def test_simple_subpackage3(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                 "mvn(org.apache.maven:maven-plugin-api:3.2.0) = 3.2.1")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["requires_simple_subpackages2_compat2/buildroot/usr/share/maven-metadata/require.xml"])
    def test_simple_subpackage4(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-plugin-api)")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["requires_on_artifact_from_same_package/buildroot/usr/share/maven-metadata/require.xml"])
    def test_simple_artifact_in_same_package(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless")
        self.assertEqual(set(want), set(sout))

    #test for rhbz#1012980
    @mavenreq(["require_skipped/buildroot/usr/share/maven-metadata/require.xml"])
    def test_require_skipped(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')
        lines = stderr.split('\n')
        self.assertEqual(True, len(lines) > 1)
        self.assertEqual(lines[-5], 'org.codehaus.plexus:plexus-ant-factory:1.0 ' \
                                     'required by org.apache.commons-lang:commons-lang')

    # rhbz#1017701 comment 2
    @mavenreq(["aether/buildroot/usr/share/maven-metadata/require.xml"])
    def test_rhbz1017701_c2(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "maven31-mvn(org.eclipse.aether:aether-api) = 0.9.0.M3")
        self.assertEqual(set(want), set(sout))


    @mavenreq(["require1/buildroot/usr/share/maven-metadata/require.xml"], javaconfdirs=['alternative-java'])
    def test_java_config(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-spineless",
                "mvn(org.apache.maven:maven-project)")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require_multi/buildroot/usr/share/maven-metadata/require.xml"], javaconfdirs=['filtered'])
    def test_dep_filtering(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("ns-mvn(org.codehaus.plexus:plexus-ant-factory)", "java-headless",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "jpackage-utils")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require_multi/buildroot/usr/share/maven-metadata/require.xml"], javaconfdirs=['filtered/'])
    def test_config_env1(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("ns-mvn(org.codehaus.plexus:plexus-ant-factory)", "java-headless",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "jpackage-utils")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require_multi/buildroot/usr/share/maven-metadata/require.xml"],
              javaconfdirs=['filtered/', 'alternative-java/'])
    def test_config_env2(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("ns-mvn(org.codehaus.plexus:plexus-ant-factory)", "java-headless",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "jpackage-utils")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require2/buildroot/usr/share/maven-metadata/require.xml"],
              xmvnresolve_output="pom_deps")
    def test_deps_from_pom(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("mvn(org.fedoraproject.xmvn:xmvn-core)",
                "java-headless", "jpackage-utils",
                "mvn(org.fedoraproject.xmvn:xmvn-api)")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require3/buildroot/usr/share/maven-metadata/require.xml"],
              xmvnresolve_output="pom_parent_deps")
    def test_deps_from_pom_with_parent(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("mvn(org.fedoraproject.xmvn:xmvn-core)", "jpackage-utils",
                "mvn(org.fedoraproject.xmvn:xmvn-api:pom:)", "java-headless")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require4/buildroot/usr/share/maven-metadata/require.xml"],
              xmvnresolve_output="subpkg_deps")
    def test_deps_from_pom_on_subpkg(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("mvn(org.fedoraproject.xmvn:xmvn-core)", "jpackage-utils",
                "mvn(org.fedoraproject.xmvn:xmvn-api:pom:) = 1.0", "java-headless")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["require5/buildroot/usr/share/maven-metadata/require.xml"])
    def test_unknown_dep(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        serr = [x for x in stderr.split('\n') if x]
        want = ("org.apache.maven:maven-project:2.2.1")
        assertIn(self, want, serr)

    @mavenreq(["require6/buildroot/usr/share/maven-metadata/require.xml"],
              xmvnresolve_output="pom_deps_fail")
    def test_pom_dep_fail(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        want = ("unresolvable:pom-dependency:pom:2.2.1")
        self.assertTrue(want in stderr, stderr)

    @mavenreq(["osgi_simple/buildroot/usr/share/maven-metadata/require.xml"])
    def test_osgi_basic(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("osgi(osgi.req1)", "jpackage-utils", "java-headless")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["osgi_self/buildroot/usr/share/maven-metadata/require.xml"])
    def test_osgi_self(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["osgi_versioned/buildroot/usr/share/maven-metadata/require.xml"])
    def test_osgi_versioned(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("osgi(osgi.req1) = 1.0", "jpackage-utils", "java-headless")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["osgi_versioned_ns/buildroot/usr/share/maven-metadata/require.xml"])
    def test_osgi_versioned_ns(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("devtoolset-3-osgi(osgi.req1) = 1.0", "jpackage-utils", "java-headless")
        self.assertEqual(set(want), set(sout))

    @mavenreq(["dashes/buildroot/usr/share/maven-metadata/require.xml"])
    def test_dashes(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("mvn(org.apache.maven:maven-plugin-api) = 1.alpha.2",
                "osgi(osgi2) = 1.5.1.SNAPSHOT",
                "java-headless", "jpackage-utils")
        self.assertEqual(set(want), set(sout))

if __name__ == '__main__':
    unittest.main()
