import unittest
import shutil
import sys

from test_common import mavenreq, assertIn


class TestMavenReq(unittest.TestCase):

    def tearDown(self):
        try:
            shutil.rmtree("/tmp/.javapackages_cache/")
        except OSError:
            pass

    @mavenreq(["invalid.xml"])
    def test_invalid(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenreq(["not_xml.xml"])
    def test_not_xml(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenreq(["nonexistent_file_blablabla"])
    def test_nonexistent(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)

    @mavenreq(["require1/require.xml"])
    def test_require1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-project)")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require-java/require.xml"])
    def test_require_java(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "mvn(org.apache.maven:maven-project)",
                "java-headless >= 1:1.6")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require-java-devel/require.xml"])
    def test_require_java_devel(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-project)", "java-devel >= 1:1.6")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require-java-both/require.xml"])
    def test_require_java_both(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "mvn(org.apache.maven:maven-project)",
                "java-headless >= 1:1.6", "java-devel >= 1:1.6")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require_parent/require.xml"])
    def test_require_parent(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "ns-mvn(org.codehaus.plexus:plexus-ant-factory)")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require_multi/require.xml"])
    def test_require_multi(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "ns-mvn(org.codehaus.plexus:plexus-ant-factory)",
                "ns-mvn(codehaus:plexus-utils) = 1.2", "java-headless",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require_multi_namespaces/require.xml"])
    def test_require_multi_namespace(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "ns2-mvn(codehaus:plexus-cipher)", "ns-mvn(codehaus:plexus-utils)",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require_multi_versioned/require.xml"])
    def test_require_multi_versioned(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("java-headless", "jpackage-utils",
                "ns-mvn(org.codehaus.plexus:plexus-ant-factory:1.0) = 1.0",
                "ns-mvn(codehaus:plexus-utils:1.2)",
                "ns-mvn(codehaus:plexus-cipher:1.0) = 1.1",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "mvn(org.apache.maven.plugins:maven-idea-plugin:1.5) = 1.4")
        self.assertEquals(set(want), set(sout))


    @mavenreq(["require_mixed/require.xml"])
    def test_mixed(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "ns-mvn(org.codehaus.plexus:plexus-ant-factory)",
                "ns-mvn(codehaus:plexus-utils) = 1.2",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "mvn(org.apache.maven.plugins:maven-idea-plugin)")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["requires_simple_subpackages/require.xml"])
    def test_simple_subpackage(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-plugin-api) = 3.2.1")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["requires_simple_subpackages2/require.xml"])
    def test_simple_subpackage2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-plugin-api) = 3.2.1",
                "mvn(org.codehaus.plexus:plexus-utils)")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["requires_simple_subpackages2_compat/require.xml"])
    def test_simple_subpackage3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                 "mvn(org.apache.maven:maven-plugin-api:3.2.0) = 3.2.1")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["requires_simple_subpackages2_compat2/require.xml"])
    def test_simple_subpackage4(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "mvn(org.apache.maven:maven-plugin-api)")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["requires_on_artifact_from_same_package/require.xml"])
    def test_simple_artifact_in_same_package(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless")
        self.assertEquals(set(want), set(sout))

    #test for rhbz#1012980
    @mavenreq(["require_skipped/require.xml"])
    def test_require_skipped(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertNotEqual(stderr, '')
        lines = stderr.split('\n')
        self.assertEquals(True, len(lines) > 1)
        self.assertEquals(lines[-5], 'org.codehaus.plexus:plexus-ant-factory:1.0 ' \
                                     'required by org.apache.commons-lang:commons-lang')

    # rhbz#1017701 comment 2
    @mavenreq(["aether/require.xml"])
    def test_rhbz1017701_c2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-headless",
                "maven31-mvn(org.eclipse.aether:aether-api) = 0.9.0.M3")
        self.assertEquals(set(want), set(sout))


    @mavenreq(["require1/require.xml"], config='alternative-java')
    def test_java_config(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("jpackage-utils", "java-spineless",
                "mvn(org.apache.maven:maven-project)")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require_multi/require.xml"], config='filtered')
    def test_dep_filtering(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("ns-mvn(org.codehaus.plexus:plexus-ant-factory)", "java-headless",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "jpackage-utils")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require_multi/require.xml"], javaconfdirs=['data/config/filtered'])
    def test_config_env1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("ns-mvn(org.codehaus.plexus:plexus-ant-factory)", "java-headless",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "jpackage-utils")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require_multi/require.xml"],
              javaconfdirs=['data/config/filtered', 'data/config/alternative-java'])
    def test_config_env2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("ns-mvn(org.codehaus.plexus:plexus-ant-factory)", "java-spineless",
                "mvn(org.apache.maven.wagon:wagon-provider-api::test-jar:)",
                "jpackage-utils")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require2/maven-metadata/require.xml"])
    def test_deps_from_pom(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("mvn(org.fedoraproject.xmvn:xmvn-core)",
                "java-headless", "jpackage-utils",
                "mvn(org.fedoraproject.xmvn:xmvn-api)")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require3/maven-metadata/require.xml"])
    def test_deps_from_pom_with_parent(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("mvn(org.fedoraproject.xmvn:xmvn-core)", "jpackage-utils",
                "mvn(org.fedoraproject.xmvn:xmvn-api:pom:)", "java-headless")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require4/maven-metadata/require.xml"])
    def test_deps_from_pom_on_subpkg(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        want = ("mvn(org.fedoraproject.xmvn:xmvn-core)", "jpackage-utils",
                "mvn(org.fedoraproject.xmvn:xmvn-api:pom:) = 1.0", "java-headless")
        self.assertEquals(set(want), set(sout))

    @mavenreq(["require5/require.xml"])
    def test_unknown_dep(self, stdout, stderr, return_value):
        self.assertNotEquals(return_value, 0)
        serr = [x for x in stderr.split('\n') if x]
        want = ("org.apache.maven:maven-project:2.2.1")
        assertIn(self, want, serr)

    @mavenreq(["require6/require.xml"])
    def test_pom_dep_fail(self, stdout, stderr, return_value):
        self.assertNotEquals(return_value, 0)
        serr = [x for x in stderr.split('\n') if x]
        want = ("unresolvable:pom-dependency:pom:2.2.1")
        assertIn(self, want, serr)

if __name__ == '__main__':
    unittest.main()
