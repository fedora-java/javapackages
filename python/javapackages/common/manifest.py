#-
# Copyright (c) 2014, Red Hat, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the Red Hat nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:  Alexander Kurtakov <akurtako@redhat.com>
#           Michal Srb <msrb@redhat.com>

import zipfile
from zipfile import ZipFile


class Manifest(object):

    def __init__(self, path):
        self._path = path
        self._manifest = self._read_manifest()

        if self._manifest is None:
            raise IOError("Unable to open MANIFEST.MF in {path}".format(path=self._path))

    def _read_manifest(self):
        mf = None
        if self._path.endswith("/META-INF/MANIFEST.MF"):
            mf = open(self._path, "rb")
        if zipfile.is_zipfile(self._path):
            # looks like "zipfile.is_zipfile()" is not reliable
            # see rhbz#889131 for more details
            try:
                jarfile = ZipFile(self._path)
                if "META-INF/MANIFEST.MF" in jarfile.namelist():
                    mf = jarfile.open("META-INF/MANIFEST.MF", "rU")
            except IOError:
                pass
        if mf is None:
            return None
        content = mf.read()
        mf.close()
        return content.decode("utf-8")

    def get_requires(self):
        reqs = []
        headers = self._parse_manifest()
        if headers.get("Require-Bundle"):
            for bundle in self._split_bundle_name(headers.get("Require-Bundle")):
                if bundle != "system.bundle":
                    reqs.append(bundle)
        return reqs

    def get_provides(self):
        symbolicName = ""
        version = ""
        for line in self._normalize_manifest():
            if line.startswith("Bundle-SymbolicName:"):
                symbolicName = line.split(':')[1].strip()
                symbolicName = symbolicName.split(";")[0].strip()
            if line.startswith("Bundle-Version:"):
                versions = line.split(':')[1].strip()
                versions = versions.split('.')[0:3]
                version = ".".join(versions)
        return symbolicName, version

    def _normalize_manifest(self):
        lines = []
        manifest = self._manifest.split(u'\n')
        for line in manifest:
            if line.startswith(' '):
                lines[-1] += line.strip()
            else:
                lines.append(line.strip())
        return lines

    def _parse_manifest(self):
        headers = {}
        DELIM = ": "
        for line in self._normalize_manifest():
            split = line.split(DELIM)
            if len(split) > 1:
                name = split[0].strip()
                headers[name] = split[1].strip()
        return headers

    def _split_bundle_name(self, bundles):
        bundlenames = []
        bundleline = ""
        for bundle in bundles.split(','):
            if not bundle:
                continue
            if "(" in bundle or "[" in bundle:
                bundleline = bundle
                continue
            if bundleline:
                bundle = bundleline + bundle
            if ":=optional" in bundle:
                bundleline = ""
                continue
            if ";" in bundle:
                bundlenames.append(bundle.split(";")[0].strip())
            else:
                bundlenames.append(bundle.strip())
            bundleline = ""
        return bundlenames
