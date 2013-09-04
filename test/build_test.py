import unittest
from test_common import *

class TestMvnbuild(ScriptTest, unittest.TestCase):
    def path(self):
        return "../java-utils/mvn_build.py"

    @compareXmvnArgs([])
    def test_run_no_args(self):
        pass

    @compareXmvnArgs(['-b', ])
    def test_bootstrap(self):
        pass

    @compareXmvnArgs(['-d', ])
    def test_xmvn_debug(self):
        pass

    @compareXmvnConfig(['-d', ])
    def test_xmvn_debug1(self):
        pass

    @compareXmvnArgs(['-f', ])
    def test_force(self):
        pass

    @compareXmvnConfig(['-f', ])
    def test_force1(self):
        pass

    @compareXmvnArgs(['-g', ])
    def test_goal_before(self):
        pass

    @compareXmvnArgs(['-G', ])
    def test_goal_after(self):
        pass

    @compareXmvnArgs(['-i', ])
    def test_skip_install(self):
        pass

    @compareXmvnArgs(['-j', ])
    def test_skip_javadoc(self):
        pass

    @compareXmvnArgs(['-s', ])
    def test_singleton(self):
        pass

    @compareXmvnConfig(['-s', ])
    def test_singleton1(self):
        pass

    @compareXmvnArgs(['-X', ])
    def test_debug(self):
        pass

    @compareXmvnConfig(['-X', ])
    def test_debug1(self):
        pass

if __name__ == '__main__':
    unittest.main()
