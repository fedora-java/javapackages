from javapackages.maven.artifact import Artifact
from javapackages.maven.printer import Printer

import javapackages.metadata.pyxbmetadata as m


class MetadataAlias(object):
    def __init__(self, groupId, artifactId, extension, classifier):

        self.groupId = groupId
        self.artifactId = artifactId
        self.extension = extension or "jar"
        self.classifier = classifier

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId, self.artifactId,
                                   self.extension, self.classifier)

    def to_metadata(self):
        a = m.ArtifactAlias()
        a.groupId = self.groupId
        a.artifactId = self.artifactId
        a.classifier = self.classifier or None
        if self.extension != "jar":
            a.extension = self.extension or None
        return a

    def __hash__(self):
        h = 87
        h += 15 + hash(self.groupId)
        h += 25 + hash(self.artifactId)
        h += 35 + hash(self.extension)
        h += 45 + hash(self.classifier)
        return h

    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        if (self.groupId == other.groupId and
           self.artifactId == other.artifactId and
           self.extension == other.extension and
           self.classifier == other.classifier):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_metadata(cls, metadata):
        groupId = metadata.groupId.strip()
        artifactId = metadata.artifactId.strip()
        extension = metadata.extension
        classifier = metadata.classifier

        return cls(groupId, artifactId, extension, classifier)

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, extension=a.extension,
                   classifier=a.classifier)
