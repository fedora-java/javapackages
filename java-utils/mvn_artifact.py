#!/usr/bin/python
# Copyright (c) 2013, Red Hat, Inc
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
# 3. Neither the name of Red Hat nor the names of its
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

from __future__ import print_function
import javapackages.metadata as m
from javapackages.depmap import Depmap
from javapackages import Artifact

import sys
import os
import optparse

from javapackages.artifact import *
from javapackages.pom import *
#from lxml.etree import Element, ElementTree, SubElement, Comment
from lxml import etree
import pyxb

class SaneParser(optparse.OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

usage="usage: %prog [options] <MVN spec | POM path> [artifact path]"
epilog="""
MVN spec:
Specification of Maven artifact in following format:

    groupId:artifactId[:extension[:classifier]][:version]

Wildcards (*) and empty parts in specifications are allowed (treated as wildcard).
JAR path must also be specified if this option is used.

Examples of valid specifications:
commons-lang:commons-lang:1.2
commons-lang:commons-lang:war:
commons-lang:commons-lang:war:test-jar:
commons-lang:commons-lang:war:test-jar:3.1
*:commons-lang (equivalent to ':commons-lang')

POM path:
Path where POM file is located.

Artifact path:
Path where Artifact file (usually JAR) is located.
"""

# TODO:
# add basic support for properties
# refactoring needed


config = ".xmvn-reactor"


class ExtensionsDontMatch(Exception):
    pass


def load_metadata(metadatadir="/usr/share/maven-metadata"):
    mfiles = [os.path.join(metadatadir, f) for f in os.listdir(metadatadir)]
    return Depmap(mfiles)

# TODO: move to artifact.py
def artifact_to_metadata(artifact):
    a = m.ArtifactMetadata()
    a.groupId = artifact.groupId
    a.artifactId = artifact.artifactId
    a.version = artifact.version
    if hasattr(artifact, "classifier") and artifact.classifier:
        a.classifier = artifact.classifier
    if artifact.extension:
        a.extension = artifact.extension

    return a


def add_artifact_elements(root, ainfo, deps, ppath=None, jpath=None):
    artifacts = []
    for path in [ppath, jpath]:
        if path:
            a = artifact_to_metadata(ainfo)
            if path is ppath:
                a.extension = "pom"
            a.path = os.path.abspath(path)
            dependencies = []
            for dep in deps:
                dependencies.append(dep)
            a.dependencies = pyxb.BIND(*dependencies)
            artifacts.append(a)

    if root.artifacts is None:
        root.artifacts = pyxb.BIND(*artifacts)
    else:
        for a in artifacts:
            root.artifacts.append(a)


if __name__ == "__main__":
    parser = SaneParser(usage=usage,
                        epilog=epilog)
    for index, arg in enumerate(sys.argv):
        sys.argv[index] = arg.decode(sys.getfilesystemencoding())

    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("At least 1 argument is required")

    try:
        uart = Artifact.from_mvn_str(args[0])
        uart.validate(allow_backref=False)
        if len(args) == 1:
            parser.error("When using artifact specification artifact path must be "
                         "provided")
        if not (uart.groupId and uart.artifactId and uart.version):
            parser.error("Defined artifact has to include at least groupId, "
                         "artifactId and version")
    except (ArtifactFormatException):
        uart = POM(args[0])
        pom_path = args[0]
    else:
        pom_path = None

    jar_path = None
    if len(args) > 1:
        jar_path = args[1]
        extension = (os.path.splitext(jar_path)[1])[1:]
        if hasattr(uart, "extension") and uart.extension and uart.extension != extension:
            raise ExtensionsDontMatch("Extensions don't match: '%s' != '%s'" % (uart.extension, extension))
        else:
            uart.extension = extension
    else:
        uart.extension = "pom"

    if os.path.exists(config):
        xml = open(config).read()
        metadata = m.CreateFromDocument(xml)
    else:
        metadata = m.metadata()

    deps = []
    # try to locate all necessary pom files
    if pom_path:
        mets = load_metadata()
        p = POM(pom_path)
        deps.extend([x.to_metadata() for x in p.get_dependencies()])
        for provided in mets.get_provided_artifacts():
            if (provided.groupId == p.parentGroupId and
                provided.artifactId == p.parentArtifactId):
                for dep in provided.dependencies:
                    deps.append(dep)

    add_artifact_elements(metadata, uart, deps, pom_path, jar_path)

    with open(config, 'w') as f:
        dom = metadata.toDOM(None)
        f.write(dom.toprettyxml(indent="   "))
