#!/usr/bin/python
# Copyright (c) 2013, Red Hat, Inc
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
# 3. Neither the name of Red Hat nor the names of its
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
# Authors:  Stanislav Ochotnicky <sochotnicky@redhat.com>

from javapackages.artifact import Artifact

class Dependency(object):

    def __init__(self, groupId, artifactId, requestedVersion,
                 resolvedVersion="", extension="", classifier="",
                 namespace="", exclusions=[]):
        self.groupId = groupId
        self.artifactId = artifactId
        self.requestedVersion = requestedVersion
        self.resolvedVersion = resolvedVersion
        self.extension = extension
        self.classifier = classifier
        self.namespace = namespace
        self.exclusions = exclusions


    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.groupId.__hash__() + \
               self.artifactId.__hash__() + \
               self.requestedVersion.__hash__() + \
               self.resolvedVersion.__hash__() + \
               self.extension.__hash__() + \
               self.classifier.__hash__() + \
               self.namespace.__hash__()



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

        exclusions = []
        if hasattr(metadata, 'exclusions') and metadata.exclusions:
            for excl in metadata.exclusions.exclusion:
                eclusions.append(Artifact.from_metadata(excl))

        return cls(groupId, artifactId, requestedVersion, resolvedVersion,
                   extension, classifier, namespace, exclusions)
