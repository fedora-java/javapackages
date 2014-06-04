from pom.artifact import Artifact
from pom.pom import POM
from pom.printer import Printer

import metadata as m
import pyxb


class MetadataArtifact(object):
    def __init__(self, groupId, artifactId, extension="",
                 classifier="", version="", namespace="",
                 path="", aliases=None, compatVersions=None,
                 properties=None, dependencies=None):


        self.groupId = groupId
        self.artifactId = artifactId
        self.extension= extension
        self.classifier = classifier
        self.version = version
        self.namespace = namespace
        self.path = path

        self.aliases = aliases or set()
        self.compatVersions = compatVersions or set()
        self.properties = properties or {}
        self.dependencies = dependencies or set()

    def is_compat(self):
        """Return true if artifact has compat verions specified.
        This means package should have versioned provides for this artifact"""

        return self.compatVersions

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId, self.artifactId,
                                   self.extension, self.classifier,
                                   self.version)

    def to_metadata(self):
        a = m.ArtifactMetadata()
        a.groupId = self.groupId
        a.artifactId = self.artifactId
        a.version = self.version
        a.classifier = self.classifier or None
        a.extension = self.extension or None
        a.namespace = self.namespace or None
        a.path = self.path or None
        if self.dependencies:
            deps = [d.to_metadata() for d in self.dependencies]
            a.dependencies = pyxb.BIND(*deps)
        if self.compatVersions:
            a.compatVersions = pyxb.BIND(*self.compatVersions)

        if self.aliases:
            als = [alias.to_metadata() for alias in self.aliases]
            a.aliases = pyxb.BIND(*als)

        if self.properties:
            import javapackages.depmap
            prop = [javapackages.depmap.Depmap.build_property(k, v) for k, v in self.properties.iteritems()]
            a.properties = pyxb.BIND(*prop)

        return a

    @classmethod
    def from_metadata(cls, metadata):
        groupId = metadata.groupId.strip()
        artifactId = metadata.artifactId.strip()
        version = extension = classifier = namespace = path = ""
        if hasattr(metadata, 'path') and metadata.path:
            path = metadata.path.strip()
        if hasattr(metadata, 'version') and metadata.version:
            version = metadata.version.strip()
        if hasattr(metadata, 'extension') and metadata.extension:
            extension = metadata.extension.strip()
        if hasattr(metadata, 'classifier') and metadata.classifier:
            classifier = metadata.classifier.strip()
        if hasattr(metadata, 'namespace') and metadata.namespace:
            namespace = metadata.namespace.strip()

        compatVersions = set()
        if hasattr(metadata, 'compatVersions') and metadata.compatVersions:
            compatVersions = {cv for cv in metadata.compatVersions.version}

        aliases = set()
        if hasattr(metadata, 'aliases') and metadata.aliases:
            for alias in metadata.aliases.alias:
                alias_extension = alias_classifier = ""
                if hasattr(alias, 'extension') and alias.extension:
                    alias_extension = alias.extension

                if hasattr(alias, 'classifier') and alias.classifier:
                    alias_classifier = alias.classifier

                aliases.add(Alias(alias.groupId,
                                     alias.artifactId,
                                     alias_extension,
                                     alias_classifier))
        properties = {}
        if hasattr(metadata, 'properties') and metadata.properties:
            properties = {prop.tagName:prop.firstChild.value
                          for prop in metadata.properties.wildcardElements()}

        dependencies = set()
        if hasattr(metadata, 'dependencies') and metadata.dependencies:
            dependencies = {Dependency.from_metadata(dep)
                            for dep in metadata.dependencies.dependency}

        return cls(groupId, artifactId, extension, classifier, version,
                   namespace, path=path, aliases=aliases,
                   compatVersions=compatVersions, properties=properties,
                   dependencies=dependencies)

    @classmethod
    def from_pom(cls, pom_path):
        pom = POM(pom_path)
        return cls(pom.groupId, pom.artifactId, version=pom.version,
                   path=pom_path)

    @classmethod
    def from_mvn_str(cls, mvn_str):
        a = Artifact.from_mvn_str(mvn_str)

        return cls(a.groupId, a.artifactId, version=a.version,
                   extension=a.extension, classifier=a.classifier)
