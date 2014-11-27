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
        result = osgistr.split(" ")
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

    def get_rpm_str(self, version="", namespace=""):
        return "{ns}{d}osgi({bundle}) = {version}".format(ns=namespace or self.namespace,
                                                          d="-" if self.namespace else "",
                                                          bundle=self.bundle,
                                                          version=version or self.version)


class OSGiResolver(object):

    # FIXME: make it configurable
    _binpath = "/usr/share/java-utils/p2-install"

    @staticmethod
    def process_metadata(metadata):
        artifacts = metadata.get_provided_artifacts()
        paths = []
        paths.extend([x.get_buildroot_path() for x in artifacts])
        return OSGiResolver.process_paths(paths)

    @staticmethod
    def process_path(path):
        return OSGiResolver.process_paths([path])

    @staticmethod
    def process_paths(paths):
        return OSGiResolver._call_script(paths)

    @staticmethod
    def is_available():
        if os.path.exists(OSGiResolver._binpath):
            return True
        return False

    @staticmethod
    def _call_script(paths):
        procargs = [OSGiResolver._binpath, "--name", "rpmdepgen",
                    "--dry-run", "--print-deps"]
        procargs.extend(paths)
        proc = subprocess.Popen(procargs, shell=False, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        stdout, stderr = proc.communicate()
        proc.wait()
        if proc.returncode != 0:
            raise Exception(stderr)
        result = stdout.split("\n")[:-1]
        return [OSGiBundle.from_string(x) for x in result]


def print_provides(provides):
    for key in provides.keys():
        print("osgi({name}) = {ver}".format(name=key,
                                            ver=provides[key]))


def normalize_manifest(manifest):
    lines = []
    manifest = manifest.split(u'\n')
    for line in manifest:
        if line.startswith(' '):
            lines[-1] += line.strip()
        else:
            lines.append(line.strip())
    return lines


def parse_manifest(manifest):
    headers = {}
    DELIM = ": "
    for line in normalize_manifest(manifest):
        split = line.split(DELIM)
        if len(split) > 1:
            name = split[0].strip()
            headers[name] = split[1].strip()
    return headers


def split_bundle_name(bundles):
    bundlenames = []
    bundleline = ""
    for bundle in bundles.split(','):
        if not bundle:
            continue
        if "(" in bundle or "[" in bundle:
            bundleline = bundle
            continue
        if bundleline:
            bundle = bundleline + bundle
        if ":=optional" in bundle:
            bundleline = ""
            continue
        if ";" in bundle:
            bundlenames.append(bundle.split(";")[0].strip())
        else:
            bundlenames.append(bundle.strip())
        bundleline = ""
    return bundlenames


def open_manifest(path):
    mf = None
    if path.endswith("/META-INF/MANIFEST.MF"):
        mf = open(path, "rb")
    if zipfile.is_zipfile(path):
        # looks like "zipfile.is_zipfile()" is not reliable
        # see rhbz#889131 for more details
        try:
            jarfile = ZipFile(path)
            if "META-INF/MANIFEST.MF" in jarfile.namelist():
                mf = jarfile.open("META-INF/MANIFEST.MF", "rU")
        except IOError:
            pass
    if mf is None:
        return None
    content = mf.read()
    mf.close()
    return content.decode("utf-8")


def get_requires_from_manifest(manifest):
    reqs = []
    headers = parse_manifest(manifest)
    if headers.get("Require-Bundle"):
        for bundle in split_bundle_name(headers.get("Require-Bundle")):
            if bundle != "system.bundle":
                reqs.append(bundle)
    return reqs


def get_requires(path):
    reqs = []
    manifest = open_manifest(path)
    if manifest is None:
        return reqs
    reqs = get_requires_from_manifest(manifest)
    return reqs


def get_provides_from_manifest(manifest):
    symbolicName = None
    version = None
    for line in normalize_manifest(manifest):
        if line.startswith("Bundle-SymbolicName:"):
            symbolicName = line.split(':')[1].strip()
            symbolicName = symbolicName.split(";")[0].strip()
        if line.startswith("Bundle-Version:"):
            versions = line.split(':')[1].strip()
            versions = versions.split('.')[0:3]
            version = ".".join(versions)
    if symbolicName and version:
        return {symbolicName: version}
    return {}


def get_provides(path):
    provs = {}
    manifest = open_manifest(path)
    if manifest is None:
        return provs
    provs = get_provides_from_manifest(manifest)
    return provs


def find_possible_bundles(buildroot):
    """
    Search given path (typically buildroot) for JAR and MANIFEST files.
    """
    paths = []
    for dirpath, _, filenames in os.walk(buildroot):
        for filename in filenames:
            fpath = os.path.abspath(os.path.join(dirpath, filename))
            if _check_path(fpath):
                paths.append(fpath)
    return paths


def _check_path(path):
    if os.path.islink(path):
        return False
    if path.endswith(".jar"):
        return True
    if path.endswith("/MANIFEST.MF"):
        # who knows where the manifest can be in buildroot
        # TODO: improve this check somehow(?)
        # this is an attempt to identify only MANIFEST.MF files
        # which are in %{_datadir} or %{_prefix}/lib
        if "/usr/share/" in path or "/usr/lib" in path:
            return True
    return False


def read_provided_bundles_cache(cachedir):
    try:
        cachefile = open(os.path.join(cachedir, config.prov_bundles_cache_f), 'rb')
        provided = pickle.load(cachefile)
        cachefile.close()
    except IOError:
        return None
    return provided


def write_provided_bundles_cache(cachedir, provided):
    try:
        cachefile = open(os.path.join(cachedir, config.prov_bundles_cache_f), 'wb')
        pickle.dump(provided, cachefile)
        cachefile.close()
    except IOError:
        return None
    return provided


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
