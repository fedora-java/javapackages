#
# Copyright (c) 2015, Red Hat, Inc.
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
# Authors:  Stanislav Ochotnicky <sochotnicky@redhat.com>
#           Michal Srb <msrb@redhat.com>

from javapackages.maven.pomreader import POMReader, PomLoadingException
from javapackages.maven.dependency import Dependency
from javapackages.maven.plugin import Plugin
from javapackages.maven.extension import Extension

import os


class POM(object):
    """
    Class for querying basic information from pom.xml files
    """
    def __init__(self, path):
        if not path:
            raise PomLoadingException("Path \"{p}\" is invalid".format(p=path))
        self._doc = POMReader.load(path)
        self._path = os.path.join(path)

    def __str__(self):
        return ":".join([self.groupId, self.artifactId, self.version])

    def has_parent(self):
        parent = POMReader.find(self._doc, "./pom:parent")
        if parent is not None:
            return True
        return False

    @property
    def parent(self):
        aId = POMReader.find(self._doc, "./pom:parent/pom:artifactId")
        if aId is None:
            return None
        artifactId = aId.text

        groupId = ""
        gId = POMReader.find(self._doc, "./pom:parent/pom:groupId")
        if gId is not None:
            groupId = gId.text

        version = ""
        ver = POMReader.find(self._doc, "./pom:parent/pom:version")
        if ver is not None:
            version = ver.text

        relativePath = ""
        relPath = POMReader.find(self._doc, "./pom:parent/pom:relativePath")
        if relPath is not None:
            relativePath = relPath.text

        return ParentPOM(groupId, artifactId, version, relativePath)

    @property
    def groupId(self):
        """
        Effective groupId of the pom artifact taking into account parent groupId
        """
        gId = POMReader.find(self._doc, "./pom:groupId")
        if gId is None:
            gId = POMReader.find(self._doc, "./pom:parent/pom:groupId")
        if gId is None:
            raise PomLoadingException("Unable to determine groupId")
        return gId.text.strip()

    @property
    def artifactId(self):
        """
        Effective artifactId of the pom artifact
        """
        aId = POMReader.find(self._doc, "./pom:artifactId")
        if aId is None:
            raise PomLoadingException("Unable to determine artifactId")
        return aId.text.strip()

    @property
    def version(self):
        """
        Effective version of the pom artifact taking into account parent
        version
        """
        version = POMReader.find(self._doc, "./pom:version")
        if version is None:
            version = POMReader.find(self._doc, "./pom:parent/pom:version")
        if version is None:
            raise PomLoadingException("Unable to determine artifact version")
        return version.text.strip()

    @property
    def packaging(self):
        """
        Packaging type of artifact or "jar" if unspecified
        """
        packaging = POMReader.find(self._doc, "./pom:packaging")
        if packaging is None:
            # use default packaging type
            return "jar"
        return packaging.text.strip()

    @property
    def dependencies(self):
        """
        List of dependencies
        """
        xmlnodes = POMReader.xpath(self._doc,
                                   "./pom:dependencies/pom:dependency")
        return [Dependency.from_xml_element(x) for x in xmlnodes]

    @property
    def dependencyManagement(self):
        """
        List of dependencies from dependency management section
        """
        xmlnodes = POMReader.xpath(self._doc,
                                   "./pom:dependencyManagement"
                                   "/pom:dependencies/pom:dependency")
        return [Dependency.from_xml_element(x) for x in xmlnodes]

    @property
    def pluginManagement(self):
        """
        List of plugins from plugin management section
        """
        xmlnodes = POMReader.xpath(self._doc,
                                   "./pom:pluginManagement"
                                   "/pom:plugins/pom:plugin")
        return [Plugin.from_xml_element(x) for x in xmlnodes]

    @property
    def plugins(self):
        """
        List of plugins
        """
        xmlnodes = POMReader.xpath(self._doc,
                                   "./pom:build/pom:plugins/pom:plugin")
        return [Plugin.from_xml_element(x) for x in xmlnodes]

    @property
    def extensions(self):
        """
        List of extensions
        """
        xmlnodes = POMReader.xpath(self._doc,
                                   "./pom:build/pom:extensions/pom:extension")
        return [Extension.from_xml_element(x) for x in xmlnodes]

    @property
    def properties(self):
        """
        Dictionary consisting of properties specified in pom.xml
        """
        properties = {}
        xmlnodes = POMReader.find(self._doc, "./pom:properties")
        if xmlnodes is None:
            return properties
        propnodes = xmlnodes.getchildren()
        for node in propnodes:
            if node.tag.startswith('{'):
                tag = node.tag[node.tag.find('}') + 1:]
            else:
                tag = node.tag
            properties[tag] = node.text

        return properties


class ParentPOM(object):
    def __init__(self, groupId, artifactId, version="", relativePath=""):
        self.groupId = ""
        self.artifactId = ""

        if groupId is not None:
            self.groupId = groupId.strip()
        if artifactId is not None:
            self.artifactId = artifactId.strip()
        if version is not None:
            self.version = version.strip()
        if relativePath is not None:
            self.relativePath = relativePath.strip()
