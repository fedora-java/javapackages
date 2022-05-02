#
# Copyright (c) 2014-2016, Red Hat, Inc.
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

from javapackages.maven.pom import POM, PomLoadingException

from javapackages.xmvn.xmvn_resolve import (XMvnResolve, ResolutionRequest,
                                            XMvnResolveException)
from javapackages.common.util import args_to_unicode
from javapackages.common.exception import JavaPackagesToolsException

import sys
import os
from xml.etree import ElementTree
from optparse import OptionParser


usage = "usage: %prog <Source POM> <Output POM>"
epilog = """
Resolves pom file from its parents and sanitizes its
dependencies so that it includes only those that have
compile or runtime scope.

Source POM:
Path where POM file is located.

Output POM:
Path where the sanitized POM file will be written to.
"""


def get_parent_pom(pom):

    req = ResolutionRequest(pom.groupId, pom.artifactId,
                            extension="pom", version=pom.version)
    result = XMvnResolve.process_raw_request([req])[0]
    if not result:
        raise XMvnResolveException("Unable to resolve parent POM {g}:{a}:{e}:{v}"
                                   .format(g=pom.groupId, a=pom.artifactId,
                                           e="pom", v=pom.version))

    return POM(result.artifactPath)


def merge_sections(main, update):
    for upd in update:
        for curr in main:
            if curr.compare_to(upd):
                curr.merge_with(upd)
                break
        else:
            main.append(upd)


def get_model_variables(pom):
    props = {}
    if pom.groupId:
        props["project.groupId"] = pom.groupId
    if pom.artifactId:
        props["project.artifactId"] = pom.artifactId
    if pom.version:
        props["project.version"] = pom.version
    return props


def expand_props(deps, props):
    for d in deps:
        d.interpolate(props)


def add_artifact_elements(metadata, art_template, ppath=None, jpath=None):
    for path in [ppath, jpath]:
        if path:
            art = art_template.copy()
            art.path = os.path.abspath(path)
            metadata.artifacts.append(art)


def gather_dependencies(pom_path):
    if not pom_path:
        return []
    pom = POM(pom_path)
    pom_props = get_model_variables(pom)
    deps, depm, props = _get_dependencies(pom)
    # expand project model variables
    expand_props(deps, pom_props)
    expand_props(depm, pom_props)

    curr_pom = pom
    parent = pom.parent
    while parent:
        ppom = None
        if parent.relativePath:
            try:
                ppom_path = os.path.join(os.path.dirname(curr_pom._path),
                                         parent.relativePath)
                if os.path.isdir(ppom_path):
                    ppom_path = os.path.join(ppom_path, 'pom.xml')
                ppom = POM(ppom_path)
            except PomLoadingException:
                pass
        else:
            try:
                ppom_path = os.path.join(os.path.dirname(curr_pom._path), '..')
                if os.path.isdir(ppom_path):
                    ppom_path = os.path.join(ppom_path, 'pom.xml')
                ppom = POM(ppom_path)
            except PomLoadingException:
                pass

        if not ppom:
            try:
                ppom = get_parent_pom(parent)
            except XMvnResolveException:
                break

        parent = ppom.parent
        pom_props = get_model_variables(ppom)
        pdeps, pdepm, pprops = _get_dependencies(ppom)
        expand_props(pdeps, pom_props)
        expand_props(pdepm, pom_props)

        # merge "dependencies" sections
        merge_sections(deps, pdeps)
        # merge "dependencyManagement" sections
        merge_sections(depm, pdepm)

        # merge "properties" sections
        for pkey in pprops:
            if pkey not in props:
                props[pkey] = pprops[pkey]

        curr_pom = ppom

    for d in deps:
        d.interpolate(props)

    for dm in depm:
        dm.interpolate(props)

    # apply dependencyManagement on deps
    for d in deps:
        for dm in depm:
            if d.compare_to(dm):
                d.merge_with(dm)
                break

    # only deps with scope "compile" or "runtime" are interesting
    deps = [x for x in deps if x.scope in ["", "compile", "runtime"]]

    return deps


