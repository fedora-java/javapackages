import sys

from artifact import AbstractArtifact, ArtifactFormatException
from exclusion import Exclusion
from pomreader import POMReader
from lxml.etree import Element, SubElement, tostring


class Dependency(AbstractArtifact):

    def __init__(self, groupId, artifactId, extension="", classifier="",
                 version="", scope="", optional=False, exclusions=set()):
        self.groupId = groupId.strip()
        self.artifactId = artifactId.strip()
        self.extension = extension.strip()
        self.classifier = classifier.strip()
        self.version = version.strip()
        self.scope = scope.strip()
        self.optional = optional
        self.exclusions = exclusions

    def __unicode__(self):
        return u"{gid}:{aid}:{ext}:{cla}:{ver}".format(gid=self.groupId,
                                                       aid=self.artifactId,
                                                       ext=self.extension,
                                                       cla=self.classifier,
                                                       ver=self.version)

    def __str__(self):
        return unicode(self).encode(sys.getfilesystemencoding())

    def get_xml_element(self, root="dependency"):
        """
        Return XML Element node representation of the Artifact
        """
        root = AbstractArtifact.get_xml_element(self, root)

        if self.scope:
            item = SubElement(root, "scope")
            item.text = self.scope

        if self.optional:
            item = SubElement(root, "optional")
            item.text = str(self.optional).lower()

        exc_root = Element("exclusions")
        if self.exclusions:
            for e in self.exclusions:
                exc_root.insert(len(exc_root), e.get_xml_element())

        root.insert(len(root), exc_root)
        return root

    def get_xml_str(self, root="artifact"):
        """
        Return XML formatted string representation of the Artifact
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
               self.artifactId.__hash__() + \
               self.version.__hash__() + \
               self.extension.__hash__() + \
               self.classifier.__hash__()

    @classmethod
    def from_xml_element(cls, xmlnode):
        """
        Create Dependency from xml.etree.ElementTree.Element as contained
        within pom.xml.
        """

        parts = {'groupId': '',
                 'artifactId': '',
                 'extension': '',
                 'classifier': '',
                 'version': '',
                 'scope': '',
                 'optional': False}

        parts = POMReader.find_parts(xmlnode, parts)

        if not parts['groupId'] or not parts['artifactId']:
            raise ArtifactFormatException(
                "Empty groupId or artifactId encountered. "
                "This is a bug, please report it!")

        if parts['optional'] is not False:
            if parts['optional'] == "false":
                parts['optional'] = False
            elif parts['optional'] == "true":
                parts['optional'] = True

        # exclusions
        excnodes = POMReader.xpath(xmlnode, "./exclusions/exclusion")

        exclusions = set()
        for e in [Exclusion.from_xml_element(x) for x in excnodes]:
            exclusions.add(e)

        return cls(parts['groupId'], parts['artifactId'], parts['extension'],
                   parts['classifier'], parts['version'], parts['scope'],
                   parts['optional'], exclusions)

    @classmethod
    def from_mvn_str(cls, mvnstr):
        """
        Create Dependency from Maven-style definition

        The string should be in the format of:
           groupId:artifactId[:extension[:classifier]][:version]

        Where last part is always considered to be version unless empty
        """
        p = cls.get_parts_from_mvn_str(mvnstr)
        return cls(p['groupId'], p['artifactId'], p['extension'],
                   p['classifier'], p['version'])
