#-
# Copyright (c) 2014, Red Hat, Inc.
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
# Authors: Stanislav Ochotnicky <sochotnicky@redhat.com>
#
# this script is used by add_maven_depmap rpm macro to generate
# mapping between maven groupId:artifactId and jar file in our local
# filesystem (i.e. %{_javadir})
# rpm macro expects to find this file as %{_javadir}-utils/maven_depmap.py


from optparse import OptionParser
import os
import shutil
import sys
import gzip

from os.path import basename
import zipfile
from time import gmtime, strftime

from javapackages.maven.pom import POM
from javapackages.metadata.artifact import MetadataArtifact
from javapackages.metadata.alias import MetadataAlias

import javapackages.metadata.pyxbmetadata as m
import pyxb


class PackagingTypeMissingFile(Exception):
    def __init__(self, pom_path):
        self.args=("Packaging type is not 'pom' and no artifact path has been provided for POM %s" % pom_path,)

class IncompatibleFilenames(Exception):
    def __init__(self, pom_path, jar_path):
        self.args=("Filenames of POM %s and JAR %s does not match properly. Check that JAR subdirectories matches '.' in pom name." % (pom_path, jar_path),)

class ExtensionsDontMatch(Exception):
    def __init__(self, coordinates_ext, file_ext):
        self.args=("Extensions don't match: '%s' != '%s'" % (coordinates_ext, file_ext),)

class MissingJarFile(Exception):
    def __init__(self):
        self.args=("JAR seems to be missing in standard directories. Make sure you have installed it",)

class UnknownFileExtension(Exception):
    def __init__(self, jar_path):
        self.args=("Unknown file extension: %s" % (jar_path),)


def _make_files_versioned(versions, pom_path, jar_path):
    """Make pom and jar file versioned"""
    versions = list(set(versions.split(',')))

    vpom_path = pom_path
    vjar_path = jar_path

    ret_pom_path = pom_path
    ret_jar_path = jar_path

    # pom
    if ':' not in vpom_path:
        root, ext = os.path.splitext(vpom_path)
        symlink = False
        for ver in sorted(versions):
            dest = "%s-%s%s" % (root, ver, ext)
            if not symlink:
                shutil.copy(os.path.realpath(vpom_path), dest)
                symlink = True
                vpom_path = dest
                ret_pom_path = dest
            else:
                os.symlink(basename(vpom_path), dest)
            # output file path for file lists
            print(dest)
        # remove unversioned pom
        os.remove(pom_path)

    # jar
    if vjar_path:
        root, ext = os.path.splitext(vjar_path)
        symlink = False
        for ver in sorted(versions):
            dest = "%s-%s%s" % (root, ver, ext)
            if not symlink:
                shutil.copy(os.path.realpath(vjar_path), dest)
                symlink = True
                vjar_path = dest
                ret_jar_path = dest
            else:
                os.symlink(basename(vjar_path), dest)
            # output file path for file lists
            print(dest)
        # remove unversioned jar
        os.remove(jar_path)

    # return paths to versioned, but regular files (not symlinks)
    return ret_pom_path, ret_jar_path


# Add a file to a ZIP archive (or JAR, WAR, ...) unless the file
# already exists in the archive.  Provided by Tomas Radej.
def append_if_missing(archive_name, file_name, file_contents):
    archive = zipfile.ZipFile(archive_name, 'a')
    try:
        if file_name not in archive.namelist():
            archive.writestr(file_name, file_contents)
    finally:
        archive.close()


# Inject pom.properties if JAR doesn't have one.  This is necessary to
# identify the origin of JAR files that are present in the repository.
def inject_pom_properties(jar_path, artifact):
    if not zipfile.is_zipfile(jar_path):
        return
    props_path = "META-INF/maven/{a.groupId}/{a.artifactId}/pom.properties".format(a=artifact)
    timestamp = strftime("%a %b %d %H:%M:%S UTC %Y", gmtime())
    properties = """#Generated by Java Packages Tools
#{timestamp}
version={a.version}
groupId={a.groupId}
artifactId={a.artifactId}
""".format(timestamp=timestamp,
           a=artifact)

    if artifact.extension:
        properties = properties + \
            "extension={ext}\n".format(ext=artifact.extension)
    if artifact.classifier:
        properties = properties + \
            "classifier={clas}\n".format(clas=artifact.classifier)

    append_if_missing(jar_path, props_path, properties)


