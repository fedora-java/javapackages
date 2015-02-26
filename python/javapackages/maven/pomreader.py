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

from lxml.etree import ElementTree, XMLParser
from javapackages.common.exception import JavaPackagesToolsException


class PomLoadingException(JavaPackagesToolsException):
    pass


POM_NAMESPACE = "http://maven.apache.org/POM/4.0.0"


def load(pom_path):
    et = ElementTree()
    parser = XMLParser(remove_comments=True, strip_cdata=True)
    try:
        doc = et.parse(pom_path, parser=parser)
    except IOError:
        raise PomLoadingException("Cannot read file {f}".format(f=pom_path))

    if doc is None:
        raise PomLoadingException("Failed to load {f}".format(f=pom_path))
    return doc


def find(doc, xpath_str, namespace=POM_NAMESPACE):
    ret = xpath(doc, xpath_str, namespace)
    if len(ret) > 0:
        ret = ret[0]
    else:
        ret = None
    return ret


def xpath(doc, xpath_str, namespace=POM_NAMESPACE):
    ret = doc.xpath(xpath_str, namespaces=dict(pom=namespace))
    # perhaps there is no namespace?
    if len(ret) == 0:
        ret = doc.xpath(xpath_str.replace('pom:', ''))
    return ret


def find_parts(doc, parts, xpath_str=".//"):
    for key in parts:
        node = doc.xpath('{0}*[local-name() = "{1}"]'.format(xpath_str, key))
        if node is not None and len(node) > 0 and node[0].text is not None:
            parts[key] = node[0].text.strip()
    return parts


def find_raw_parts(doc, parts, xpath_str=".//"):
    for key in parts:
        node = doc.xpath('{0}*[local-name() = "{1}"]'.format(xpath_str, key))
        if node is not None and len(node) > 0:
            if node[0].text is not None:
                parts[key] = node[0].text.strip()
            else:
                # node is present, but it has no content
                parts[key] = ""
        else:
            parts[key] = None
    return parts
