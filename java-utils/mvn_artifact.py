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
from javapackages import Artifact

import sys
import os
import optparse

from javapackages.artifact import *
from javapackages.pom import *
#from lxml.etree import Element, ElementTree, SubElement, Comment
from lxml import etree


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


def find_parent_pom(parent):
    # FIXME: not nice...
    pomdir = "/usr/share/maven-poms"

    for root, dirs, filenames in os.walk(pomdir):
        for pomfile in filenames:
            pompath = os.path.join(root, pomfile)
            pom = POM(pompath)
            if parent.groupId == pom.groupId and parent.artifactId == pom.artifactId:
                return pompath
    return None


# TODO: something like this should be probably implemented in pom.py
def pom_get_parent(ppath):

    pom = etree.parse(ppath)
    parent = pom.xpath('/pom:project/pom:parent', namespaces=dict(pom='http://maven.apache.org/POM/4.0.0'))
    if len(parent) == 0:
        parent = pom.xpath('/project/parent')
    if len(parent) == 0:
        return None

    return Artifact.from_xml_element(parent[0])


def get_dependencies(ppath):
    """Return set of dependencies from specified POM file."""
    pom = etree.parse(ppath)
    # TODO: something like this should be probably implemented in
    # pom.py/artifact.py
    dependencies = pom.xpath('/pom:project/pom:dependencies/pom:dependency',
                             namespaces=dict(pom='http://maven.apache.org/POM/4.0.0'))
    if len(dependencies) == 0:
        dependencies = pom.xpath('/project/dependencies/dependency')

    result = set()
    for dep in dependencies:
        adep = Artifact.from_xml_element(dep)

        # skip dependencies with scope "test" and "provided"
        scope = dep.find('./{*}scope')
        if scope is not None and scope.text in ["test", "provided"]:
            continue

        exclusions = set()
        exclxml = dep.find('./{*}exclusions')
        if exclxml is not None:
            for excl in exclxml:
                gid = excl.find('./{*}groupId').text
                aid = excl.find('./{*}artifactId').text
                e = m.DependencyExclusion(gid, aid)
                exclusions.add(e)

        d = m.Dependency()
        d.groupId = adep.groupId
        d.artifactId = adep.artifactId
        if adep.classifier:
            d.classifier = adep.classifier
        if adep.extension:
            d.extension = adep.extension
        d.requestedVersion = adep.version

        if len(exclusions) != 0:
            d.exclusions = m.CTD_ANON_7()
            for e in exclusions:
                d.exclusions.append(e)

        result.add(d)

    return result

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
    if root.artifacts is None:
        root.artifacts = m.CTD_ANON_()

    for path in [ppath, jpath]:
        if path:
            a = artifact_to_metadata(ainfo)
            if path is ppath:
                a.extension = "pom"
            a.path = os.path.abspath(path)
            a.dependencies = m.CTD_ANON_6()
            for dep in deps:
                a.dependencies.append(dep)
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

    # try to locate all necessary pom files
    poms = []
    if pom_path:
        poms.append(pom_path)
        while True:
            newparent = pom_get_parent(poms[-1])
            if newparent:
                parentfile = find_parent_pom(newparent)
                if parentfile and parentfile not in poms:
                    poms.append(parentfile)
                else:
                    break
            else:
                break

    # read dependencies from all pom files
    deps = []
    for pom in poms:
        deps += get_dependencies(pom)

    add_artifact_elements(metadata, uart, deps, pom_path, jar_path)

    with open(config, 'w') as f:
        dom = metadata.toDOM(None)
        f.write(dom.toprettyxml(indent="   "))
