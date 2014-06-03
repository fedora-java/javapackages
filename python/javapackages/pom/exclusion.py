import sys

from artifact import AbstractArtifact, ArtifactFormatException
from pomreader import POMReader
from lxml.etree import Element, SubElement, tostring


class Exclusion(AbstractArtifact):

    def __init__(self, groupId, artifactId):
        self.groupId = groupId.strip()
        self.artifactId = artifactId.strip()

    def __unicode__(self):
        return u"{gid}:{aid}".format(gid=self.groupId, aid=self.artifactId)

    def __str__(self):
        return unicode(self).encode(sys.getfilesystemencoding())

    def get_xml_element(self, root="exclusion"):
        """
        Return XML Element node representation of the Exclusion
        """
        return AbstractArtifact.get_xml_element(self, root)

    def get_xml_str(self, root="exclusion"):
        """
        Return XML formatted string representation of the Exclusion
        """
        return AbstractArtifact.get_xml_str(self, root)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.groupId.__hash__() + \
               self.artifactId.__hash__()

    @classmethod
    def from_xml_element(cls, xmlnode):
        """
        Create Exclusion from xml.etree.ElementTree.Element as contained
        within pom.xml.
        """

        parts = {'groupId': '', 'artifactId': ''}
        parts = POMReader.find_parts(xmlnode, parts)

        if not parts['groupId'] or not parts['artifactId']:
            raise ArtifactFormatException(
                "Empty groupId or artifactId encountered. "
                "This is a bug, please report it!")

        return cls(parts['groupId'], parts['artifactId'])

    @classmethod
    def from_mvn_str(cls, mvnstr):
        """
        Create Exclusion from Maven-style definition

        The string should be in the format of:
           groupId:artifactId
        """
        p = cls.get_parts_from_mvn_str(mvnstr)
        return cls(p['groupId'], p['artifactId'])
