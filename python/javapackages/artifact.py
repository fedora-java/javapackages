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

import re
import sys

import pyxb
from lxml.etree import Element, SubElement, tostring

from javapackages.pom import POM
import javapackages.metadata as m

class ArtifactException(Exception):
    pass

class ArtifactFormatException(ArtifactException):
    pass

class ArtifactValidationException(ArtifactException):
    pass

class ProvidedArtifact(object):
    def __init__(self, groupId, artifactId, extension="",
                 classifier="", version="", namespace="",
                 path="", aliases=None, compatVersions=None,
                 properties=None, dependencies=None):


        self.artifact = Artifact(groupId, artifactId, extension,
                                 classifier, version, namespace)
        self.compatVersions = compatVersions or set()
        self.aliases = aliases or set()
        self.properties = properties or {}
        self.path = path
        self.dependencies = dependencies or set()

    def is_compat(self):
        """Return true if artifact has compat verions specified.
        This means package should have versioned provides for this artifact"""

        return self.compatVersions

    def __getattr__(self, attrib):
        return getattr(self.artifact, attrib)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.artifact.__hash__() + \
               self.compatVersions.__hash__() + \
               self.aliases.__hash__() + \
               self.properties.__hash__() + \
               self.path.__hash__()

    def __unicode__(self):
        return self.artifact.__unicode__()

    def __str__(self):
        return self.artifact.__str__()

    def get_rpm_str(self, version=None):
        """Return representation of artifact as used in RPM dependencies

        Example outputs:
        mvn(commons-logging:commons-logging) = 2.0

        Versioned:
        mvn(commons-logging:commons-logging:war:1.0) = 1.2
        mvn(commons-logging:commons-logging:war:1.2) = 1.2
        """

        strlist = []
        if not self.compatVersions:
            strlist.append(self.artifact.get_rpm_str())
        else:
            for ver in self.compatVersions:
                rpmstr = self.artifact.get_rpm_str(ver)
                strlist.append(rpmstr)

        if not (self.version):
            raise ArtifactFormatException(
                "Cannot create versioned string from artifact without version: {art}".format(art=str(self)))

        for alias in self.aliases:
            full_alias = Artifact.merge_artifacts(alias.artifact, self.artifact)
            strlist.append(full_alias.get_rpm_str())

        result = ""
        for rpmstr in strlist:
            if result:
                result += "\n"
            result += "{rpmstr} = {version}".format(rpmstr=rpmstr, version=self.version)

        return result

    def to_metadata(self):
        # TODO: add support for properties(?)
        a = m.ArtifactMetadata()
        a.groupId = self.groupId
        a.artifactId = self.artifactId
        a.version = self.version
        a.classifier = self.classifier or None
        a.extension = self.extension or None
        a.namespace = self.namespace or None
        a.path = self.path or None
        if self.dependencies:
            deps = [d.to_metadata() for d in self.dependencies]
            a.dependencies = pyxb.BIND(*deps)
        if self.compatVersions:
            a.compatVersions = pyxb.BIND(*self.compatVersions)

        if self.aliases:
            als = [alias.to_metadata() for alias in self.aliases]
            a.aliases = pyxb.BIND(*als)

        return a

    @classmethod
    def from_metadata(cls, metadata):
        groupId = metadata.groupId.strip()
        artifactId = metadata.artifactId.strip()
        version = extension = classifier = namespace = path =  ""
        if hasattr(metadata, 'path') and metadata.path:
            path = metadata.path.strip()
        if hasattr(metadata, 'version') and metadata.version:
            version = metadata.version.strip()
        if hasattr(metadata, 'extension') and metadata.extension:
            extension = metadata.extension.strip()
        if hasattr(metadata, 'classifier') and metadata.classifier:
            classifier = metadata.classifier.strip()
        if hasattr(metadata, 'namespace') and metadata.namespace:
            namespace = metadata.namespace.strip()

        compatVersions = set()
        if hasattr(metadata, 'compatVersions') and metadata.compatVersions:
            compatVersions = {cv for cv in metadata.compatVersions.version}

        aliases = set()
        if hasattr(metadata, 'aliases') and metadata.aliases:
            for alias in metadata.aliases.alias:
                alias_extension = alias_classifier = ""
                if hasattr(alias, 'extension') and alias.extension:
                    alias_extension = alias.extension

                if hasattr(alias, 'classifier') and alias.classifier:
                    alias_classifier = alias.classifier

                aliases.add(Alias(alias.groupId,
                                     alias.artifactId,
                                     alias_extension,
                                     alias_classifier))
        properties = {}
        if hasattr(metadata, 'properties') and metadata.properties:
            properties = {prop.tagName:prop.firstChild.value
                          for prop in metadata.properties.wildcardElements()}

        dependencies = set()
        if hasattr(metadata, 'dependencies') and metadata.dependencies:
            dependencies = {Dependency.from_metadata(dep)
                            for dep in metadata.dependencies.dependency}

        return cls(groupId, artifactId, extension, classifier, version,
                   namespace, path=path, aliases=aliases,
                   compatVersions=compatVersions, properties=properties,
                   dependencies=dependencies)

    @classmethod
    def from_pom(cls, pom_path):
        pom = POM(pom_path)

        return cls(pom.groupId, pom.artifactId, version=pom.version,
                   path=pom_path, dependencies=pom.get_dependencies())

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, version=a.version,
                   extension=a.extension, classifier=a.classifier)

