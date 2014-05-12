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
from javapackages.depmap import Depmap, MetadataInvalidException
from javapackages import Artifact

import sys
import os
from optparse import OptionParser

from javapackages.artifact import *
from javapackages.pom import *
from lxml import etree
import pyxb

from xml.dom.minidom import getDOMImplementation


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


def load_poms(pomdir="/usr/share/maven-poms"):
    pfiles = [os.path.join(pomdir, f) for f in os.listdir(pomdir)]
    poms = []
    return poms.extend([POM(p) for p in pfiles])


def is_it_ivy_file(fpath):
    """Try to determine whether file in given path is Ivy file or not"""
    et = ElementTree()
    doc = et.parse(fpath)

    return doc.tag == "ivy-module"


def add_artifact_elements(root, uart, ppath=None, jpath=None):
    artifacts = []
    for path in [ppath, jpath]:
        if path:
            a = uart.to_metadata()
            if path is ppath:
                if not is_it_ivy_file(ppath):
                    a.extension = "pom"
                else:
                    a.extension = os.path.splitext(pom_path)[1][1:]

                    # add property "type"
                    domimpl = getDOMImplementation()
                    doc  = domimpl.createDocument(None, None, None)
                    ty = doc.createElement('type')
                    te = doc.createTextNode('ivy')
                    ty.appendChild(te)
                    a.properties = pyxb.BIND(ty)

            a.path = os.path.abspath(path)
            artifacts.append(a)

    if root.artifacts is None:
        root.artifacts = pyxb.BIND(*artifacts)
    else:
        for a in artifacts:
            root.artifacts.append(a)


def get_dependency_management(pom_path):

    curr_pom = POM(pom_path)
    dm = []

    if not curr_pom.parentGroupId:
        dm.extend([x for x in curr_pom.get_dependency_management()])
        return dm

    all_poms = load_poms()
    poms = []
    poms.append(curr_pom)

    while poms[-1].parentGroupId:
        for p in all_poms:
            if poms[-1].parentGroupId == p.groupId and poms[-1].parentArtifactId == p.ArtifactId:
                poms.append(p)

    for p in reversed(poms):
        # FIXME: not entirely correct
        dm.append([x for x in p.get_dependency_management()])

    return dm


def get_dependencies(pom_path):
    deps = []

    if pom_path:
        p = POM(pom_path)
        deps.extend([x for x in p.get_dependencies()])
        dep_management = get_dependency_management(pom_path)

        for d in deps:
            for dm in dep_management:
                if d.artifactId == dm.artifactId and d.groupId == dm.groupId:
                    deps.append(Dependency.merge_dependencies(d, dm))
                    deps.pop(deps.index(d))
                    dep_management.pop(dep_management.index(dm))

        try:
            mets = load_metadata()
            for provided in mets.get_provided_artifacts():
                if provided.groupId == p.parentGroupId and provided.artifactId == p.parentArtifactId:
                    for dep in provided.dependencies:
                        deps.append(Dependency.from_metadata(dep))
        except MetadataInvalidException:
            pass

    return deps


if __name__ == "__main__":
    OptionParser.format_epilog = lambda self, formatter: self.epilog
    parser = OptionParser(usage=usage,
                        epilog=epilog)
    parser.add_option("--skip-dependencies", action="store_true", default=False,
                      help="skip dependencies section in resulting metadata")
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

    art = ProvidedArtifact(uart.groupId, uart.artifactId, version=uart.version)
    if hasattr(uart, "extension") and uart.extension:
        art.artifact.extension = uart.extension
    if hasattr(uart, "classifier") and uart.classifier:
        art.artifact.classifier= uart.classifier

    jar_path = None
    if len(args) > 1:
        jar_path = args[1]
        extension = (os.path.splitext(jar_path)[1])[1:]
        if hasattr(art, "extension") and art.extension and art.extension != extension:
            raise ExtensionsDontMatch("Extensions don't match: '%s' != '%s'" % (art.extension, extension))
        else:
            art.extension = extension
    else:
        art.extension = "pom"

    if os.path.exists(config):
        xml = open(config).read()
        metadata = m.CreateFromDocument(xml)
    else:
        metadata = m.metadata()

    if not options.skip_dependencies:
        art.dependencies = get_dependencies(pom_path)

    add_artifact_elements(metadata, art, pom_path, jar_path)

    with open(config, 'w') as f:
        dom = metadata.toDOM(None)
        f.write(dom.toprettyxml(indent="   "))
