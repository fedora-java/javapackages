from test_common import exec_pom_macro_simple, WorkdirTestCase

class TestGeneric(WorkdirTestCase):
    def test_inject(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                """%pom_xpath_inject "/project/target[@name='init']" '
                       <mkdir dir="lib"/>
                ' build.xml""",
                'build.xml', 'build_with_lib.xml', filename='build.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_remove(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                """%pom_xpath_remove "/project/target[@name='dist']" build.xml""",
                'build.xml', 'build_without_dist.xml', filename='build.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_set(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                """%pom_xpath_set "target[@name='clean']" '<echo/>' build.xml""",
                'build.xml', 'build_set.xml', filename='build.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_set_attribute(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                """%pom_xpath_set "jar/@jarfile" '${dist}/other.jar' build.xml""",
                'build.xml', 'build_attr.xml', filename='build.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_remove_attribute(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                """%pom_xpath_remove "jar/@basedir" build.xml""",
                'build.xml', 'build_attr_removed.xml', filename='build.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_namespace(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                """%pom_xpath_set "target/ivy:cachepath/@type" 'war' build.xml""",
                'build_ns.xml', 'build_ns_set.xml', filename='build.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)



class TestIvy(WorkdirTestCase):
    def test_inject(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                """%pom_xpath_inject dependencies '
                       <dependency org="foo" name="bar" transitive="false"/>
                '""",
                'simple_ivy.xml', 'simple_ivy_added_foo_bar.xml', filename='ivy.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_unsupported(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_remove_parent",
                "simple_ivy.xml", filename='ivy.xml')
        self.assertIn('Operation not supported', stderr)
        self.assertNotEqual(0, return_value)
        self.assertEqual('', report)

    def test_add_dep(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                """%pom_add_dep 'org.eclipse.jetty.orbit:javax.servlet:3.1:servlet->default:false' '
                    <artifact name="javax.servlet" type="orbit" ext="jar"/>
                '""",
                'simple_ivy.xml', 'simple_ivy_added_orbit.xml', filename='ivy.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_remove_dep(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_remove_dep 'xerces:'",
                'simple_ivy.xml', 'simple_ivy_removed_xerces.xml', filename='ivy.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_change_dep(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_change_dep ':xercesImpl' ':xerces'",
                'simple_ivy.xml', 'simple_ivy_xerces_aid.xml', filename='ivy.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_remove_rev(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_change_dep ':nekohtml' '::-'",
                'simple_ivy.xml', 'simple_ivy_remove_rev.xml', filename='ivy.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)