def add_compat_versions(artifact, versions):
    if not versions:
        return artifact

    artifact.compatVersions = versions.split(',')
    return artifact


def add_aliases(artifact, additions):
    if not additions:
        return artifact

    aliases = additions.split(',')
    result = set()
    for a in aliases:
        alias = MetadataAlias.from_mvn_str(a)
        alias.extension = artifact.extension
        result.add(alias)

    artifact.aliases = result
    return artifact


def write_metadata(metadata_file, artifacts):
    if os.path.exists(metadata_file):
        try:
            xml = gzip.open(metadata_file, 'rb').read()
        except IOError:
            # Not a gzipped file?
            xml = open(metadata_file, "r").read()
        root = m.CreateFromDocument(xml)
        artifacts += [a for a in root.artifacts.artifact]
    else:
        root = m.metadata()

    root.artifacts = pyxb.BIND(*artifacts)

    with open(metadata_file, 'w') as f:
        dom = root.toDOM(None)
        f.write(dom.toprettyxml(indent="   "))

if __name__ == "__main__":

    usage="usage: %prog [options] metadata_path pom_path|<MVN spec> [jar_path]"
    parser = OptionParser(usage=usage)
    parser.add_option("-a","--append",type="str",
                      help="Additional depmaps to add (gid:aid)  [default: %default]")
    parser.add_option('-r', '--versions', type="str",
                      help='Additional versions to add for each depmap')
    parser.add_option('-n', '--namespace', type="str",
                      help='Namespace to use for generated fragments', default="")

    parser.set_defaults(append=None)

    (options, args) = parser.parse_args()
    append_deps = options.append
    add_versions = options.versions
    namespace = options.namespace

    if len(args) < 2:
        parser.error("Incorrect number of arguments")
    # These will fail when incorrect number of arguments is given.
    metadata_path = args[0].strip()
    pom_path = args[1].strip()
    jar_path = None

    artifact = None
    have_pom = False

    if len(args) == 3:
        jar_path = args[2].strip()
        local = None
        fragment = None
        if ':' in pom_path:
            pom_str = pom_path.rsplit('/')[-1]
            artifact = MetadataArtifact.from_mvn_str(pom_str)
            artifact_ext = artifact.extension or "jar"
            file_ext = os.path.splitext(jar_path)[1][1:]
            if artifact_ext != file_ext:
                raise ExtensionsDontMatch(artifact_ext, file_ext)

            if artifact.extension == 'jar':
                artifact.extension = ''

            if not artifact.version:
                parser.error("Artifact definition has to include version")
        else:
            artifact = MetadataArtifact.from_pom(pom_path)
            ext = os.path.splitext(jar_path)[1][1:]
            if ext != "jar":
                artifact.extension = ext
            have_pom = True
        if artifact:
            inject_pom_properties(jar_path, artifact)
    else:
        # looks like POM only artifact
        if ':' not in pom_path:
            artifact = MetadataArtifact.from_pom(pom_path)
            have_pom = True

            if POM(pom_path).packaging != "pom":
                raise PackagingTypeMissingFile(pom_path)
        else:
            print("JAR file path must be specified when using artifact coordinates")
            sys.exit(1)


    # output file path for file lists
    print(metadata_path)

    artifact = add_compat_versions(artifact, add_versions)
    if add_versions:
        pom_path, jar_path = _make_files_versioned(add_versions, pom_path, jar_path)

    if namespace:
        artifact.namespace = namespace

    artifact.properties["xmvn.resolver.disableEffectivePom"] = "true"


    buildroot = os.environ.get('RPM_BUILD_ROOT')
    am = []
    if jar_path:
        metadata_jar_path = os.path.abspath(jar_path)
        artifact.path = metadata_jar_path.replace(buildroot, "") if buildroot else metadata_jar_path
        artifact = add_aliases(artifact, append_deps)
        if artifact.extension == "jar":
            artifact.extension = ""
        am.append(artifact.to_metadata())
        # output file path for file list (if it's not versioned)
        if not add_versions:
            print(jar_path)
    if have_pom:
        metadata_pom_path = os.path.abspath(pom_path)
        artifact.path = metadata_pom_path.replace(buildroot, "") if buildroot else metadata_pom_path
        artifact.extension = "pom"
        artifact.aliases = None
        artifact = add_aliases(artifact, append_deps)
        am.append(artifact.to_metadata())
        # output file path for file list (if it's not versioned)
        if not add_versions:
            print(pom_path)

    write_metadata(metadata_path, am)
