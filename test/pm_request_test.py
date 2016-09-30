import unittest
import socket

from test_common import *


class PmRequestTest(unittest.TestCase):

    def setUp(self):
        self.sock_path = "/tmp/test_pm_request_socket"
        self.env = {'PM_REQUEST_SOCKET': self.sock_path}

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.sock_path)
        self.sock.listen(1)

        self.scriptpath = path.join(DIRPATH, '..', 'java-utils', 'request-artifact.py')

    def test_ok(self):
        (out, err, proc) = call_script(self.scriptpath,
                                       ['maven', 'junit:junit'],
                                       extra_env=self.env, async=True)
        conn, _ = self.sock.accept()
        request = conn.makefile().readline().rstrip()
        self.assertEqual(request, "install 'mvn(junit:junit)'")
        conn.sendall(b"ok\n")
        conn.close()
        ret = proc.wait()
        self.assertEqual(ret, 0)

    def test_nok(self):
        (out, err, proc) = call_script(self.scriptpath,
                                       ['maven', 'junit:junit'],
                                       extra_env=self.env, async=True)
        conn, _ = self.sock.accept()
        request = conn.makefile().readline().rstrip()
        self.assertEqual(request, "install 'mvn(junit:junit)'")
        conn.sendall(b"nok\n")
        conn.close()
        ret = proc.wait()
        self.assertEqual(ret, 2)

    def test_jar(self):
        (out, err, proc) = call_script(self.scriptpath,
                                       ['maven', 'gid:aid:jar::'],
                                       extra_env=self.env, async=True)
        conn, _ = self.sock.accept()
        request = conn.makefile().readline().rstrip()
        self.assertEqual(request, "install 'mvn(gid:aid)'")
        conn.sendall(b"ok\n")
        conn.close()
        ret = proc.wait()
        self.assertEqual(ret, 0)

    def test_full_coords(self):
        (out, err, proc) = call_script(self.scriptpath,
                                       ['maven', 'gid:aid:ext:cla:ver'],
                                       extra_env=self.env, async=True)
        conn, _ = self.sock.accept()
        request = conn.makefile().readline().rstrip()
        self.assertEqual(request, "install 'mvn(gid:aid:ext:cla:ver)'")
        conn.sendall(b"ok\n")
        conn.close()
        ret = proc.wait()
        self.assertEqual(ret, 0)

    def test_connection_error(self):
        (out, err, proc) = call_script(self.scriptpath,
                                       ['maven', 'junit:junit'],
                                       extra_env=self.env, async=True)
        conn, _ = self.sock.accept()
        conn.close()
        ret = proc.wait()
        self.assertEqual(ret, 3)

    def test_unsupported_type(self):
        (out, err, ret) = call_script(self.scriptpath,
                                      ['foobar', 'coords'])
        self.assertEqual(ret, 1)
        self.assertEqual(err.rstrip(), "Unsupported artifact type")

    def tearDown(self):
        try:
            os.unlink(self.sock_path)
        except:
            pass


if __name__ == '__main__':
    unittest.main()
