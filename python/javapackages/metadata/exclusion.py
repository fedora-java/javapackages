from javapackages.maven.artifact import Artifact
from javapackages.maven.printer import Printer
import javapackages.metadata.pyxbmetadata as m


class MetadataExclusion(object):
    def __init__(self, groupId, artifactId):

        self.groupId = groupId
        self.artifactId = artifactId

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId, self.artifactId)

    def to_metadata(self):
        return m.DependencyExclusion(self.groupId, self.artifactId)

    def __hash__(self):
        h = 67
        h += 13 + hash(self.groupId)
        h += 23 + hash(self.artifactId)
        return h

    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        if (self.groupId == other.groupId and
           self.artifactId == other.artifactId):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_metadata(cls, metadata):
        groupId = metadata.groupId.strip()
        artifactId = metadata.artifactId.strip()

        return cls(groupId, artifactId)

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, version=a.version,
                   extension=a.extension, classifier=a.classifier)

    @classmethod
    def from_mvn_exclusion(cls, mvn_exc):
        return cls(mvn_exc.groupId, mvn_exc.artifactId)
