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

if __name__ == '__main__':
    unittest.main()
