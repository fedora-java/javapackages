#
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

from os.path import basename, dirname
import zipfile
from time import gmtime, strftime
from copy import deepcopy

from javapackages.maven.pom import POM
from javapackages.metadata.artifact import MetadataArtifact
from javapackages.metadata.alias import MetadataAlias
from javapackages.metadata.dependency import MetadataDependency
from javapackages.metadata.metadata import Metadata

from javapackages.common.exception import JavaPackagesToolsException


class PackagingTypeMissingFile(JavaPackagesToolsException):
    def __init__(self, pom_path):
        self.args=("Packaging type is not 'pom' and no artifact path has been provided for POM %s" % pom_path,)

class IncompatibleFilenames(JavaPackagesToolsException):
    def __init__(self, pom_path, jar_path):
        self.args=("Filenames of POM %s and JAR %s does not match properly. Check that JAR subdirectories matches '.' in pom name." % (pom_path, jar_path),)

class ExtensionsDontMatch(JavaPackagesToolsException):
    def __init__(self, coordinates_ext, file_ext):
        self.args=("Extensions don't match: '%s' != '%s'" % (coordinates_ext, file_ext),)

class MissingJarFile(JavaPackagesToolsException):
    def __init__(self):
        self.args=("JAR seems to be missing in standard directories. Make sure you have installed it",)

class UnknownFileExtension(JavaPackagesToolsException):
    def __init__(self, jar_path):
        self.args=("Unknown file extension: %s" % (jar_path),)


def _print_path_with_dirs(path, base):
    print(path)
    path = dirname(path)
    while path != base and path != '/':
        print("%dir " + path)
        path = dirname(path)


def _make_files_versioned(versions, pom_path, jar_path, pom_base, jar_base):
    """Make pom and jar file versioned"""
    versions = sorted(set(versions.split(',')))

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
            _print_path_with_dirs(dest, pom_base)
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
            _print_path_with_dirs(dest, jar_base)
        # remove unversioned jar
        os.remove(jar_path)

    # return paths to versioned, but regular files (not symlinks)
    return ret_pom_path, ret_jar_path

def _resolve_deps(pom):
    deps = []
    depm = []
    props = {}

    deps.extend([x for x in pom.dependencies])
    depm.extend([x for x in pom.dependencyManagement])
    props = pom.properties
    if pom.groupId:
        props["project.groupId"] = pom.groupId
    if pom.artifactId:
        props["project.artifactId"] = pom.artifactId
    if pom.version:
        props["project.version"] = pom.version

    for d in deps:
        d.interpolate(props)

    for dm in depm:
        dm.interpolate(props)

    # apply dependencyManagement on deps
    for d in deps:
        for dm in depm:
            if d.compare_to(dm):
                d.merge_with(dm)
                break

    # only deps with scope "compile" or "runtime" are interesting
    deps = [x for x in deps if x.scope in ["", "compile", "runtime"]]

    return deps

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
    properties = """#Generated by Java Packages Tools
version={a.version}
groupId={a.groupId}
artifactId={a.artifactId}
""".format(a=artifact)

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
    result = list()
    for a in aliases:
        alias = MetadataAlias.from_mvn_str(a)
        alias.extension = artifact.extension
        result.append(alias)

    artifact.aliases = result
    return artifact


def write_metadata(metadata_file, artifacts):
    if os.path.exists(metadata_file):
        metadata = Metadata.create_from_file(metadata_file)
    else:
        metadata = Metadata()

    # pylint:disable=E1103
    metadata.artifacts += deepcopy(artifacts)

    metadata.write_to_file(metadata_file)


def _main():
    usage="usage: %prog [options] metadata_path pom_path|<MVN spec> [jar_path]"
    parser = OptionParser(usage=usage)
    parser.add_option("-a","--append",type="str",
                      help="Additional depmaps to add (gid:aid)  [default: %default]")
    parser.add_option('-r', '--versions', type="str",
                      help='Additional versions to add for each depmap')
    parser.add_option('-n', '--namespace', type="str",
                      help='Namespace to use for generated fragments', default="")
    parser.add_option('--pom-base', type="str",
                      help='Base path under which POM files are installed', default="")
    parser.add_option('--jar-base', type="str",
                      help='Base path under which JAR files are installed', default="")

    parser.set_defaults(append=None)

    (options, args) = parser.parse_args()
    append_deps = options.append
    add_versions = options.versions
    namespace = options.namespace
    pom_base = options.pom_base
    jar_base = options.jar_base

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
            sys.exit("JAR file path must be specified when using artifact coordinates")


    # output file path for file lists
    print(metadata_path)

    artifact = add_compat_versions(artifact, add_versions)
    if add_versions:
        pom_path, jar_path = _make_files_versioned(add_versions, pom_path, jar_path, pom_base, jar_base)

    if namespace:
        artifact.namespace = namespace

    if have_pom:
        pom = POM(pom_path)
        if pom.parent or pom.packaging == "pom":
            artifact.properties["xmvn.resolver.disableEffectivePom"] = "true"
        else:
            deps = []
            for d in _resolve_deps(pom):
                deps.append(MetadataDependency.from_mvn_dependency(d))
            if deps:
                artifact.dependencies = set(deps)


    buildroot = os.environ.get('RPM_BUILD_ROOT')
    am = []
    if jar_path:
        metadata_jar_path = os.path.abspath(jar_path)
        artifact.path = metadata_jar_path.replace(buildroot, "") if buildroot else metadata_jar_path
        artifact = add_aliases(artifact, append_deps)
        if artifact.extension == "jar":
            artifact.extension = ""
        am.append(artifact.copy())
        # output file path for file list (if it's not versioned)
        if not add_versions:
            _print_path_with_dirs(jar_path, jar_base)
    if have_pom:
        metadata_pom_path = os.path.abspath(pom_path)
        artifact.path = metadata_pom_path.replace(buildroot, "") if buildroot else metadata_pom_path
        artifact.extension = "pom"
        artifact.aliases = None
        artifact = add_aliases(artifact, append_deps)
        am.append(artifact.copy())
        # output file path for file list (if it's not versioned)
        if not add_versions:
            _print_path_with_dirs(pom_path, pom_base)

    write_metadata(metadata_path, am)


if __name__ == "__main__":
    try:
        _main()
    except JavaPackagesToolsException as e:
        sys.exit(e)
