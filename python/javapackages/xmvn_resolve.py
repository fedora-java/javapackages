#!/usr/bin/python
# Copyright (c) 2014, Red Hat, Inc
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
# Authors:  Michal Srb <msrb@redhat.com>


import subprocess
import lxml.etree
from artifact import Artifact


class XMvnResolve(object):
    # TODO:
    # - do not hardcode path to xmvn-resolve
    # - documentation

    @staticmethod
    def process_raw_request(raw_request_list):
        request = XMvnResolve.__join_raw_requests(raw_request_list)
        procargs = ['/usr/bin/xmvn-resolve', '--raw-request']
        proc = subprocess.Popen(procargs, shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout = proc.communicate(input=request)[0]
        proc.wait()
        result = XMvnResolve.__process_results(stdout)
        return result

    @staticmethod
    def __join_raw_requests(raw_request_list):
        request = "<requests>"
        for r in raw_request_list:
            request += r.get_xml()
        request += "</requests>"

        return request

    @staticmethod
    def __process_results(result_xml):
        results = []

        doc = lxml.etree.fromstring(result_xml)
        nodes = doc.xpath('/results/result')
        for node in nodes:
            if len(node) > 0:
                ns = node.find('./namespace')
                compat_ver = node.find('./compatVersion')
                results.append(ResolutionResult(ns.text or "",
                                                compat_ver.text or ""))
            else:
                results.append(None)
        return results


class ResolutionResult(object):
    def __init__(self, namespace="", compatVersion=""):
        self.namespace = namespace
        self.compatVersion = compatVersion

    def __str__(self):
        return "version:" + self.compatVersion + "namespace: " + self.namespace


class ResolutionRequest(object):
    def __init__(self, artifact):
        self.artifact = artifact

    def get_xml(self):
        return ResolutionRequest.create_raw_request_xml(self.artifact)

    @staticmethod
    def create_raw_request_xml(artifact):
        template = """
<request>
    <artifact>
        <groupId>{gid}</groupId>
        <artifactId>{aid}</artifactId>{ext}{cla}{ver}
    </artifact>
</request>
"""
        version = ""
        classifier = ""
        extension = ""
        if artifact.extension:
            extension = "<extension>{ext}</extension>".format(ext=extension)
        if artifact.classifier:
            classifier = "<classifier>{cla}</classifier>".format(cla=classifier)
        if artifact.version:
            version = "<version>{ver}</version>".format(ver=artifact.version)

        return template.format(gid=artifact.groupId, aid=artifact.artifactId,
                               ext=extension, cla=classifier, ver=version)


if __name__ == "__main__":
    artifact = Artifact("junit", "junit")

    req = ResolutionRequest(artifact)

    results = XMvnResolve.process_raw_request([req])
    print(len(results))
    print(results[0])
