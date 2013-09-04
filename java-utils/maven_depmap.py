#!/usr/bin/python
# Copyright (c) 2012-2013, Red Hat, Inc
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
# rpm macro expects to find this file as %{_datadir}/java-utils/maven_depmap.py

from optparse import OptionParser
import sys
import os
import re
from StringIO import StringIO
import xml.dom.minidom
import codecs

from os.path import basename, dirname, splitext
from zipfile import ZipFile
from time import gmtime, strftime

from lxml.etree import SubElement, Element, ElementTree, XMLParser

from javapackages import POM, Artifact


class Fragment:
    """simple structure to hold fragment information"""
    def __init__(self, upstream_artifact, local_artifact):
        self.upstream_artifact = upstream_artifact
        self.local_artifact = local_artifact

    def __getitem__(self, index):
        return self.__dict__[index]


class PackagingTypeMissingFile(Exception):
    def __init__(self, pom_path):
        self.args=("Packaging type is not 'pom' and no artifact path has been provided for POM %s" % pom_path,)

class IncompatibleFilenames(Exception):
    def __init__(self, pom_path, jar_path):
        self.args=("Filenames of POM %s and JAR %s does not match properly. Check that JAR subdirectories matches '.' in pom name." % (pom_path, jar_path),)

class MissingJarFile(Exception):
    def __init__(self):
        self.args=("JAR seems to be missing in standard directories. Make sure you have installed it",)

def _get_javadir_part(jar_path):
    # This is not nice, because macros can change but handling these
    # in RPM macros is ugly as hell.
    javadirs=["/usr/share/java", "/usr/share/java-jni", "/usr/lib/java",
              "/usr/lib64/java"]

    jarpart = None
    for jdir in javadirs:
        if jdir in jar_path:
            javadir_re = re.compile(".*%s/" % jdir)
            jarpart = re.sub(javadir_re, "", jar_path)
    if not jarpart:
        raise MissingJarFile()
    return jarpart

def _get_jpp_from_filename(pom_path, jar_path = None):
    """Get resolved (groupId,artifactId) tuple from POM and JAR path.

    POM name and JAR name have to be compatible.
    JPP.xbean-xbean-main.pom means groupId is "JPP/xbean" and artifactId
    is "xbean-main". Therefore for JAR name to be compatible it has be
    in %{_javadir}/xbean/xbean-main.jar.
    """
    pomname = basename(pom_path)
    if jar_path:
        if not os.path.isfile(jar_path):
            raise IOError("JAR path doesn't exist")
        jarpart = _get_javadir_part(jar_path)

        if pomname[3] == '.':
            if '/' not in jarpart:
                raise IncompatibleFilenames(pom_path, jar_path)
            jpp_gid = "JPP/%s" % dirname(jarpart)
            jpp_aid = splitext(basename(jarpart))[0]
            # we assert that jar and pom parts match
            if not pomname == "JPP.%s-%s.pom" % (jpp_gid[4:], jpp_aid):
                raise IncompatibleFilenames(pom_path, jar_path)
        else:
            if '/' in jarpart:
                raise IncompatibleFilenames(pom_path, jar_path)
            jpp_gid = "JPP"
            jpp_aid = splitext(basename(jarpart))[0]
            # we assert that jar and pom parts match
            if not pomname == "JPP-%s.pom" % jpp_aid:
                raise IncompatibleFilenames(pom_path, jar_path)
    else:
        if pomname[3] == ".":
            match = re.match('JPP\.([^-]*?)-.*', pomname)
            jpp_gid="JPP/%s" % match.group(1)
            match = re.match('JPP\.[^-]*?-(.*)\.pom', pomname)
            jpp_aid= match.group(1)
        else:
            jpp_gid = "JPP"
            jpp_aid = pomname[4:-4]
    return(jpp_gid, jpp_aid)


def get_local_artifact(upstream_artifact, jar_path=None):
    if not jar_path:
        # does this even make sense? There is no pom, no dependencies...
        return Artifact("JPP", upstream_artifact.artifactId,
                        upstream_artifact.extension,
                        upstream_artifact.classifier,
                        upstream_artifact.version)

    jarpart = _get_javadir_part(jar_path)
    local_gid = "JPP"
    fname, ext = splitext(basename(jarpart))

    if upstream_artifact.extension:
        if ext[1:] != upstream_artifact.extension:
            raise IncompatibleFilenames(str(upstream_artifact), jar_path)
    else:
        if ext[1:] != "jar":
            raise IncompatibleFilenames(str(upstream_artifact), jar_path)

    local_aid = fname
    if upstream_artifact.classifier:
        local_aid = fname[:fname.rfind('-')]
        if fname[fname.rfind('-')+1:] != upstream_artifact.classifier:
            raise IncompatibleFilenames(str(upstream_artifact), jar_path)
    if '/' in jarpart:
        local_gid = "JPP/{gid}".format(gid=dirname(jarpart))

    return Artifact(local_gid, local_aid, upstream_artifact.extension,
                    upstream_artifact.classifier, upstream_artifact.version)


