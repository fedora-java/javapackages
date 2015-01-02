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
# Authors:  Michal Srb <msrb@redhat.com>

import javapackages.common.config as config
from javapackages.metadata.metadata import Metadata, MetadataLoadingException
from javapackages.cache.cache import Cache


class MetadataCache(Cache):
    def __init__(self, rpmconf):
        super(MetadataCache, self).__init__(rpmconf)
        self._config_name = config.metadata_cache_f
        self._cache = self._read_cache()

        if self._cache is None:
            self._cache = self._process_buildroot()
            self._write_cache(self._cache)

    def _process_buildroot(self):
        # "path: Metadata" mapping
        cache = {}

        metadata_paths = self._find_paths()
        for path in metadata_paths:
            try:
                metadata = Metadata(path)
                if metadata:
                    cache.update({path: metadata})
            except MetadataLoadingException:
                continue

        return cache

    def _check_path(self, path):
        # TODO
        if "/usr/share/maven-metadata/" in path and path.endswith(".xml"):
            return True
        return False

    def get_artifact_for_path(self, path, can_be_dir=False):
        for metadata in self._cache.values():
            artifact = metadata.get_artifact_for_path(path,
                                                      can_be_dir=can_be_dir)
            if artifact:
                return artifact
        return None

    def get_metadata_for_path(self, path):
        try:
            return self._cache[path]
        except KeyError:
            pass
        return None

    def get_provided_artifacts(self):
        artifacts = []
        for metadata in self._cache.values():
            artifacts.extend(metadata.artifacts)
        return artifacts

    def get_skipped_artifacts(self):
        artifacts = []
        for metadata in self._cache.values():
            artifacts.extend(metadata.skipped_artifacts)
        return artifacts

    def get_provided_osgi(self):
        bundles = []
        for metadata in self._cache.values():
            bundles += metadata.get_osgi_provides()
        return bundles
