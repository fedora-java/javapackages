from pom.artifact import Artifact
from pom.printer import Printer

import metadata as m


# TODO: this is very similar to MetadataAlias
class MetadataSkippedArtifact(object):
    def __init__(self, groupId, artifactId, extension, classifier):

        self.groupId = groupId
        self.artifactId = artifactId
        self.extension = extension
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
