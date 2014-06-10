import os
import sys
import unittest

from test_common import *

class TestOSGiProv(unittest.TestCase):

    @osgiprov(["/usr/bin/zip"])
    def test_rhbz889131(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0, stderr)
        sout = [x for x in stdout.split('\n') if x]
        self.assertEquals(len(sout), 0)

if __name__ == '__main__':
    unittest.main()
