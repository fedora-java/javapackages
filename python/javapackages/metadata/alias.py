from javapackages.maven.artifact import Artifact
from javapackages.maven.printer import Printer

from javapackages.common.binding import ObjectBinding


class MetadataAlias(ObjectBinding):
    element_name = 'alias'
    fields = ['groupId', 'artifactId', 'extension', 'classifier']
    defaults = {'extension': 'jar'}

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId, self.artifactId,
                                   self.extension, self.classifier)

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, extension=a.extension,
                   classifier=a.classifier)
