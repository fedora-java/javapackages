from javapackages.maven.artifact import Artifact
from javapackages.maven.printer import Printer
from exclusion import MetadataExclusion

import pyxbmetadata as m
import pyxb
import sys


class MetadataDependency(object):
    def __init__(self, groupId, artifactId, extension="",
                 classifier="", namespace="",
                 requestedVersion="", resolvedVersion="",
                 exclusions=set()):

        self.groupId = groupId
        self.artifactId = artifactId
        self.extension = extension or "jar"
        self.classifier = classifier
        self.namespace = namespace
        self.requestedVersion = requestedVersion or "SYSTEM"
        self.resolvedVersion = resolvedVersion
        self.exclusions = exclusions or set()

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId, self.artifactId,
                                   self.extension, self.classifier,
                                   self.requestedVersion)

    def get_rpm_str(self, namespace="", compat=False, pkgver=None):
        return Printer.get_rpm_str(self.groupId, self.artifactId,
                                   self.extension, self.classifier,
                                   self.requestedVersion,
                                   namespace=namespace or self.namespace,
                                   compat=compat or self.resolvedVersion,
                                   pkgver=pkgver)

    def is_provided_by(self, artifacts):
        for provided in artifacts:
            if (provided.groupId == self.groupId and
               provided.artifactId == self.artifactId and
               provided.classifier == self.classifier and
               provided.extension == self.extension and
               provided.namespace == self.namespace):

                if self.resolvedVersion and provided.is_compat():
                    # does it match one of provided compat?
                    for compatVer in provided.compatVersions:
                        if self.resolvedVersion == compatVer:
                            return True, provided.version
                elif (not self.resolvedVersion and
                      not provided.is_compat()):
                    return True, provided.version
                break
        return False, None

    def to_metadata(self):
        d = m.Dependency()
        d.groupId = self.groupId
        d.artifactId = self.artifactId
        d.requestedVersion = self.requestedVersion or None
        d.resolvedVersion = self.resolvedVersion or None
        d.classifier = self.classifier or None
        d.extension = self.extension or None
        if self.exclusions:
            excl = {e.to_metadata() for e in self.exclusions}
            d.exclusions = pyxb.BIND(*excl)
        return d

    def __unicode__(self):
        return unicode(self.get_mvn_str())

    def __str__(self):
        return unicode(self).encode(sys.getfilesystemencoding())

    @classmethod
    def from_metadata(cls, metadata):
        groupId = metadata.groupId.strip()
        artifactId = metadata.artifactId.strip()

        requestedVersion = resolvedVersion = extension = classifier = namespace = ""
        if hasattr(metadata, 'requestedVersion') and metadata.requestedVersion:
            requestedVersion = metadata.requestedVersion.strip()
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

        return cls(groupId, artifactId, extension, classifier,
                   namespace, requestedVersion, resolvedVersion,
                   exclusions)

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, extension=a.extension,
                   classifier=a.classifier, requestedVersion=a.version)

    @classmethod
    def from_mvn_dependency(cls, mvn_dep):
        exclusions = set()
        for e in mvn_dep.exclusions:
            exclusions.add(MetadataExclusion.from_mvn_exclusion(e))

        return cls(mvn_dep.groupId, mvn_dep.artifactId,
                   extension=mvn_dep.extension,
                   classifier=mvn_dep.classifier,
                   requestedVersion=mvn_dep.version,
                   exclusions=exclusions)
