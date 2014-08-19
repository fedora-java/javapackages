from javapackages.maven.artifact import Artifact
from javapackages.maven.printer import Printer

import javapackages.metadata.pyxbmetadata as m


# TODO: this is very similar to MetadataAlias
class MetadataSkippedArtifact(object):
    def __init__(self, groupId, artifactId, extension="", classifier=""):

        self.groupId = groupId
        self.artifactId = artifactId
        self.extension = extension or "jar"
        self.classifier = classifier

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId, self.artifactId,
                                   self.extension, self.classifier)

    def to_metadata(self):
        a = m.SkippedArtifact()
        a.groupId = self.artifact.groupId
        a.artifactId = self.artifact.artifactId
        a.classifier = self.artifact.classifier or None
        a.extension = self.artifact.extension or None
        return a

    def __hash__(self):
        h = 77
        h += 14 + hash(self.groupId)
        h += 24 + hash(self.artifactId)
        h += 34 + hash(self.extension)
        h += 44 + hash(self.classifier)
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

        extension = classifier = ""
        if hasattr(metadata, 'extension') and metadata.extension:
            extension = metadata.extension.strip()
        if hasattr(metadata, 'classifier') and metadata.classifier:
            classifier = metadata.classifier.strip()

        return cls(groupId, artifactId, extension, classifier)

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, extension=a.extension,
                   classifier=a.classifier)
