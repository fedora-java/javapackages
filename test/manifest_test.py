import os
import shutil
import tempfile
import unittest
import zipfile

from javapackages.common.manifest import Manifest


def _folded_utf8_manifest(line_ending):
    # UTF-8 bytes for "Boué" split across a folded manifest continuation line.
    return b"".join([
        b"Manifest-Version: 1.0" + line_ending,
        b"Bundle-SymbolicName: org.example.bundle" + line_ending,
        b"Bundle-Version: 1.2.3" + line_ending,
        b"Built-By: Guillaume Bou\xc3" + line_ending,
        b" \xa9" + line_ending,
        line_ending,
    ])


def _ascii_folded_manifest(line_ending):
    return b"".join([
        b"Manifest-Version: 1.0" + line_ending,
        b"Bundle-SymbolicName: org.example.bundle" + line_ending,
        b"Bundle-Version: 1.2.3" + line_ending,
        b"Built-By: Jane" + line_ending,
        b" Doe" + line_ending,
        line_ending,
    ])


class TestManifestUtf8Folding(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp(prefix="jpkg-manifest-")

    def tearDown(self):
        shutil.rmtree(self.workdir)

    def test_folded_utf8_manifest_file(self):
        meta_inf = os.path.join(self.workdir, "META-INF")
        os.makedirs(meta_inf)
        manifest_path = os.path.join(meta_inf, "MANIFEST.MF")

        with open(manifest_path, "wb") as f:
            f.write(_folded_utf8_manifest(b"\r\n"))

        manifest = Manifest(manifest_path)
        self.assertEqual(("org.example.bundle", "1.2.3"), manifest.get_provides())
        headers = manifest._parse_manifest()
        self.assertEqual("Guillaume Boué", headers.get("Built-By"))

    def test_folded_utf8_manifest_in_jar(self):
        jar_path = os.path.join(self.workdir, "sample.jar")
        with zipfile.ZipFile(jar_path, "w") as zf:
            zf.writestr("META-INF/MANIFEST.MF", _folded_utf8_manifest(b"\r\n"))

        manifest = Manifest(jar_path)
        self.assertEqual(("org.example.bundle", "1.2.3"), manifest.get_provides())
        headers = manifest._parse_manifest()
        self.assertEqual("Guillaume Boué", headers.get("Built-By"))

    def test_folded_utf8_manifest_lf_endings(self):
        meta_inf = os.path.join(self.workdir, "META-INF")
        os.makedirs(meta_inf)
        manifest_path = os.path.join(meta_inf, "MANIFEST.MF")

        with open(manifest_path, "wb") as f:
            f.write(_folded_utf8_manifest(b"\n"))

        manifest = Manifest(manifest_path)
        headers = manifest._parse_manifest()
        self.assertEqual("Guillaume Boué", headers.get("Built-By"))

    def test_ascii_continuation_still_works(self):
        meta_inf = os.path.join(self.workdir, "META-INF")
        os.makedirs(meta_inf)
        manifest_path = os.path.join(meta_inf, "MANIFEST.MF")

        with open(manifest_path, "wb") as f:
            f.write(_ascii_folded_manifest(b"\r\n"))

        manifest = Manifest(manifest_path)
        headers = manifest._parse_manifest()
        self.assertEqual("JaneDoe", headers.get("Built-By"))


if __name__ == '__main__':
    unittest.main()
