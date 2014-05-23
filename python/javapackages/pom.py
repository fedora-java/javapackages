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
# Authors:  Stanislav Ochotnicky <sochotnicky@redhat.com>

from lxml.etree import ElementTree, XMLParser

class PomLoadingException(Exception):
    pass

class POM(object):
    """
    Class for querying basic information from pom.xml files used by Apache Maven
    """
    def __init__(self, path):
        et = ElementTree ()
        parser = XMLParser(remove_comments=True,
                           strip_cdata=True)
        try:
            self.__doc = et.parse(path, parser=parser)
        except IOError:
            raise PomLoadingException("Cannot read file {0}".format(path))

        if self.__doc is None:
            raise PomLoadingException("Failed to load pom.xml. You have a problem")


    def __find(self, xpath):
        ret = self.__findall(xpath)
        if len(ret) > 0:
            ret = ret[0]
        else:
            ret = None

        return ret

    def __findall(self, xpath):
        ret = self.__doc.xpath(xpath, namespaces=dict(pom='http://maven.apache.org/POM/4.0.0'))
        # perhaps there is no namespace?
        if len(ret) == 0:
            ret = self.__doc.xpath(xpath.replace('pom:', ''))
        return ret

    def __str__(self):
        return ":".join([self.groupId, self.artifactId, self.version])


    @property
    def parentArtifactId(self):
        """
        artifactId of the parent artifact of None
        """
        aId = self.__find('./pom:parent/pom:artifactId')
        if aId is None:
            return None
        else:
            return aId.text.strip()

    @property
    def parentGroupId(self):
        """
        groupId of the parent artifact of None
        """
        gId = self.__find('./pom:parent/pom:groupId')
        if gId is None:
            return None
        else:
            return gId.text.strip()

    @property
    def groupId(self):
        """
        Effective groupId of the pom Artifact taking into account parent groupId
        """
        gId = self.__find('./pom:groupId')
        if gId is None:
            gId = self.__find('./pom:parent/pom:groupId')
        if gId is None:
            gId = self.__find('/ivy-module/info')
            if gId is not None:
                gId = gId.attrib["organisation"]
            if gId is not None:
                return gId
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
        aId = self.__find('./pom:artifactId')
        if aId is None:
            aId = self.__find('/ivy-module/info')
            if aId is not None:
                aId = aId.attrib["module"]
            if aId is not None:
                return aId
        if aId is None:
            raise PomLoadingException("Unable to determine artifactID")
        if len(aId) != 0:
            raise PomLoadingException("Unexpected child nodes under artifactId")
        return aId.text.strip()

    @property
    def version(self):
        """
        Effective version of the pom Artifact taking into account parent
        version
        """
        version = self.__find('./pom:version')
        if version is None:
            version = self.__find('./pom:parent/pom:version')
        if version is None:
            version = self.__find('/ivy-module/info')
            if version is not None:
                version = version.attrib["revision"]
            if version is not None:
                return version
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
        p = self.__find('./pom:packaging')
        if p is not None:
            if len(p) != 0:
                raise PomLoadingException("Unexpected child nodes under packaging")
            return p.text.strip()
        p = self.__find('/ivy-module/info')
        if p is not None:
            return 'ivy'
        return None

    def get_dependencies(self, get_all=False):
        # TODO: circular imports between artifact and pom (?)
        from javapackages.artifact import Dependency
        ret = set()

        dependencies = self.__findall('./pom:dependencies/pom:dependency')
        if dependencies:
            if hasattr(dependencies[0], "attrib") and dependencies[0].attrib:
                # this is probably ivy file, we currently don't really support
                # reading dependencies from ivy files - returning empty set
                return ret
            for dep in dependencies:
                adep = Dependency.from_xml_element(dep, create_all=get_all)
                if not adep:
                    continue
                ret.add(adep)
        return ret

    def get_dependency_management(self):
        result = set()

        # TODO: circular imports between artifact and pom (?)
        from javapackages.artifact import Dependency

        deps = self.__findall('./pom:dependencyManagement/pom:dependency')
        if deps:
            for dep in deps:
                adep = Dependency.from_xml_element(dep, create_all=False)
                if not adep:
                    continue
                result.add(adep)
        return result

    def get_plugins(self):
        result = set()

        plugs = self.__findall('./pom:build/pom:plugins/pom:plugin')
        if plugs:
            for p in plugs:
                plug = MavenPlugin.from_xml_element(p)
                if not plug:
                    continue
                result.add(plug)
        return result

    def get_extensions(self):
        result = set()

        extensions = self.__findall('./pom:build/pom:extensions/pom:extension')
        if extensions:
            for e in extensions:
                ext = MavenExtension.from_xml_element(e)
                if not ext:
                    continue
                result.add(ext)
        return result


class MavenPlugin(object):
    def __init__(self, groupId, artifactId, version="", dependencies=set()):
        self.groupId = groupId or "org.apache.maven.plugins"
        self.artifactId = artifactId
        self.version = version
        self.dependencies = dependencies
        # TODO: <extensions/>?

    @classmethod
    def from_xml_element(cls, xmlnode):
        """
        Create Dependency from xml.etree.ElementTree.Element as contained
        within pom.xml
        """
        parts = {'groupId': '',
                 'artifactId': '',
                 'version': ''}

        for key in parts:
            node = xmlnode.find("./{*}" + key)
            if node is not None and node.text is not None:
                parts[key] = node.text.strip()

        dependencies = set()
        deps = xmlnode.find('./{*}dependencies')
        if deps is not None:
            for depxml in deps:
                # TODO: circular imports between artifact and pom (?)
                from javapackages.artifact import Dependency
                dep = Dependency.from_xml_element(depxml, create_all=True)
                dependencies.add(dep)

        return cls(parts['groupId'], parts['artifactId'], parts['version'], dependencies)


class MavenExtension(object):
    def __init__(self, groupId, artifactId, version=""):
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version

    @classmethod
    def from_xml_element(cls, xmlnode):
        """
        Create Dependency from xml.etree.ElementTree.Element as contained
        within pom.xml
        """
        parts = {'groupId': '',
                 'artifactId': '',
                 'version': ''}

        for key in parts:
            node = xmlnode.find("./{*}" + key)
            if node is not None and node.text is not None:
                parts[key] = node.text.strip()

        return cls(parts['groupId'], parts['artifactId'], parts['version'])
