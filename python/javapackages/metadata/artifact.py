import javapackages.common.config as config
from javapackages.common.osgi import OSGiBundle
from javapackages.maven.artifact import Artifact
from javapackages.maven.pom import POM
from javapackages.maven.printer import Printer

from javapackages.metadata.alias import MetadataAlias
from javapackages.metadata.dependency import MetadataDependency
import javapackages.metadata.pyxbmetadata as m

import pyxb.utils.six as six
import pyxb
import os
import logging
from xml.dom.minidom import getDOMImplementation


# for Python 2.6 compatibility
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
# Prevent warnings from PyXB about missing logger handler:
# No handlers could be found for logger "pyxb.binding.basis"
logging.getLogger("pyxb.binding.basis").addHandler(NullHandler())


class MetadataArtifact(object):
    def __init__(self, groupId, artifactId, extension="",
                 classifier="", version="", namespace="",
                 path="", aliases=None, compatVersions=None,
                 properties=None, dependencies=None):

        self.groupId = groupId
        self.artifactId = artifactId
        self.extension = extension or "jar"
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
        return True if self.compatVersions else False

    def has_osgi_information(self):
        if self.properties:
            try:
                self.properties["osgi.id"]
                return True
            except KeyError:
                pass
        return False

    def get_osgi_bundle(self):
        if not self.properties:
            return None
        return OSGiBundle.from_properties(self.properties)

    def get_buildroot_path(self, prefix=None):
        if not self.path:
            return None
        if prefix is None:
            prefix = config.get_buildroot()
        return os.path.join(prefix, self.path[1:])

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId, self.artifactId,
                                   self.extension, self.classifier,
                                   self.version)

    def get_rpm_str(self, namespace="", pkgver=None):
        result = []

        if not self.is_compat():
            # non-compat rpm string for main artifact
            result.append(Printer.get_rpm_str(self.groupId, self.artifactId,
                          self.extension, self.classifier, namespace=namespace, pkgver=pkgver))

            # non-compat rpm string(s) for aliases
            for alias in self.aliases:
                result.append(Printer.get_rpm_str(alias.groupId, alias.artifactId, alias.extension,
                                                  alias.classifier, namespace=namespace, pkgver=pkgver))
        else:
            # compat rpm string(s) for main artifact
            for compat_ver in self.compatVersions:
                result.append(Printer.get_rpm_str(self.groupId, self.artifactId, self.extension, self.classifier,
                                                  compat=compat_ver, namespace=namespace, pkgver=pkgver))

                # compat rpm string(s) for aliases
                for alias in self.aliases:
                    result.append(Printer.get_rpm_str(alias.groupId, alias.artifactId, alias.extension,
                                                      alias.classifier, compat=compat_ver,
                                                      namespace=namespace, pkgver=pkgver))
        return "\n".join(result)

    def __unicode__(self):
        return six.text_type(self.get_mvn_str())

    def __str__(self):
        return self.__unicode__()

    def __hash__(self):
        h = 26
        h += 11 + hash(self.groupId)
        h += 21 + hash(self.artifactId)
        h += 31 + hash(self.extension)
        h += 41 + hash(self.classifier)
        h += 61 + hash(self.namespace)
        h += 71 + hash(self.is_compat())
        return h

    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        if (self.groupId == other.groupId and
           self.artifactId == other.artifactId and
           self.extension == other.extension and
           self.classifier == other.classifier and
           self.namespace == other.namespace and
           self.is_compat() == other.is_compat()):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

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
            props = [self._create_property(k, v) for k, v in six.iteritems(self.properties)]
            a.properties = pyxb.BIND(*props)
        return a

    def _create_property(self, name, value):
        domimpl = getDOMImplementation()
        doc = domimpl.createDocument(None, None, None)
        elem = doc.createElement(name)
        tnode = doc.createTextNode(value)
        elem.appendChild(tnode)
        return elem

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
            compatVersions = set(cv for cv in metadata.compatVersions.version)

        aliases = set()
        if hasattr(metadata, 'aliases') and metadata.aliases:
            for alias in metadata.aliases.alias:
                alias_extension = metadata.extension
                alias_classifier = ""
                if hasattr(alias, 'extension') and alias.extension:
                    alias_extension = alias.extension

                if hasattr(alias, 'classifier') and alias.classifier:
                    alias_classifier = alias.classifier

                aliases.add(MetadataAlias(alias.groupId,
                                          alias.artifactId,
                                          alias_extension,
                                          alias_classifier))
        properties = {}
        if hasattr(metadata, 'properties') and metadata.properties:
            properties = dict((prop.tagName, prop.firstChild.value)
                          for prop in metadata.properties.wildcardElements())

        dependencies = set()
        if hasattr(metadata, 'dependencies') and metadata.dependencies:
            dependencies = set(MetadataDependency.from_metadata(dep)
                            for dep in metadata.dependencies.dependency)

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