def parse_pom(pom_file, jar_file = None):
    """Returns Fragment class or None if POM file is invalid"""
    pom = POM(pom_file)

    # if project packaging is undefined => jar
    # only "pom" packaging type can be without jar_file path otherwise
    # we bail
    if not jar_file:
        if not pom.packaging or pom.packaging != "pom":
            raise PackagingTypeMissingFile(pom_path)

    jpp_gid, jpp_aid = _get_jpp_from_filename(pom_file, jar_file)

    upstream_artifact = Artifact(pom.groupId, pom.artifactId, version=pom.version)
    local_artifact = Artifact(jpp_gid, jpp_aid)
    return Fragment(upstream_artifact, local_artifact)

def create_mappings(fragment, additions = None):
    maps = [fragment]
    if additions:
        adds = additions.split(',')
        for add in adds:
            maps.append(Fragment(Artifact.from_mvn_str(add), fragment.local_artifact))
    return maps

def prettify_element(elem):
    xmlbuf = StringIO()
    et = ElementTree()
    et._setroot(elem)
    et.write(xmlbuf,
             xml_declaration=True,
             encoding = 'utf-8',
             method = "xml")
    return xml.dom.minidom.parseString(xmlbuf.getvalue()).toprettyxml()

def output_fragment(fragment_path, fragment, mappings, add_versions):
    """Writes fragment into fragment_path in specialised format
    compatible with jpp"""
    root = None
    try:
        et = ElementTree()
        parser = XMLParser(remove_blank_text=True)
        root = et.parse(fragment_path, parser=parser)
    except IOError:
        root = Element("dependencyMap")

    if not add_versions:
        versions = []
    else:
        versions = add_versions.split(',')

    if add_versions or add_versions == "":
        # skip RPM provides in compat packages
        SubElement(root, "skipProvides")

    versions.insert(0, fragment.upstream_artifact.version)
    for ver in versions:
        for fragment in mappings:
            dep = SubElement(root, "dependency")
            if add_versions or add_versions == "":
                fragment.local_artifact.version = ver
            else:
                fragment.local_artifact.version = ""
            mvn_xml = fragment.upstream_artifact.get_xml_element(root="maven")
            local_xml = fragment.local_artifact.get_xml_element(root="jpp")

            dep.append(mvn_xml)
            dep.append(local_xml)
    xmlstr = prettify_element(root)
    with codecs.open(fragment_path, 'w', "utf-8") as fout:
        fout.write(xmlstr)



# Add a file to a ZIP archive (or JAR, WAR, ...) unless the file
# already exists in the archive.  Provided by Tomas Radej.
def append_if_missing(archive_name, file_name, file_contents):
    with ZipFile(archive_name, 'a') as archive:
        if file_name not in archive.namelist():
            archive.writestr(file_name, file_contents)

# Inject pom.properties if JAR doesn't have one.  This is necessary to
# identify the origin of JAR files that are present in the repository.
def inject_pom_properties(jar_path, fragment):
    props_path = "META-INF/maven/{f.groupId}/{f.artifactId}/pom.properties".format(f=fragment.upstream_artifact)
    timestamp = strftime("%a %b %d %H:%M:%S UTC %Y", gmtime())
    properties = """#Generated by Java Packages Tools
#{timestamp}
version={f.upstream_artifact.version}
groupId={f.upstream_artifact.groupId}
artifactId={f.upstream_artifact.artifactId}""".format(timestamp=timestamp,
                                                      f=fragment)
    append_if_missing(jar_path, props_path, properties)

if __name__ == "__main__":

    usage="usage: %prog [options] fragment_path pom_path [jar_path]"
    parser = OptionParser(usage=usage)
    parser.add_option("-a","--append",type="str",
                      help="Additional depmaps to add (gid:aid)  [default: %default]")
    parser.add_option('-r', '--versions', type="str",
                      help='Additional versions to add for each depmap')




    parser.set_defaults(append=None)

    (options, args) = parser.parse_args()
    append_deps = options.append
    add_versions = options.versions

    if len(args) < 2:
        parser.error("Incorrect number of arguments")
    # These will fail when incorrect number of arguments is given.
    fragment_path = args[0].strip()
    pom_path = args[1].strip()
    if len(args) == 3:
        jar_path = args[2].strip()
        local = None
        fragment = None
        if ':' in pom_path:
            upstream = Artifact.from_mvn_str(pom_path)
            if upstream.extension == 'jar':
                upstream.extension = ''
            if not upstream.version:
                print "Artifact definition has to include version"
                sys.exit(1)
            local = get_local_artifact(upstream, jar_path)
            fragment = Fragment(upstream, local)
        else:
            fragment = parse_pom(pom_path, jar_path)
        if fragment:
            inject_pom_properties(jar_path, fragment)
    else:
        fragment = parse_pom(pom_path)

    if fragment:
        mappings = create_mappings(fragment, append_deps)
        output_fragment(fragment_path, fragment, mappings, add_versions)
    else:
        print "Problem parsing POM file. Is it valid maven POM? Send bugreport \
        to https://fedorahosted.org/javapackages/ and attach %s to \
        this bugreport" % pom_path
        sys.exit(1)
