#
# Copyright (c) 2015, Red Hat, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the Red Hat nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:  Michal Srb <msrb@redhat.com>

import javapackages.common.config as config
from javapackages.common.osgi import OSGiBundle
from javapackages.maven.artifact import Artifact
from javapackages.maven.pom import POM
import javapackages.common.strutils as Printer

from javapackages.metadata.alias import MetadataAlias
from javapackages.metadata.dependency import MetadataDependency

from javapackages.common.binding import ObjectBinding

import os


class MetadataArtifact(ObjectBinding):
    element_name = 'artifact'
    fields = ['groupId', 'artifactId', 'extension', 'classifier',
              'version', 'namespace', 'path', 'aliases', 'properties',
              'compatVersions', 'dependencies']
    defaults = {'extension': 'jar'}
    types = {'compatVersions': set(['version']),
             'aliases': list([MetadataAlias]),
             'dependencies': list([MetadataDependency]),
             'properties': dict}

    def __init__(self, *args, **kwargs):
        super(MetadataArtifact, self).__init__(*args, **kwargs)
        for alias in self.aliases:
            if 'extension' not in alias and 'extension' in self:
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
        return Printer.get_mvn_str(self.groupId,
                                   self.artifactId,
                                   ext=self.extension,
                                   cla=self.classifier,
                                   ver=self.version)

    def get_rpm_str(self, namespace=None, pkg_ver=None):
        result = []

        if not self.is_compat():
            # non-compat rpm string for main artifact
            result.append(Printer.get_rpm_str(self.groupId,
                                              self.artifactId,
                                              ext=self.extension,
                                              cla=self.classifier,
                                              namespace=namespace,
                                              pkg_ver=pkg_ver))

            # non-compat rpm string(s) for aliases
            for alias in self.aliases:
                result.append(Printer.get_rpm_str(alias.groupId,
                                                  alias.artifactId,
                                                  ext=alias.extension,
                                                  cla=alias.classifier,
                                                  namespace=namespace,
                                                  pkg_ver=pkg_ver))
        else:
            # compat rpm string(s) for main artifact
            for compat_ver in self.compatVersions:
                result.append(Printer.get_rpm_str(self.groupId,
                                                  self.artifactId,
                                                  ext=self.extension,
                                                  cla=self.classifier,
                                                  compat_ver=compat_ver,
                                                  namespace=namespace,
                                                  pkg_ver=pkg_ver))

                # compat rpm string(s) for aliases
                for alias in self.aliases:
                    result.append(Printer.get_rpm_str(alias.groupId,
                                                      alias.artifactId,
                                                      ext=alias.extension,
                                                      cla=alias.classifier,
                                                      compat_ver=compat_ver,
                                                      namespace=namespace,
                                                      pkg_ver=pkg_ver))
        return "\n".join(result)

    def __unicode__(self):
        return self.get_mvn_str()

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
