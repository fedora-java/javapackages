#!/usr/bin/python
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

import sys

from pomreader import POMReader
from printer import Printer
from lxml.etree import Element, SubElement, tostring


class ArtifactException(Exception):
    pass


class ArtifactFormatException(Exception):
    pass


class AbstractArtifact(object):

    def get_mvn_str(self):
        m = self.__get_members()
        return Printer.get_mvn_str(m['groupId'], m['artifactId'],
                                   m['extension'], m['classifier'],
                                   m['version'])

    def get_rpm_str(self, namespace="", compat=False, pkgver=None):
        m = self.__get_members()
        return Printer.get_rpm_str(m['groupId'], m['artifactId'],
                                   m['extension'], m['classifier'],
                                   m['version'], namespace=namespace,
                                   compat=compat, pkgver=pkgver)

    @staticmethod
    def get_parts_from_mvn_str(mvnstr):
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

        parts = {'groupId': '',
                 'artifactId': '',
                 'extension': '',
                 'classifier': '',
                 'version': ''}

        parts['groupId'] = tup[0]
        parts['artifactId'] = tup[1]
        parts['extension'] = tup[2] if len(tup) >= 4 else ""
        parts['classifier'] = tup[3] if len(tup) >= 5 else ""
        parts['version'] = tup[-1] if len(tup) >= 3 else ""

        return parts

    def get_xml_element(self, root_element_name=None):
        """
        Return XML Element node representation of the Artifact
        """
        if root_element_name is None:
            clsname = self.__class__.__name__
            root_element_name = clsname[0].lower() + clsname[1:]
        root = Element(root_element_name)

        members = self.__get_members()

        for key in members:
            if members[key]:
                item = SubElement(root, key)
                item.text = members[key]
        return root

    def get_xml_str(self, root_element_name=None):
        """
        Return XML formatted string representation of the Artifact
        """
        if root_element_name is None:
            clsname = self.__class__.__name__
            root_element_name = clsname[0].lower() + clsname[1:]

        root = self.get_xml_element(root_element_name)
        return tostring(root, pretty_print=True)

    def get_artifact(self, extension="", classifier="", version=""):
        m = self.__get_members()

        return Artifact(m['groupId'], m['artifactId'],
                        extension or m['extension'],
                        classifier or m['classifier'],
                        version or m['version'])

    def merge_with(self, artifact):
        if type(self) != type(artifact):
            raise Exception("Unable to merge artifacts of different types. "
                            "{this} cannot be merged with {other}"
                            .format(this=type(self), other=type(artifact)))

        for member in self.__dict__:
            if not member.startswith('_') and not getattr(self, member):
                setattr(self, member, getattr(artifact, member))
        return True

    def update_from(self, artifact):
        if self.compare_to(artifact):
            for member in self.__dict__:
                if not member.startswith('_') and not getattr(self, member):
                    setattr(self, member, getattr(artifact, member))
            return True
        return False

    def compare_to(self, artifact):
        if type(self) != type(artifact):
            return False
        this = self.__get_significant_members()
        other = artifact.__get_significant_members()
        try:
            del this['version']
            del other['version']
        except KeyError:
            pass

        if this == other:
            return True
        return False

    def __unicode__(self):
        return unicode(self.get_mvn_str())

    def __str__(self):
        return unicode(self).encode(sys.getfilesystemencoding())

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__get_significant_members() == other.__get_significant_members()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        result = 0
        for key in self.__get_significant_members():
            var = getattr(self, key)
            result += var.__hash__()
        return result

    def __get_significant_members(self, ignore_version=False):
        m = {}
        for mname in ["groupId", "artifactId", "extension", "classifier"]:
            if hasattr(self, mname):
                m[mname] = getattr(self, mname)
            if not ignore_version and hasattr(self, "version"):
                m["version"] = getattr(self, "version")
        return m

    def __get_members(self):
        m = {'groupId': '',
             'artifactId': '',
             'extension': '',
             'classifier': '',
             'version': ''}

        for key in m:
            if hasattr(self, key):
                m[key] = getattr(self, key)

        return m


class Artifact(AbstractArtifact):
    """
    Simplified representation of Maven artifact for purpose of packaging

    Package consists mostly of simple properties and string formatting and
    loading functions to prevent code duplication elsewhere
    """

    def __init__(self, groupId, artifactId, extension="",
                 classifier="", version=""):
        self.groupId = groupId.strip()
        self.artifactId = artifactId.strip()
        self.extension = extension.strip()
        self.classifier = classifier.strip()
        self.version = version.strip()

    @classmethod
    def merge_artifacts(cls, dominant, recessive):
        """
        Merge two artifacts into one. Information missing in dominant artifact will
        be copied from recessive artifact. Returns new merged artifact
        """
        ret = cls(dominant.groupId, dominant.artifactId, dominant.extension,
                  dominant.classifier, dominant.version)
        for key in ("artifactId", "groupId", "extension", "version",
                    "classifier"):
            if not getattr(ret, key):
                setattr(ret, key, getattr(recessive, key))
        return ret

    @classmethod
    def from_xml_element(cls, xmlnode):
        """
        Create Artifact from xml.etree.ElementTree.Element as contained
        within pom.xml or a dependency map.
        """

        parts = {'groupId':'',
                 'artifactId':'',
                 'extension':'',
                 'classifier':'',
                 'version':''}

        parts = POMReader.find_parts(xmlnode, parts)

        if not parts['groupId'] or not parts['artifactId']:
            raise ArtifactFormatException(
                "Empty groupId or artifactId encountered. "
                "This is a bug, please report it!")

        return cls(parts['groupId'], parts['artifactId'], parts['extension'],
                   parts['classifier'], parts['version'])

    @classmethod
    def from_mvn_str(cls, mvnstr):
        """
        Create Artifact from Maven-style definition

        The string should be in the format of:
           groupId:artifactId[:extension[:classifier]][:version]

        Where last part is always considered to be version unless empty
        """
        p = Artifact.get_parts_from_mvn_str(mvnstr)
        return cls(p['groupId'], p['artifactId'], p['extension'],
                   p['classifier'], p['version'])
