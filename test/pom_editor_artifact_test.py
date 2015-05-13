from test_common import exec_pom_macro_simple, WorkdirTestCase
import unittest

class TestPomArtifact(WorkdirTestCase):
    def test_gid1(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_remove_dep commons-ioX",
                'example_common.xml', 'example_common_removed_commons_iox.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_gid2(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_remove_dep commons-ioX:",
                'example_common.xml', 'example_common_removed_commons_iox.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_aid(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_remove_dep :junit",
                'example_schemas.xml', 'example_schemas_removed_junit.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_all(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_remove_dep :",
                'example_common.xml', 'example_common_removed_all_deps.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_version(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_add_dep org.apache.uima:uimaj:2.5.0",
                'minimal_pom.xml', 'minimal_pom_add_uimaj.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_scope(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_add_dep org.apache.ant:ant-parent::test",
                'minimal_pom.xml', 'minimal_pom_add_ant.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_classifier(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_add_dep org.apache.ant:ant-parent:::cls",
                'minimal_pom.xml', 'minimal_pom_add_cls.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

class TestPomChange(WorkdirTestCase):
    def test_change_simple(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_change_dep junit:junit junit:junit3",
                'example_common.xml', 'example_common_junit3.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_copy_aid1(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_change_dep commons-io org.apache.commons-io",
                'example_common.xml', 'example_common_apache.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_copy_aid2(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_change_dep commons-io: org.apache.commons-io:",
                'example_common.xml', 'example_common_apache.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_copy_gid(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_change_dep :commons-io :commons",
                'example_common.xml', 'example_common_commons.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_remove_scope(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_change_dep :::test :::-",
                'simple_pom.xml', 'simple_removed_scope.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_keep_classifier(self):
        return_value, stderr, report = exec_pom_macro_simple(\
                "%pom_change_dep commons-io org.apache.commons.commons-io:",
                'classifier.xml', 'keep_classifier.xml')
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

if __name__ == '__main__':
    unittest.main()
