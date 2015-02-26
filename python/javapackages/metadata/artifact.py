import javapackages.common.config as config
from javapackages.common.osgi import OSGiBundle
from javapackages.maven.artifact import Artifact
from javapackages.maven.pom import POM
import javapackages.maven.printer as Printer

from javapackages.metadata.alias import MetadataAlias
from javapackages.metadata.dependency import MetadataDependency

from javapackages.common.binding import ObjectBinding

import six
import os


class MetadataArtifact(ObjectBinding):
    element_name = 'artifact'
    fields = ['groupId', 'artifactId', 'extension', 'classifier',
              'version', 'namespace', 'path', 'aliases', 'properties',
              'compatVersions', 'dependencies']
    defaults = {'extension': 'jar'}
    types = {'compatVersions': set(['version']),
             'aliases': set([MetadataAlias]),
             'dependencies': set([MetadataDependency]),
             'properties': dict}

    def __init__(self, *args, **kwargs):
        super(MetadataArtifact, self).__init__(*args, **kwargs)
        for alias in self.aliases:
            if not 'extension' in alias and 'extension' in self:
                alias.extension = self.extension

    def is_compat(self):
        """Return true if artifact has compat verions specified.
        This means package should have versioned provides for this artifact"""
        return True if self.compatVersions else False

    def has_osgi_information(self):
        return "osgi.id" in self.properties

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