class Artifact(object):
    """
    Simplified representation of Maven artifact for purpose of packaging

    Package consists mostly of simple properties and string formatting and
    loading functions to prevent code duplication elsewhere
    """

    def __init__(self, groupId, artifactId, extension="",
                 classifier="", version="", namespace=""):
        self.groupId = groupId.strip()
        self.artifactId = artifactId.strip()
        self.extension = extension.strip()
        self.classifier = classifier.strip()
        self.version = version.strip()
        self.namespace = namespace.strip()

    def __unicode__(self):
        return u"{gid}:{aid}:{ext}:{cls}:{ver}".format(gid=self.groupId,
                                                       aid=self.artifactId,
                                                       ext=self.extension,
                                                       cls=self.classifier,
                                                       ver=self.version)

    def __str__(self):
        return unicode(self).encode(sys.getfilesystemencoding())

    def get_mvn_str(self, version=None):
        mvnstr = "{gid}:{aid}".format(gid=self.groupId,
                                      aid=self.artifactId)

        if self.extension:
            mvnstr = mvnstr + ":{ext}".format(ext=self.extension)

        if self.classifier:
            if not self.extension:
                mvnstr = mvnstr + ":"
            mvnstr = mvnstr + ":{clas}".format(clas=self.classifier)

        if version:
            mvnstr = mvnstr + ":{ver}".format(ver=version)
        elif self.classifier or self.extension:
            mvnstr = mvnstr + ":"

        return mvnstr

    def get_rpm_str(self, version=None):
        """Return representation of artifact as used in RPM dependencies

        Example outputs:
        mvn(commons-logging:commons-logging)
        mvn(commons-logging:commons-logging:1.2) # versioned
        mvn(commons-logging:commons-logging:war:)
        mvn(commons-logging:commons-logging:war:1.2) # versioned
        mvn(commons-logging:commons-logging:war:test-jar:)
        mvn(commons-logging:commons-logging:war:test-jar:1.2) # versioned
        maven31-mvn(commons-logging:commons-logging)
        """
        namespace = "mvn"
        if self.namespace:
            namespace = self.namespace + "-mvn"

        mvnstr = self.get_mvn_str(version)

        return "{namespace}({mvnstr})".format(namespace=namespace,
                                              mvnstr=mvnstr)

    def get_xml_element(self, root="artifact"):
        """
        Return XML Element node representation of the Artifact
        """
        root = Element(root)

        for key in ("artifactId", "groupId", "extension", "version",
                    "classifier", "namespace"):
            if hasattr(self, key) and getattr(self,key):
                item = SubElement(root, key)
                item.text = getattr(self, key)
        return root

    def get_xml_str(self, root="artifact"):
        """
        Return XML formatted string representation of the Artifact
        """
        root = self.get_xml_element(root)
        return tostring(root, pretty_print=True)

    def validate(self, allow_empty=True, allow_wildcards=True, allow_backref=True):
        """
        Function to validate current state of artifact with regards to
        wildcards, empty parts and backreference usage
        """
        all_empty = True
        wildcard_used = False
        backref_used = False
        backref_re = re.compile(r'@\d+')
        for key in ("artifactId", "groupId", "extension", "version",
                    "classifier", "namespace"):
            val = getattr(self, key)
            if not val:
                continue
            if val:
                all_empty = False
            if val.find('*') != -1:
                wildcard_used = True
            if backref_re.match(val):
                backref_used = True

        if not allow_empty and all_empty:
            raise ArtifactValidationException("All parts of artifact are empty")
        if not allow_wildcards and wildcard_used:
            raise ArtifactValidationException("Wildcard used in artifact")
        if not allow_backref and backref_used:
            raise ArtifactValidationException("Backreference used in artifact")
        return True

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.groupId.__hash__() + \
               self.artifactId.__hash__() + \
               self.version.__hash__() + \
               self.extension.__hash__() + \
               self.classifier.__hash__() + \
               self.namespace.__hash__()


    @classmethod
    def merge_artifacts(cls, dominant, recessive):
        """
        Merge two artifacts into one. Information missing in dominant artifact will
        be copied from recessive artifact. Returns new merged artifact
        """
        ret = cls(dominant.groupId, dominant.artifactId, dominant.extension,
                  dominant.classifier, dominant.version, dominant.namespace)
        for key in ("artifactId", "groupId", "extension", "version",
                    "classifier", "namespace"):
            if not getattr(ret, key):
                setattr(ret, key, getattr(recessive, key))
        return ret

    @classmethod
    def from_xml_element(cls, xmlnode, namespace=""):
        """
        Create Artifact from xml.etree.ElementTree.Element as contained
        within pom.xml or a dependency map.
        """

        # TODO: find better way of handling pom/ivy/xyz differences
        parts = {'groupId':'',
                 'artifactId':'',
                 'extension':'',
                 'classifier':'',
                 'version':''}

        ivyparts = {'org': '',
                    'name': '',
                    'revision': ''}

        for key in parts:
            node = xmlnode.find("./{*}" + key)
            if node is not None and node.text is not None:
                parts[key] = node.text.strip()

        if hasattr(xmlnode, "attrib"):
            attribs = xmlnode.attrib
            for key in ivyparts:
                try:
                    ivyparts[key] = attribs[key]
                except KeyError:
                    pass

            parts['groupId'] = parts['groupId'] or ivyparts['org']
            parts['artifactId'] = parts['artifactId'] or ivyparts['name']
            parts['version'] = parts['version'] or ivyparts['revision']

        if not parts['groupId'] or not parts['artifactId']:
            raise ArtifactFormatException(
                "Empty groupId or artifactId encountered. "
                "This is a bug, please report it!")


        if not namespace:
            namespace = xmlnode.find('./namespace')
            if namespace is not None:
                namespace = namespace.text.strip()
            else:
                namespace = ""

        return cls(parts['groupId'], parts['artifactId'], parts['extension'],
                   parts['classifier'], parts['version'], namespace)

    @classmethod
    def from_mvn_str(cls, mvnstr, namespace=""):
        """
        Create Artifact from Maven-style definition

        The string should be in the format of:
           groupId:artifactId[:extension[:classifier]][:version]

        Where last part is always considered to be version unless empty
        """
        tup = mvnstr.split(":")

        # groupId and artifactId are always present
        if len(tup) < 2:
            raise ArtifactFormatException("Artifact string '{mvnstr}' does not "
                                          "contain ':' character. Can not parse"
                                          .format(mvnstr=mvnstr))

        if len(tup) > 5:
            raise ArtifactFormatException("Artifact string '{mvnstr}' contains "
                                          "too many colons. Can not parse"
                                          .format(mvnstr=mvnstr))

        groupId = tup[0]
        artifactId = tup[1]
        extension = tup[2] if len(tup) >= 4 else ""
        classifier = tup[3] if len(tup) >= 5 else ""
        version = tup[-1] if len(tup) >= 3 else ""

        return cls(groupId, artifactId, extension,
                   classifier, version, namespace)

    @classmethod
    def from_metadata(cls, metadata):
        groupId = metadata.groupId.strip()
        artifactId = metadata.artifactId.strip()

        version = extension = classifier = namespace = ""
        if hasattr(metadata, 'version') and metadata.version:
            version = metadata.version.strip()
        if hasattr(metadata, 'extension') and metadata.extension:
            extension = metadata.extension.strip()
        if hasattr(metadata, 'classifier') and metadata.classifier:
            classifier = metadata.classifier.strip()
        if hasattr(metadata, 'namespace') and metadata.namespace:
            namespace = metadata.namespace.strip()

        return cls(groupId, artifactId, extension, classifier,
                   version, namespace)

