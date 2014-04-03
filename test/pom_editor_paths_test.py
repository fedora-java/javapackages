from test_common import exec_pom_macro, WorkdirTestCase

class TestPomPath(WorkdirTestCase):
    def test_sanity(self):
        return_value, stderr, report = exec_pom_macro('', {
            'submodule': 'minimal_pom.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_default_nonexistent(self):
        return_value, stderr, _ = exec_pom_macro('%pom_remove_parent', {})
        self.assertIn("Couldn't locate ", stderr)
        self.assertNotEqual(0, return_value)

    def test_submodule_nonexistent(self):
        return_value, stderr, _ = exec_pom_macro('%pom_remove_parent submodule', {})
        self.assertIn("Couldn't locate ", stderr)
        self.assertNotEqual(0, return_value)

    def test_default(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_parent',
                poms_tree={'': 'minimal_pom.xml'},
                want_tree={'': 'minimal_removed_parent.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_explicit(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_parent pom.xml',
                poms_tree={'': 'minimal_pom.xml'},
                want_tree={'': 'minimal_removed_parent.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_submodule_default(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_parent submodule',
                poms_tree={'submodule': 'minimal_pom.xml'},
                want_tree={'submodule': 'minimal_removed_parent.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_submodule_explicit(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_parent submodule',
                poms_tree={'submodule': 'minimal_pom.xml'},
                want_tree={'submodule': 'minimal_removed_parent.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_submodule_more_levels(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_parent submodule/something',
                poms_tree={'submodule/something': 'minimal_pom.xml'},
                want_tree={'submodule/something': 'minimal_removed_parent.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

class TestMorePoms(WorkdirTestCase):
    def test_submodules_default(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_parent submodule1 submodule2',
                poms_tree={'submodule1': 'minimal_pom.xml',
                    'submodule2': 'simple_pom.xml'},
                want_tree={'submodule1': 'minimal_removed_parent.xml',
                    'submodule2': 'simple_removed_parent.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_submodules_different_levels(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_parent . submodule2',
                poms_tree={'submodule1': 'minimal_pom.xml',
                    'submodule2': 'simple_pom.xml',
                    '': 'minimal_pom.xml'},
                want_tree={'submodule2': 'simple_removed_parent.xml',
                    '': 'minimal_removed_parent.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_many_submodules(self):
        poms = ['submodule{0}'.format(i) for i in range(10)]
        command = '%pom_remove_parent ' + ' '.join(poms)
        poms_tree = {'untouched': 'minimal_pom.xml'}
        want_tree = {}
        for pom in poms:
            poms_tree[pom] = 'simple_pom.xml'
            want_tree[pom] = 'simple_removed_parent.xml'
        return_value, stderr, report = exec_pom_macro(command, poms_tree, want_tree)
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_submodules_partial_match(self):
        return_value, stderr, _ = exec_pom_macro(\
                '%pom_remove_dep :commons-io submodule1 submodule2',
                poms_tree={'submodule1': 'minimal_pom.xml',
                    'submodule2': 'simple_pom.xml'})
        self.assertIn("Error", stderr)
        self.assertIn("not found", stderr)
        self.assertNotEqual(0, return_value)

    def test_submodules_partial_match_force(self):
        return_value, stderr, report = exec_pom_macro(\
                '%pom_remove_dep -f :commons-io submodule1 submodule2',
                poms_tree={'submodule1': 'minimal_pom.xml',
                    'submodule2': 'simple_pom.xml'},
                want_tree={'submodule2': 'simple_removed_commons_io.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

class TestRecursive(WorkdirTestCase):
    example_tree = {
            '': 'example_parent.xml',
            'common': 'example_common.xml',
            'intermediate': 'example_intermediate.xml',
            'intermediate/schemas': 'example_schemas.xml'}

    def test_default_recursive1(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_dep -r :commons-io',
                poms_tree=self.example_tree,
                want_tree={'intermediate': 'example_intermediate_removed_commons_io.xml',
                    'common': 'example_common_removed_commons_io.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_default_recursive2(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_dep -r :junit',
                poms_tree=self.example_tree,
                want_tree={'intermediate/schemas': 'example_schemas_removed_junit.xml',
                    'common': 'example_common_removed_junit.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_recursive_plugin_with_module(self):
        poms_tree = dict(self.example_tree)
        poms_tree[''] = 'example_parent_plugin_with_module.xml'
        return_value, stderr, report = exec_pom_macro('%pom_remove_dep -r :junit',
                poms_tree=poms_tree,
                want_tree={'intermediate/schemas': 'example_schemas_removed_junit.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_default_recursive_profile(self):
        poms_tree = dict(self.example_tree)
        poms_tree[''] = 'example_parent_profile.xml'
        return_value, stderr, report = exec_pom_macro('%pom_remove_dep -r :commons-io',
                poms_tree=poms_tree,
                want_tree={'intermediate': 'example_intermediate_removed_commons_io.xml',
                    'common': 'example_common_removed_commons_io.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_recursive_no_match(self):
        return_value, stderr, _ = exec_pom_macro('%pom_remove_dep -r :not-there',
                poms_tree=self.example_tree)
        self.assertIn("Error", stderr)
        self.assertIn("not found", stderr)
        self.assertNotEqual(0, return_value)

    def test_recursive_missing(self):
        poms_tree = dict(self.example_tree)
        del poms_tree['intermediate/schemas']
        return_value, stderr, _ = exec_pom_macro('%pom_remove_dep -r :commons-io',
                poms_tree=poms_tree)
        self.assertIn("Cannot read", stderr)
        self.assertNotEqual(0, return_value)

    def test_recursive_subpom(self):
        return_value, stderr, report = exec_pom_macro('%pom_remove_dep -r :junit intermediate',
                poms_tree=self.example_tree,
                want_tree={'intermediate/schemas': 'example_schemas_removed_junit.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_recursive_multiple(self):
        poms_tree = dict(self.example_tree)
        return_value, stderr, report = exec_pom_macro('%pom_remove_dep -r :junit intermediate common',
                poms_tree=poms_tree,
                want_tree={'intermediate/schemas': 'example_schemas_removed_junit.xml',
                    'common': 'example_common_removed_junit.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_recursive_partial_match(self):
        return_value, stderr, _ = exec_pom_macro('%pom_remove_dep -r commons-ioX intermediate common',
                poms_tree=self.example_tree)
        self.assertIn("Error", stderr)
        self.assertIn("not found", stderr)
        self.assertNotEqual(0, return_value)

    def test_recursive_partial_match_forced(self):
        return_value, stderr, report = exec_pom_macro(\
                '%pom_remove_dep -rf commons-ioX:commons-io intermediate common',
                poms_tree=self.example_tree,
                want_tree={'common': 'example_common_removed_commons_iox.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

class TestAttributeRecognition(WorkdirTestCase):
    def test_default_extra_xml(self):
        return_value, stderr, report = exec_pom_macro('\
                %pom_add_dep org.apache.uimaj:uimaj-core "<scope>test</scope>"',
                poms_tree={'': 'minimal_pom.xml'},
                want_tree={'': 'minimal_add_dep_scope.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_explicit_extra_xml(self):
        return_value, stderr, report = exec_pom_macro('\
                %pom_add_dep org.apache.uimaj:uimaj-core pom.xml "<scope>test</scope>"',
                poms_tree={'': 'minimal_pom.xml'},
                want_tree={'': 'minimal_add_dep_scope.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_submodule_extra_xml(self):
        return_value, stderr, report = exec_pom_macro('\
                %pom_add_dep org.apache.uimaj:uimaj-core submodule "<scope>test</scope>"',
                poms_tree={'submodule': 'minimal_pom.xml'},
                want_tree={'submodule': 'minimal_add_dep_scope.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_submodules_extra_xml(self):
        return_value, stderr, report = exec_pom_macro(\
                '%pom_add_dep org.apache.uimaj:uimaj-core submodule1 submodule2 "<scope>test</scope>"',
                poms_tree={'submodule1': 'minimal_pom.xml',
                    'submodule2': 'minimal_pom.xml'},
                want_tree={'submodule1': 'minimal_add_dep_scope.xml',
                    'submodule2': 'minimal_add_dep_scope.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_dep_mgmt_extra_xml(self):
        return_value, stderr, report = exec_pom_macro(\
                '%pom_add_dep_mgmt org.apache.uimaj:uimaj-core submodule1 submodule2 "<scope>test</scope>"',
                poms_tree={'submodule1': 'minimal_pom.xml',
                    'submodule2': 'minimal_pom.xml'},
                want_tree={'submodule1': 'minimal_add_dep_mgmt_scope.xml',
                    'submodule2': 'minimal_add_dep_mgmt_scope.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)

    def test_plugin_extra_xml(self):
        return_value, stderr, report = exec_pom_macro(\
                '%pom_add_plugin org.apache.maven:maven-remote-resources-plugin \
                submodule1 submodule2 "<goal>generate-resources</goal>"',
                poms_tree={'submodule1': 'minimal_pom.xml',
                    'submodule2': 'minimal_pom.xml'},
                want_tree={'submodule1': 'minimal_add_plugin_resource.xml',
                    'submodule2': 'minimal_add_plugin_resource.xml'})
        self.assertEqual(0, return_value, stderr)
        self.assertEqual('', report, report)
