#!/usr/bin/python
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

import os
import pickle
import re
import subprocess

import javapackages.common.config as config
from javapackages.common.manifest import Manifest
from javapackages.common.util import execute_command


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

    def get_rpm_str(self, version="", namespace=""):
        ns = namespace or self.namespace
        verstr = ""
        if version:
            verstr = " = {ver}".format(ver=version)
        return "{ns}{d}osgi({bundle}){verstr}".format(ns=ns,
                                                      d="-" if ns else "",
                                                      bundle=self.bundle,
                                                      verstr=verstr)


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
        try:
            osgi_id = properties["osgi.id"]
            version = properties["osgi.version"]
        except KeyError:
            return None
        bundle, _, namespace, _ = OSGiBundle.parse(osgi_id)

        requires = []
        try:
            reqstr = properties["osgi.requires"]
            for r in reqstr.split(","):
                req = OSGiRequire.from_string(r)
                if req:
                    requires.append(req)
        except:
            pass

        return cls(bundle, version=version, namespace=namespace,
                   requires=requires)

    def get_rpm_str(self, version="", namespace=""):
        return "{ns}{d}osgi({bundle}) = {version}".format(ns=namespace or self.namespace,
                                                          d="-" if self.namespace else "",
                                                          bundle=self.bundle,
                                                          version=version or self.version)


class OSGiResolver(object):

    # FIXME: make it configurable
    _binpath = "/usr/share/java-utils/p2-install"

    @staticmethod
    def process_metadata(metadata, scl=None):
        artifacts = metadata.get_provided_artifacts()
        paths = []
        paths.extend([x.get_buildroot_path() for x in artifacts])
        return OSGiResolver.process_paths(paths, scl=scl)

    @staticmethod
    def process_path(path, scl=None):
        bundle = OSGiResolver.process_paths([path], scl=scl)
        if bundle:
            return bundle[0]
        return None

    @staticmethod
    def process_paths(paths, scl=None):
        return OSGiResolver._call_script(paths, scl=scl)

    @staticmethod
    def is_available():
        if os.path.exists(OSGiResolver._binpath):
            return True
        return False

    @staticmethod
    def _call_script(paths, scl=None):
        args = "--name rpmdepgen --dry-run --print-deps"
        rc, stdout, stderr = execute_command(OSGiResolver._binpath,
                                             args=[args.split()],
                                             enable_scl=scl)
        if rc != 0:
            raise Exception(stderr)
        result = stdout.split("\n")[:-1]
        return [OSGiBundle.from_string(x) for x in result]


def check_path_in_metadata(path, cachedir_path):
    buildroot = config.get_buildroot()

    from javapackages.metadata.metadata import Metadata, MetadataInvalidException
    artifacts = Metadata.read_provided_artifacts_from_cache(cachedir_path)
    if artifacts is None:
        artifacts = []
        metadata_paths = []
        for dirpath, dirnames, filenames in os.walk(buildroot):
            for filename in filenames:
                fpath = os.path.abspath(os.path.join(dirpath, filename))
                # FIXME: add path to metadata directory to config file?
                if "/maven-metadata/" in fpath:
                    metadata_paths.append(fpath)
        try:
            mdata = Metadata(metadata_paths)
            artifacts = mdata.write_provided_artifacts_to_cache(cachedir_path)
        except MetadataInvalidException:
            pass

    for a in artifacts:
        path = os.path.abspath(path)
        if path.startswith(buildroot):
            path = path[len(buildroot):]
            path = os.path.join('/', path)
        if a.path and a.has_osgi_information():
            if (os.path.abspath(a.path) == path or
               (path.startswith(os.path.abspath(a.path)) and
               os.path.realpath(buildroot + path))):
                return True
    return False


class OSGiCache(object):

    def __init__(self, cachedir, scl=None):
        self._cachedir = cachedir
        self._cache = self._read_osgi_cache()
        self._scl = scl

        if self._cache is None:
            cache = self._process_osgi_in_buildroot()
            self._write_osgi_cache(cache)
            self._cache = cache

    def get_bundle_for_path(self, path):
        try:
            return self._cache[path]
        except KeyError:
            pass
        return None

    def get_bundle(self, name):
        for bundle in self._cache.values():
            if bundle == name:
                return bundle
        return None

    def _process_osgi_in_buildroot(self):
        # "path: OSGiBundle" mapping
        cache = {}

        bundle_paths = self._find_possible_bundles()
        for path in bundle_paths:
            if OSGiResolver.is_available():
                bundle = OSGiResolver.process_path(path, scl=self._scl)
            else:
                bundle = OSGiBundle.from_manifest(path)
            if bundle:
                cache.update({path: bundle})

        return cache

    def _find_possible_bundles(self):
        buildroot = config.get_buildroot()
        paths = []
        for dirpath, _, filenames in os.walk(buildroot):
            for filename in filenames:
                fpath = os.path.abspath(os.path.join(dirpath, filename))
                if self._check_path(fpath):
                    paths.append(fpath)
        return paths

    def _check_path(self, path):
        if os.path.islink(path):
            return False
        if path.endswith(".jar"):
            return True
        if path.endswith("/MANIFEST.MF"):
            # who knows where the manifest can be in buildroot.
            # this is an attempt to identify only MANIFEST.MF files
            # which are in %{_datadir} or %{_prefix}/lib
            if "/usr/share/" in path or "/usr/lib" in path:
                return True
        return False

    def _read_osgi_cache(self):
        try:
            cachefile = open(os.path.join(self._cachedir,
                                          config.osgi_cache_f), 'rb')
            cache = pickle.load(cachefile)
            cachefile.close()
        except IOError:
            return None
        return cache

    def _write_osgi_cache(self, cache):
        try:
            cachefile = open(os.path.join(self._cachedir,
                                          config.osgi_cache_f), 'wb')
            pickle.dump(cache, cachefile)
            cachefile.close()
        except IOError:
            return None
        return cache
