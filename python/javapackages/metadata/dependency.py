from javapackages.maven.artifact import Artifact
from javapackages.maven.printer import Printer

import metadata as m
import pyxb


class MetadataDependency(object):
    def __init__(self, groupId, artifactId, extension="",
                 classifier="", version="", namespace="",
                 requestedVersion="", resolvedVersion=None,
                 exclusions=set()):

        self.groupId = groupId
        self.artifactId = artifactId
        self.extension = extension
        self.classifier = classifier
        self.version = version
        self.namespace = namespace
        self.requestedVersion = requestedVersion
        self.resolvedVersion = resolvedVersion
        self.exclusions = exclusions or set()

    def is_compat(self):
        """Return true if this is a dependency on compat package"""

        return self.compatVersions

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId, self.artifactId,
                                   self.extension, self.classifier,
                                   self.version)

    def to_metadata(self):
        d = m.Dependency()
        d.groupId = self.groupId
        d.artifactId = self.artifactId
        d.requestedVersion = self.version
        d.classifier = self.classifier or None
        d.extension = self.extension or None
        if self.exclusions:
            excl = {m.MetadataExclusion(e.groupId, e.artifactId)
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
            exclusions = {MetadataExclusion.from_metadata(excl)
                          for excl in metadata.exclusions.exclusion}

        return cls(groupId, artifactId, requestedVersion, resolvedVersion,
                   extension, classifier, namespace, exclusions)

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, version=a.version,
                   extension=a.extension, classifier=a.classifier)
