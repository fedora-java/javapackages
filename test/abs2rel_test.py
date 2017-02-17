import unittest
from test_common import bindir_script


class TestAbs2Rel(unittest.TestCase):

    @bindir_script('abs2rel', ['dummy'])
    def test_usage(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 1)
        self.assertEqual('', stdout)
        self.assertEqual('Usage: abs2rel <PATH> <BASE>\n', stderr)

    @bindir_script('abs2rel', ['/1/2/3/a/b/c', '/1/2/3'])
    def test_abs_abs(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0)
        self.assertEqual('a/b/c\n', stdout)
        self.assertEqual('', stderr)

    @bindir_script('abs2rel', ['foo/bar', 'foo/baz'])
    def test_rel_rel(self, stdout, stderr, return_value):
        self.assertEqual(return_value, 0)
        self.assertEqual('../bar\n', stdout)
        self.assertEqual('', stderr)


if __name__ == '__main__':
    unittest.main()
