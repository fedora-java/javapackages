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

import os

import javapackages.common.config as config
from javapackages.common.osgi import OSGiBundle
from javapackages.cache.cache import Cache
from javapackages.cache.metadata import MetadataCache


class OSGiCache(Cache):

    def __init__(self, rpmconf):
        super(OSGiCache, self).__init__(rpmconf)
        self._config_name = config.osgi_cache_f
        self._cache = self._read_cache()
        self._metadata_cache = MetadataCache(rpmconf)

        if self._cache is None:
            self._cache = self._process_buildroot()
            self._write_cache(self._cache)

    def get_bundle_for_path(self, path):
        try:
            return self._cache[path]
        except KeyError:
            pass
        return None

    def get_bundle(self, name):
        for bundle in self._cache.values():
            if bundle == name:
                return bundle
        return None

    def _process_buildroot(self):
        # "path: OSGiBundle" mapping
        cache = {}

        bundle_paths = self._find_paths()
        for path in bundle_paths:
            artifact = self._metadata_cache.get_artifact_for_path(path, can_be_dir=True)
            if artifact and artifact.has_osgi_information():
                bundle = artifact.get_osgi_bundle()
            else:
                bundle = OSGiBundle.from_manifest(path)
                if bundle:
                    if not bundle.namespace and self._scl:
                        bundle.namespace = self._scl
            if bundle:
                cache.update({path: bundle})

        return cache

    def _check_path(self, path):
        if os.path.islink(path):
            return False
        if path.endswith(".jar"):
            return True
        if path.endswith("/MANIFEST.MF"):
            # who knows where the manifest can be in buildroot.
            # this is an attempt to identify only MANIFEST.MF files
            # which are in %{_datadir} or %{_prefix}/lib
            if "/usr/share/" in path or "/usr/lib" in path:
                return True
        return False

    def check_path_in_metadata(self, path):
        artifact = self._metadata_cache.get_artifact_for_path(path,
                                                              can_be_dir=True)
        if artifact and artifact.has_osgi_information():
            return True
        return False
