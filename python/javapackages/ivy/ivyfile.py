#-
# Copyright (c) 2014, Red Hat, Inc.
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

from javapackages.maven.pomreader import POMReader, PomLoadingException

import os


class IvyFile(object):
    """
    Class for querying basic information from ivy.xml files used by Apache Ivy
    """
    def __init__(self, path):
        self.__doc = POMReader.load(path)
        self._path = os.path.join(path)

    def __str__(self):
        return ":".join([self.groupId, self.artifactId, self.version])

    @property
    def parent(self):
        return None

    @property
    def parentGroupId(self):
        return None

    @property
    def parentArtifactId(self):
        return None

    @property
    def parentVersion(self):
        return None

    @property
    def groupId(self):
        gId = POMReader.find(self.__doc, '/ivy-module/info')
        if gId is not None:
            try:
                gId = gId.attrib["organisation"]
            except:
                raise PomLoadingException("Unable to determine groupId")
        return gId

    @property
    def artifactId(self):
        aId = POMReader.find(self.__doc, '/ivy-module/info')
        if aId is not None:
            try:
                aId = aId.attrib["module"]
            except KeyError:
                raise PomLoadingException("Unable to determine artifactId")
        return aId

    @property
    def version(self):
        version = POMReader.find(self.__doc, '/ivy-module/info')
        if version is not None:
            try:
                version = version.attrib["revision"]
            except KeyError:
                raise PomLoadingException("Unable to determine version")
        return version

    # only for compatibility with POM, this will be removed in future
    @property
    def packaging(self):
        return None

    @property
    def dependencies(self):
        return []

    @property
    def dependencyManagement(self):
        return []

    @property
    def pluginManagement(self):
        return []

    @property
    def plugins(self):
        return []

    @property
    def extensions(self):
        return []

    @property
    def properties(self):
        return {}
