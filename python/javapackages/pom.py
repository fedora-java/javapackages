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

from xml.etree.ElementTree import ElementTree

class PomLoadingException(Exception):
    pass

class POM(object):
    """
    Class for querying basic information from pom.xml files used by Apache Maven
    """
    def __init__(self, path):
        et = ElementTree ()
        self.__doc = et.parse(path)

        if self.__doc is None:
            raise PomLoadingException("Failed to load pom.xml. You have a problem")


    def __find(self, xpath):
        ret = self.__doc.find(xpath, namespaces=dict(pom='http://maven.apache.org/POM/4.0.0'))
        # perhaps there is no namespace?
        if ret is None:
            ret = self.__doc.find(xpath.replace('pom:',''))
        return ret

    @property
    def groupId(self):
        """
        Effective groupId of the pom Artifact taking into account parent groupId
        """
        gId = self.__find('./pom:groupId')
        if gId is None:
            gId = self.__find('./pom:parent/pom:groupId')
        return gId.text

    @property
    def artifactId(self):
        """
        Effective artifactId of the pom Artifact
        """
        return self.__find('./pom:artifactId').text

    @property
    def version(self):
        """
        Effective version of the pom Artifact taking into account parent
        version
        """
        version = self.__find('./pom:version')
        if version is None:
            version = self.__find('./pom:parent/pom:version').text
        return version.text

    @property
    def packaging(self):
        """
        Packaging type of artifact or None if unspecified
        """
        p = self.__find('./pom:packaging')
        if p is not None:
            return p.text
        return None
