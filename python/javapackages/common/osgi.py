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

import os
import pickle
import zipfile
from zipfile import ZipFile

import javapackages.common.config as config
from javapackages.metadata.metadata import Metadata, MetadataInvalidException


def print_provides(provides):
    for key in provides.keys():
        print("osgi({name}) = {ver}".format(name=key,
                                            ver=provides[key]))


def normalize_manifest(manifest):
    lines = []
    for line in manifest.readlines():
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
    if path.endswith("META-INF/MANIFEST.MF"):
        return open(path)
    if zipfile.is_zipfile(path):
        # looks like "zipfile.is_zipfile()" is not reliable
        # see rhbz#889131 for more details
        try:
            jarfile = ZipFile(path)
            if "META-INF/MANIFEST.MF" in jarfile.namelist():
                return jarfile.open("META-INF/MANIFEST.MF")
        except IOError:
            pass
    return None


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
    manifest.close()
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
    return {symbolicName: version}


def get_provides(path):
    provs = {}
    manifest = open_manifest(path)
    if manifest is None:
        return provs
    provs = get_provides_from_manifest(manifest)
    manifest.close()
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
        # which are in %{_datadir} or %{_libdir}
        if "/usr/share/" in path or "/usr/lib" in path:
            return True
    return False


def read_provided_bundles_cache(cachedir):
    try:
        cachefile = open(os.path.join(cachedir, config.prov_bundles_cache_f), 'r')
        provided = pickle.load(cachefile)
        cachefile.close()
    except IOError:
        return None
    return provided


def write_provided_bundles_cache(cachedir, provided):
    try:
        cachefile = open(os.path.join(cachedir, config.prov_bundles_cache_f), 'w')
        pickle.dump(provided, cachefile)
        cachefile.close()
    except IOError:
        return None
    return provided


def check_path_in_metadata(path, cachedir_path):
    buildroot = config.get_buildroot()

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
        if a.path:
            if (os.path.abspath(a.path) == path or
               (path.startswith(os.path.abspath(a.path)) and
               os.path.realpath(buildroot + path))):
                return True
    return False
