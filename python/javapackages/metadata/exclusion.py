from javapackages.maven.artifact import Artifact
from javapackages.maven.printer import Printer

from javapackages.common.binding import ObjectBinding


class MetadataExclusion(ObjectBinding):
    element_name = 'exclusion'
    fields = ['groupId', 'artifactId']

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId, self.artifactId)

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, version=a.version,
                   extension=a.extension, classifier=a.classifier)

    @classmethod
    def from_mvn_exclusion(cls, mvn_exc):
        return cls(mvn_exc.groupId, mvn_exc.artifactId)
