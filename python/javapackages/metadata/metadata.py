#-
# Copyright (c) 2014, Red Hat, Inc.
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
# Authors:  Stanislav Ochotnicky <sochotnicky@redhat.com>
#           Michal Srb <msrb@redhat.com>

from __future__ import print_function

import gzip
import logging
import os.path
import xml

from javapackages.metadata.artifact import MetadataArtifact
from javapackages.metadata.dependency import MetadataDependency
from javapackages.metadata.skippedartifact import MetadataSkippedArtifact
import javapackages.metadata.pyxbmetadata as m

import pyxb


class MetadataLoadingException(Exception):
    pass


class MetadataInvalidException(Exception):
    pass


class Metadata(object):

    def __init__(self, path):
        self._path = path
        self.artifacts = []
        self.skipped_artifacts = []
        self.properties = {}

        try:
            metadata = self._load_metadata(self._path)
        except (pyxb.UnrecognizedContentError,
                pyxb.UnrecognizedDOMRootNodeError,
                xml.sax.SAXParseException) as e:
            logging.warning("Failed to parse metadata {path}: {e}"
                            .format(path=path, e=e))
            raise MetadataLoadingException()

        self.artifacts = self._read_artifacts(metadata)
        self.skipped_artifacts = self._read_skipped_artifacts(metadata)
        self.properties = self._read_properties(metadata)

    def _load_metadata(self, metadata_path):
        with open(metadata_path, 'rb') as f:
            try:
                gzf = gzip.GzipFile(os.path.basename(metadata_path),
                                    'rb', fileobj=f)
                data = gzf.read()
            except IOError:
                # not a compressed metadata, just rewind and read the data
                f.seek(0)
                data = f.read()
        return m.CreateFromDocument(data)

    def _read_artifacts(self, metadata):
        artifacts = []
        if metadata.artifacts and metadata.artifacts.artifact:
            for a in metadata.artifacts.artifact:
                artifact = MetadataArtifact.from_metadata(a)
                if not artifact.version:
                    raise MetadataInvalidException("Artifact {a} does not have version in maven provides".format(a=artifact))
                artifacts.append(artifact)
        return artifacts

    def _read_skipped_artifacts(self, metadata):
        artifacts = []
        if metadata.skippedArtifacts and metadata.skippedArtifacts.skippedArtifact:
            for a in metadata.skippedArtifacts.skippedArtifact:
                artifact = MetadataSkippedArtifact.from_metadata(a)
                artifacts.append(artifact)
        return list(artifacts)

    def _read_properties(self, metadata):
        properties = {}
        if hasattr(metadata, 'properties') and metadata.properties:
            properties = dict((prop.tagName, prop.firstChild.value)
                              for prop in metadata.properties.wildcardElements())
        return properties

    def get_provided_artifacts(self):
        """Returns list of MetadataArtifact provided by given metadata."""
        return self.artifacts

    def get_skipped_artifacts(self):
        """Returns list of MetadataSkippedArtifact provided by given metadata."""
        return self.skipped_artifacts

    def get_required_artifacts(self):
        """Returns list of Dependency required by given metadata."""
        dependencies = set()
        for artifact in self.artifacts:
            for dependency in artifact.dependencies:
                dependencies.add(dependency)
        return list(dependencies)

    def get_java_requires(self):
        """Returns JVM version required by metadata or None"""
        try:
            return self.properties[u'requiresJava']
        except KeyError:
            pass
        return None

    def get_java_devel_requires(self):
        """Returns JVM development version required by metadata or None"""
        try:
            return self.properties[u'requiresJavaDevel']
        except KeyError:
            pass
        return None

    def get_osgi_provides(self):
        bundles = []
        for artifact in self.artifacts:
            bundle = artifact.get_osgi_bundle()
            if bundle:
                bundles.append(bundle)
        return bundles

    def get_osgi_requires(self):
        reqs = []
        bundles = self.get_osgi_provides()
        for bundle in bundles:
            reqs.extend(bundle.requires)
        return reqs

    def contains_only_poms(self):
        """Check if metadata file contains only POM file(s)"""
        for artifact in self.artifacts:
            if artifact.extension != "pom":
                return False
        return True

    def get_artifact_for_path(self, path, can_be_dir=False):
        path = os.path.abspath(path)
        for artifact in self.artifacts:
            artifact_path = artifact.get_buildroot_path()
            if can_be_dir:
                # artifact_path can be a directory
                if path.startswith(artifact_path):
                    return artifact
            else:
                if path == artifact_path:
                    return artifact
        return None
