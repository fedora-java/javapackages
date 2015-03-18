#
# Copyright (c) 2015, Red Hat, Inc.
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

from lxml import etree

from javapackages.metadata.artifact import MetadataArtifact
from javapackages.metadata.skippedartifact import MetadataSkippedArtifact
from javapackages.common.exception import JavaPackagesToolsException
from javapackages.common.binding import (ObjectBinding, from_element,
                                         to_element, XMLBindingException)


class MetadataLoadingException(JavaPackagesToolsException):
    pass


class MetadataInvalidException(JavaPackagesToolsException):
    pass


class Metadata(ObjectBinding):
    element_name = 'metadata'
    fields = ['uuid', 'artifacts', 'skippedArtifacts', 'properties']
    types = {'artifacts': [MetadataArtifact],
             'skippedArtifacts': [MetadataSkippedArtifact],
             'properties': dict}
    xmlns = 'http://fedorahosted.org/xmvn/METADATA/2.3.0'

    def __init__(self, *args, **kwargs):
        super(Metadata, self).__init__(*args, **kwargs)
        self._validate_artifacts()

    def _validate_artifacts(self):
        for artifact in self.artifacts:
            if not artifact.version:
                raise MetadataInvalidException(
                    "Artifact {a} does not have version in maven provides"
                    .format(a=artifact))

    def get_provided_artifacts(self):
        """Returns list of MetadataArtifact provided by given metadata."""
        return self.artifacts

    def get_skipped_artifacts(self):
        """Returns list of MetadataSkippedArtifact provided by given metadata."""
        return self.skippedArtifacts

    def get_required_artifacts(self):
        """Returns list of Dependency required by given metadata."""
        dependencies = set()
        for artifact in self.artifacts:
            for dependency in artifact.dependencies:
                dependencies.add(dependency)
        return list(dependencies)

    def get_java_requires(self):
        """Return list of required Java versions."""
        requires = set()
        for artifact in self.artifacts:
            if artifact.properties:
                req = artifact.properties.get("requiresJava", None)
                if req:
                    requires.add(req)
        return list(requires)

    def get_java_devel_requires(self):
        """Not supported."""
        return []

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

    @staticmethod
    def create_from_string(data, path=''):
        """Creates Metadata object from XML string"""
        try:
            xml = etree.fromstring(data)
            return from_element(Metadata, xml)
        except (etree.XMLSyntaxError, XMLBindingException) as e:
            logging.warning("Failed to parse metadata {path}: {e}"
                            .format(path=path, e=e))
            raise MetadataLoadingException()


    @staticmethod
    def create_from_file(path):
        """Creates Metadata object from XML file, that can be gzipped"""
        with open(path, 'rb') as f:
            try:
                gzf = gzip.GzipFile(os.path.basename(path),
                                    'rb', fileobj=f)
                data = gzf.read()
            except IOError:
                # not a compressed metadata, just rewind and read the data
                f.seek(0)
                data = f.read()

        return Metadata.create_from_string(data, path)

    def write_to_file(self, path):
        with open(path, 'wb') as f:
            f.write(etree.tostring(to_element(self), pretty_print=True))
