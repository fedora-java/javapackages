from test_common import exec_pom_macro, WorkdirTestCase, assertIn
from pom_editor_paths_test import example_tree
import unittest

class TestPomXpathDisable(WorkdirTestCase):
    def test_no_match(self):
        return_value, stderr, report = exec_pom_macro('%pom_xpath_disable nothing submodule', {
            'submodule': 'minimal_pom.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_nonexistent(self):
        return_value, stderr, _ = exec_pom_macro('%pom_xpath_disable nothing', {})
        assertIn(self, "Couldn't locate ", stderr)
        self.assertNotEqual(0, return_value)

    def test_disable_by_aid(self):
        return_value, stderr, report = exec_pom_macro(
               """%pom_xpath_disable "/pom:project/pom:artifactId='common'" """,
               poms_tree=example_tree,
               want_tree={'': 'parent_disabled_common.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_two_levels(self):
        return_value, stderr, report = exec_pom_macro(
                """%pom_xpath_disable "pom:parent[pom:artifactId='intermediate']" """,
               poms_tree=example_tree,
               want_tree={'intermediate': 'intermediate_disabled_schemas.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_skip_level(self):
        poms_tree = dict(example_tree)
        del poms_tree['intermediate/schemas']
        poms_tree['intermediate'] = 'intermediate_skip.xml'
        poms_tree['intermediate/src/schemas'] = 'example_schemas.xml'
        return_value, stderr, report = exec_pom_macro(
                """%pom_xpath_disable "pom:project.build.sourceEncoding='UTF-8'" """,
               poms_tree=poms_tree,
               want_tree={'intermediate': 'intermediate_disabled_schemas.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_fail_on_main(self):
        return_value, stderr, _ = exec_pom_macro(
                """%pom_xpath_disable "pom:groupId='com.example'" """,
               poms_tree=example_tree)
        assertIn(self, "Main POM satisfies the condition", stderr)
        self.assertNotEqual(0, return_value)

if __name__ == '__main__':
    unittest.main()
