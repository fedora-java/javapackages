from test_common import exec_pom_macro, WorkdirTestCase, assertIn
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

if __name__ == '__main__':
    unittest.main()
