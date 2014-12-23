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
# Authors:  Stanislav Ochotnicky <sochotnicky@redhat.com>
#           Michal Srb <msrb@redhat.com>

from javapackages.maven.pomreader import POMReader, PomLoadingException
from javapackages.maven.dependency import Dependency
from javapackages.maven.plugin import Plugin
from javapackages.maven.extension import Extension

import os


class POM(object):
    """
    Class for querying basic information from pom.xml files used by Apache Maven
    """
    def __init__(self, path):
        self.__doc = POMReader.load(path)
        self._path = os.path.join(path)

    def __str__(self):
        return ":".join([self.groupId, self.artifactId, self.version])

    @property
    def parent(self):
        aId = POMReader.find(self.__doc, './pom:parent/pom:artifactId')
        if aId is None:
            return None
        aId = aId.text

        gId = POMReader.find(self.__doc, './pom:parent/pom:groupId')
        if gId is not None:
            gId = gId.text

        ver = POMReader.find(self.__doc, './pom:parent/pom:version')
        if ver is not None:
            ver = ver.text

        relativePath = POMReader.find(self.__doc, './pom:parent/pom:relativePath')
        if relativePath is not None:
            relativePath = relativePath.text

        return ParentPOM(gId, aId, ver, relativePath)

    @property
    def parentGroupId(self):
        """
        groupId of the parent artifact or None
        """
        gId = POMReader.find(self.__doc, './pom:parent/pom:groupId')
        if gId is None:
            return None
        return gId.text.strip()

    @property
    def parentArtifactId(self):
        """
        artifactId of the parent artifact or None
        """
        aId = POMReader.find(self.__doc, './pom:parent/pom:artifactId')
        if aId is None:
            return None
        return aId.text.strip()

    @property
    def parentVersion(self):
        """
        version of the parent artifact or None
        """
        ver = POMReader.find(self.__doc, './pom:parent/pom:version')
        if ver is None:
            return None
        return ver.text.strip()

    @property
    def groupId(self):
        """
        Effective groupId of the pom Artifact taking into account parent groupId
        """
        gId = POMReader.find(self.__doc, './pom:groupId')
        if gId is None:
            gId = POMReader.find(self.__doc, './pom:parent/pom:groupId')
        if gId is None:
            raise PomLoadingException("Unable to determine groupId")
        if len(gId) != 0:
            raise PomLoadingException("Unexpected child nodes under groupId")
        return gId.text.strip()

    @property
    def artifactId(self):
        """
        Effective artifactId of the pom Artifact
        """
        aId = POMReader.find(self.__doc, './pom:artifactId')
        if aId is None:
            raise PomLoadingException("Unable to determine artifactId")
        if len(aId) != 0:
            raise PomLoadingException("Unexpected child nodes under artifactId")
        return aId.text.strip()

    @property
    def version(self):
        """
        Effective version of the pom Artifact taking into account parent
        version
        """
        version = POMReader.find(self.__doc, './pom:version')
        if version is None:
            version = POMReader.find(self.__doc, './pom:parent/pom:version')
        if version is None:
            raise PomLoadingException("Unable to determine artifact version")
        if len(version) != 0:
            raise PomLoadingException("Unexpected child nodes under version")
        return version.text.strip()

    @property
    def packaging(self):
        """
        Packaging type of artifact or None if unspecified
        """
        packaging = POMReader.find(self.__doc, './pom:packaging')
        if packaging is None:
            # use default packaging type
            return "jar"
        if len(packaging) != 0:
            raise PomLoadingException("Unexpected child nodes under packaging")
        return packaging.text.strip()

    @property
    def dependencies(self):
        """
        List of artifact's dependencies
        """
        xmlnodes = POMReader.xpath(self.__doc, './pom:dependencies/pom:dependency')
        return [Dependency.from_xml_element(x) for x in xmlnodes]

    @property
    def dependencyManagement(self):
        """
        List of dependencies from dependency management section
        """
        xmlnodes = POMReader.xpath(self.__doc, './pom:dependencyManagement/pom:dependencies/pom:dependency')
        return [Dependency.from_xml_element(x) for x in xmlnodes]

    @property
    def pluginManagement(self):
        """
        List of plugins from plugin management section
        """
        xmlnodes = POMReader.xpath(self.__doc, './pom:pluginManagement/pom:plugins/pom:plugin')
        return [Plugin.from_xml_element(x) for x in xmlnodes]

    @property
    def plugins(self):
        """
        List of artifact's plugins
        """
        xmlnodes = POMReader.xpath(self.__doc, './pom:build/pom:plugins/pom:plugin')
        return [Plugin.from_xml_element(x) for x in xmlnodes]

    @property
    def extensions(self):
        """
        List of artifact's extensions
        """
        xmlnodes = POMReader.xpath(self.__doc, './pom:build/pom:extensions/pom:extension')
        return [Extension.from_xml_element(x) for x in xmlnodes]

    @property
    def properties(self):
        """
        Dictionary consisting of properties specified in pom.xml
        """
        properties = {}
        xmlnodes = POMReader.find(self.__doc, './pom:properties')
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
        self.groupId = groupId.strip()
        self.artifactId = artifactId.strip()
        self.version = version
        self.relativePath = relativePath
