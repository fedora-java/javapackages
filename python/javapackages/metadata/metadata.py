#!/usr/bin/python
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

from javapackages.maven.artifact import (MetadataDependency, MetadataArtifact,
                                         MetadataSkippedArtifact, MetadataExclusion)
import pyxb

import javapackages.metadata.pyxbmetadata as metadata
from xml.dom.minidom import getDOMImplementation


class MetadataLoadingException(Exception):
    pass

class MetadataInvalidException(Exception):
    pass

class Metadata(object):

    def __init__(self, path):
        if type(path) == list:
            self.__paths = path
        else:
            self.__paths = [path]
        self.__metadata = []
        for p in self.__paths:
            try:
                self.__load_metadata(p)
            except (pyxb.UnrecognizedContentError,
                    pyxb.UnrecognizedDOMRootNodeError,
                    xml.sax.SAXParseException) as e:
                logging.warning("Failed to parse metadata {path}: {e}"
                                .format(path=path,
                                        e=e))
        if len(self.__metadata) == 0:
            raise MetadataInvalidException("None of metadata paths could be parsed")


    def __load_metadata(self, metadata_path):
        with open(metadata_path) as f:
            try:
                gzf = gzip.GzipFile(os.path.basename(metadata_path),
                                    'rb',
                                    fileobj=f)
                data = gzf.read()
            except IOError:
                # not a compressed fragment, just rewind and read the data
                f.seek(0)
                data = f.read()

            self.__metadata.append(metadata.CreateFromDocument(data))

    def get_provided_artifacts(self):
        """Returns list of Artifact provided by given depmap."""

        artifacts = []
        for m in self.__metadata:
            for a in m.artifacts.artifact:
                artifact = ProvidedArtifact.from_metadata(a)
                if not artifact.version:
                    raise MetadataInvalidException("Artifact {a} does not have version in maven provides".format(a=artifact))
                artifacts.append(artifact)
        return artifacts


    def get_required_artifacts(self):
        """Returns list of Artifact required by given depmap."""
        artifacts = set()
        for m in self.__metadata:
            for a in m.artifacts.artifact:
                if not a.dependencies:
                    continue

                for dep in a.dependencies.dependency:
                    artifacts.add(Dependency.from_metadata(dep))

        return sorted(list(artifacts))

    def get_skipped_artifacts(self):
        """Returns list of Artifact that were build but not installed"""
        artifacts = set()
        for m in self.__metadata:
            if not m.skippedArtifacts:
                continue
            for dep in m.skippedArtifacts.skippedArtifact:
                artifact = SkippedArtifact.from_metadata(dep)
                artifacts.add(artifact)
        return sorted(list(artifacts))

    def get_excluded_artifacts(self):
        """Returns list of Artifacts that should be skipped for requires"""
        artifacts = set()
        for m in self.__metadata:
            for a in m.artifacts.artifact:
                if not a.dependencies:
                    continue

                for dep in a.dependencies.dependency:
                    if not dep.exclusions:
                        continue

                    for exclusion in dep.exclusions.exclusion:
                        artifact = ExclusionArtifact.from_metadata(exclusion)
                artifacts.add(artifact)
        return sorted(list(artifacts))


    def get_java_requires(self):
        """Returns JVM version required by depmap or None"""
        for m in self.__metadata:
            if not m.properties:
                return None
            for prop in m.properties.wildcardElements():
                if prop.tagName == u'requiresJava':
                    return prop.firstChild.value
        return None

    def get_java_devel_requires(self):
        """Returns JVM development version required by depmap or None"""
        for m in self.__metadata:
            if not m.properties:
                return None
            for prop in m.properties.wildcardElements():
                if prop.tagName == u'requiresJavaDevel':
                    return prop.firstChild.value
        return None

    @staticmethod
    def build_property(name, value):
        domimpl = getDOMImplementation()
        doc = domimpl.createDocument(None, None, None)
        elem = doc.createElement(name)
        tnode = doc.createTextNode(value)
        elem.appendChild(tnode)
        return elem
