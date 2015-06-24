import os
import unittest

from javapackages.common.util import get_buildroot_files


class TestUtil(unittest.TestCase):

    def test_br_files_basic(self):
        br_path = os.path.abspath("data/buildroots/br1/")
        files = get_buildroot_files(regexp="jar$", buildroot_path=br_path)
        self.assertEqual(1, len(files))
        self.assertTrue(next(iter(files)).endswith("/usr/share/java/regular.jar"))


if __name__ == '__main__':
    unittest.main()
