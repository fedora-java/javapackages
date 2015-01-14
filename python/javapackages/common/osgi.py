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
# Authors:  Alexander Kurtakov <akurtako@redhat.com>
#           Michal Srb <msrb@redhat.com>

import re

from javapackages.common.manifest import Manifest
from javapackages.common.util import sanitize_version


class OSGiUtils(object):

    @staticmethod
    def get_rpm_str(bundle, version="", namespace=""):
        ns = namespace
        if version:
            version = sanitize_version(version)
        return "{ns}{d}osgi({bundle}){eq}{version}".format(ns=ns,
                                                           d="-" if ns else "",
                                                           bundle=bundle,
                                                           eq=" = " if version else "",
                                                           version=version)


class OSGiRequire(object):

    def __init__(self, bundle, namespace=""):
        self.bundle = bundle
        self.namespace = namespace

    @staticmethod
    def parse(osgistr):
        result = re.split("[()]", osgistr)
        namespace = ""
        try:
            bundle = result[0]
            namespace = result[1]
        except IndexError:
            pass
        return (bundle, namespace)

    @classmethod
    def from_string(cls, osgistr):
        bundle, namespace = OSGiRequire.parse(osgistr)
        return cls(bundle, namespace=namespace)

    @classmethod
    def from_properties(cls, properties):
        requires = []
        try:
            reqstr = properties["osgi.requires"]
            for r in reqstr.split(","):
                req = OSGiRequire.from_string(r)
                if req:
                    requires.append(req)
        except:
            pass

        return requires

    def get_rpm_str(self, version="", namespace=""):
        ns = namespace or self.namespace
        return OSGiUtils.get_rpm_str(self.bundle, version=version, namespace=ns)


class OSGiBundle(object):

    def __init__(self, bundle, version, namespace="", requires=[]):
        self.bundle = bundle
        self.version = version
        self.namespace = namespace
        self.requires = requires

    @staticmethod
    def parse(osgistr):
        namespace = ""
        version = ""
        reqstr = ""
        requires = []
        result = osgistr.split()
        try:
            bundle = result[0]
            version = result[1]
            reqstr = result[2]
        except IndexError:
            pass
        bundle, namespace = OSGiRequire.parse(bundle)

        if reqstr:
            requires.extend([OSGiRequire.from_string(x) for x in reqstr.split(",")])

        return (bundle, version, namespace, requires)

    @classmethod
    def from_string(cls, osgistr):
        bundle, version, namespace, requires = OSGiBundle.parse(osgistr)
        return cls(bundle, version=version, namespace=namespace,
                   requires=requires)

    @classmethod
    def from_manifest(cls, path):
        try:
            manifest = Manifest(path)
        except IOError:
            return None
        bundle, version = manifest.get_provides()
        requires = []
        requires.extend([OSGiRequire.from_string(x) for x in manifest.get_requires()])

        if not bundle:
            return None
        return cls(bundle, version=version, requires=requires)

    @classmethod
    def from_properties(cls, properties):
        osgi_id = ""
        version = ""
        namespace = ""
        try:
            osgi_id = properties["osgi.id"]
            version = properties["osgi.version"]
        except KeyError:
            return None

        try:
            namespace = properties["osgi.namespace"]
        except KeyError:
            pass

        requires = OSGiRequire.from_properties(properties)

        return cls(osgi_id, version=version, namespace=namespace,
                   requires=requires)

    def __eq__(self, other):
        if not isinstance(other, (OSGiBundle, OSGiRequire)):
            return False
        if self.bundle != other.bundle:
            return False
        if self.namespace != other.namespace:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_rpm_str(self, version="", namespace=""):
        ver = version or self.version
        ns = namespace or self.namespace
        return OSGiUtils.get_rpm_str(self.bundle, version=ver, namespace=ns)
