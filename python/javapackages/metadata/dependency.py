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

from javapackages.maven.artifact import Artifact
import javapackages.common.strutils as Printer
from javapackages.metadata.exclusion import MetadataExclusion

from javapackages.common.binding import ObjectBinding

import six


class MetadataDependency(ObjectBinding):
    element_name = 'dependency'
    fields = ['groupId', 'artifactId', 'extension', 'classifier',
              'namespace', 'optional', 'requestedVersion',
              'resolvedVersion', 'exclusions']
    defaults = {'extension': 'jar',
                'requestedVersion': 'SYSTEM'}
    types = {'optional': str,  # todo bool
             'exclusions': set([MetadataExclusion])}

    def is_optional(self):
        if self.optional and self.optional.lower() == "true":
            return True
        return False

    def get_mvn_str(self):
        return Printer.get_mvn_str(self.groupId,
                                   self.artifactId,
                                   ext=self.extension,
                                   cla=self.classifier,
                                   ver=self.requestedVersion)

    def get_rpm_str(self, namespace=None, compat_ver=None, pkg_ver=None):
        return Printer.get_rpm_str(self.groupId,
                                   self.artifactId,
                                   ext=self.extension,
                                   cla=self.classifier,
                                   namespace=namespace or self.namespace,
                                   compat_ver=compat_ver or self.resolvedVersion,
                                   pkg_ver=pkg_ver)

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

    def is_skipped(self, skipped_artifacts):
        for skipped in skipped_artifacts:
            if (self.groupId == skipped.groupId and
               self.artifactId == skipped.artifactId and
               self.classifier == skipped.classifier and
               self.extension == skipped.extension):
                return True
        return False

    def __unicode__(self):
        return six.text_type(self.get_mvn_str())

    def __str__(self):
        return self.__unicode__()

    def __hash__(self):
        h = 47
        h += 12 + hash(self.groupId)
        h += 22 + hash(self.artifactId)
        h += 32 + hash(self.extension)
        h += 42 + hash(self.classifier)
        h += 62 + hash(self.namespace)
        h += 72 + hash(self.resolvedVersion)
        return h

    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        if (self.groupId == other.groupId and
           self.artifactId == other.artifactId and
           self.extension == other.extension and
           self.classifier == other.classifier and
           self.namespace == other.namespace and
           self.resolvedVersion == other.resolvedVersion):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

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
                   optional=mvn_dep.optional,
                   requestedVersion=mvn_dep.version,
                   exclusions=exclusions)
