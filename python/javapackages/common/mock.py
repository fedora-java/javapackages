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
# Authors:  Michael Simacek <msimacek@redhat.com>

from __future__ import print_function

import socket

from javapackages.common.exception import JavaPackagesToolsException
from javapackages.maven.artifact import Artifact

socket_path = '/var/run/mock/pm-request'

class InstallationException(JavaPackagesToolsException):
    def __init__(self, dep, out):
        super(InstallationException, self).__init__()
        self.dep = dep
        self.out = out

class ConnectionException(JavaPackagesToolsException):
    pass

def install_artifact(dep):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(socket_path)
        sock.sendall("install '{0}'\n".format(dep).encode())
        fo = sock.makefile()
        status = fo.readline()
        out = fo.read()
        if status != 'ok\n':
            raise InstallationException(dep, out)
    except socket.error as e:
        raise ConnectionException(e.message)
    finally:
        sock.close()

def install_maven_artifact(artifact_spec):
    artifact = Artifact.from_mvn_str(artifact_spec)
    try:
        install_artifact(artifact.get_rpm_str(compat=artifact.version))
    except InstallationException:
        if not artifact.version:
            raise
        install_artifact(artifact.get_rpm_str())