class SkippedArtifact(Artifact):
    pass

class ExclusionArtifact(Artifact):
    pass


class Dependency(object):

    def __init__(self, groupId, artifactId, requestedVersion,
                 resolvedVersion="", extension="", classifier="",
                 namespace="", exclusions=None):
        self.artifact = Artifact(groupId,
                                 artifactId,
                                 extension=extension,
                                 classifier=classifier,
                                 version=requestedVersion,
                                 namespace=namespace)
        self.resolvedVersion = resolvedVersion
        self.exclusions = exclusions or set()

    def __getattr__(self, attrib):
        return getattr(self.artifact, attrib)

    def get_requestedVersion(self):
        return self.artifact.version
    def set_requestedVersion(self, version):
        self.artifact.version = version
    requestedVersion = property(get_requestedVersion, set_requestedVersion)

    def get_rpm_str(self, version=None):
        """Return representation of artifact as used in RPM dependencies"""
        return self.artifact.get_rpm_str(self.resolvedVersion)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.artifact.__hash__() + \
               self.resolvedVersion.__hash__()

    def __unicode__(self):
        return self.artifact.__unicode__()

    def __str__(self):
        return self.artifact.__str__()

    def to_metadata(self):
        d = m.Dependency()
        d.groupId = self.groupId
        d.artifactId = self.artifactId
        d.requestedVersion = self.version
        d.classifier = self.classifier or None
        d.extension = self.extension or None
        if self.exclusions:
            excl = {m.DependencyExclusion(e.groupId, e.artifactId)
                    for e in self.exclusions}
            d.exclusions = pyxb.BIND(*excl)
        return d

    @classmethod
    def from_metadata(cls, metadata):
        groupId = metadata.groupId.strip()
        artifactId = metadata.artifactId.strip()
        requestedVersion = metadata.requestedVersion.strip()

        resolvedVersion = extension = classifier = namespace = ""
        if hasattr(metadata, 'resolvedVersion') and metadata.resolvedVersion:
            resolvedVersion = metadata.resolvedVersion.strip()
        if hasattr(metadata, 'extension') and metadata.extension:
            extension = metadata.extension.strip()
        if hasattr(metadata, 'classifier') and metadata.classifier:
            classifier = metadata.classifier.strip()
        if hasattr(metadata, 'namespace') and metadata.namespace:
            namespace = metadata.namespace.strip()

        exclusions = set()
        if hasattr(metadata, 'exclusions') and metadata.exclusions:
            exclusions = {ExclusionArtifact.from_metadata(excl)
                          for excl in metadata.exclusions.exclusion}

        return cls(groupId, artifactId, requestedVersion, resolvedVersion,
                   extension, classifier, namespace, exclusions)

    @classmethod
    def from_xml_element(cls, xmlnode, namespace="", create_all=False):
        """
        Create Dependency from xml.etree.ElementTree.Element as contained
        within pom.xml
        """
        a = Artifact.from_xml_element(xmlnode)

        # ivy specifies version as "rev" in case of dependencies:
        if xmlnode.attrib:
            rev = xmlnode.attrib.get("rev")
            if rev:
                a.version = rev

        scope = xmlnode.find('./{*}scope')
        # by default don't create test, provided and other non-essential elements
        if (not create_all and
            scope is not None and
            scope.text not in ["compile", "runtime"]):
            return None
        exclusions = set()
        exclxml = xmlnode.find('./{*}exclusions')
        if exclxml is not None:
            for excl in exclxml:
                gid = excl.find('./{*}groupId').text
                aid = excl.find('./{*}artifactId').text
                e = m.DependencyExclusion(gid, aid)
                exclusions.add(e)


        return cls(a.groupId, a.artifactId,
                   requestedVersion=a.version, extension=a.extension,
                   classifier=a.classifier, namespace=namespace,
                   exclusions=exclusions)

    @classmethod
    def merge_dependencies(cls, dominant, recessive):
        """
        Merge two dependencies into one. Information missing in dominant dependency will
        be copied from recessive dependency. Returns new merged dependency.
        """
        ret = cls(dominant.groupId, dominant.artifactId, dominant.extension,
                  dominant.classifier, dominant.version, dominant.namespace)
        for key in ("artifactId", "groupId", "extension", "version",
                    "classifier", "namespace"):
            if not getattr(ret, key):
                setattr(ret, key, getattr(recessive, key))
        return ret


class Alias(object):
    def __init__(self, groupId, artifactId, extension="", classifier=""):

        self.artifact = Artifact(groupId, artifactId, extension, classifier)

    def to_metadata(self):
        a = m.ArtifactAlias()
        a.groupId = self.artifact.groupId
        a.artifactId = self.artifact.artifactId
        a.classifier = self.artifact.classifier or None
        a.extension = self.artifact.extension or None

        return a

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, a.extension, a.classifier)