def _get_dependencies(pom):
    deps = []
    depm = []
    props = {}

    deps.extend([x for x in pom.dependencies])
    depm.extend([x for x in pom.dependencyManagement])
    props = pom.properties

    return deps, depm, props


def _main():
    OptionParser.format_epilog = lambda self, formatter: self.epilog
    parser = OptionParser(usage=usage,
                        epilog=epilog)

    sys.argv = args_to_unicode(sys.argv)

    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("2 argument2 are required")

    if not os.path.exists(args[0]):
        message = ("The first argument '{0}' doesn't point to an existing file ").format(args[0])
        parser.error(message)

    if not os.path.exists(os.path.dirname(os.path.abspath(args[1]))):
        message = ("The path '{0}' doesn't exist ").format(os.path.dirname(args[1]))
        parser.error(message)

    if not os.path.isdir(os.path.dirname(os.path.abspath(args[1]))):
        message = ("The path '{0}' is not a directory ").format(os.path.dirname(args[1]))
        parser.error(message)

    if os.path.exists(args[1]):
        message = ("The path '{0}' exists. Refusing to overwrite ").format(args[1])
        parser.error(message)
    
    pom_path = args[0]
    uart = POM(pom_path)

    tree = None
    if uart.packaging and uart.packaging.lower() == 'pom':
        tree = ElementTree.parse(args[0])
    else:
        result_pom = "<?xml version='1.0' encoding='UTF-8'?>\n"
        result_pom += "<project xmlns=\"http://maven.apache.org/POM/4.0.0\">\n"
        result_pom += "  <modelVersion>4.0.0</modelVersion>\n"
        result_pom += ("  <groupId>{0}</groupId>\n" ).format(uart.groupId)
        result_pom += ("  <artifactId>{0}</artifactId>\n" ).format(uart.artifactId)
        result_pom += ("  <version>{0}</version>\n").format(uart.version)

        if hasattr(uart, "packaging") and uart.packaging and uart.packaging != 'jar':
            result_pom += ("  <packaging>{0}</packaging>\n").format(uart.extension)
        if hasattr(uart, "extension") and uart.extension and uart.extension != 'jar':
            result_pom += ("  <extension>{0}</extension>\n").format(uart.extension)
        if hasattr(uart, "classifier") and uart.classifier:
            result_pom += ("  <classifier>{0}</classifier>\n").format(uart.classifier)

        jar_path = None

        mvn_deps = gather_dependencies(pom_path)
        if mvn_deps:
            result_pom += "  <dependencies>\n"
            for d in mvn_deps:
                result_pom += "    <dependency>\n"
                result_pom += ("      <groupId>{0}</groupId>\n").format(d.groupId)
                result_pom += ("      <artifactId>{0}</artifactId>\n" ).format(d.artifactId)
                result_pom += ("      <version>{0}</version>\n" ).format(d.version)
                if hasattr(d, "extension") and d.extension and d.extension != 'jar':
                    result_pom += ("      <extension>{0}</extension>\n").format(d.extension)
                if hasattr(d, "classifier") and d.classifier:
                    result_pom += ("      <classifier>{0}</classifier>\n").format(d.classifier)
                if hasattr(d, "optional") and d.optional and d.optional.lower() == "true":
                    result_pom += ("      <optional>{0}</optional>\n").format(d.optional.lower())
                result_pom += "    </dependency>\n"
            result_pom += "  </dependencies>\n"

        result_pom += "</project>\n"
        tree = ElementTree.ElementTree(ElementTree.XML(result_pom))
    tree.write(args[1],encoding="UTF-8",xml_declaration=True,default_namespace="http://maven.apache.org/POM/4.0.0")
    os.chmod(args[1], 0o0644)

if __name__ == "__main__":
    try:
        _main()
    except JavaPackagesToolsException as e:
        sys.exit(e)
