#!/usr/bin/python
# Copyright (c) 2012, Red Hat, Inc
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
import xml.dom.minidom as minidom
from os.path import basename, dirname

class Fragment:
    """simple structure to hold fragment information"""
    def __init__(self, gid, aid, version, local_gid, local_aid, packaging):
        self.gid = gid.strip()
        self.aid = aid.strip()
        self.version = version.strip()
        self.local_gid = local_gid
        self.local_aid = local_aid
        self.packaging = packaging


class PackagingTypeMissingFile(Exception):
    def __init__(self, pom_path):
        self.args=("Packaging type is not 'pom' and no artifact path has been provided for pom %s" % pom_path,)

class IncompatibleFilenames(Exception):
    def __init__(self, pom_path, jar_path):
        self.args=("Filenames of pom %s and jar %s does not match properly. Check that jar subdirectories match '.' in pom name." % (pom_path, jar_path),)

class MissingJarFile(Exception):
    def __init__(self):
        self.args=("Jar seems to be missing in standard directories. Make sure you have installed it")

def _get_tag_under_parent(dom, parent, tag):
    """get first xml tag under parent tag within dom"""
    tags = dom.getElementsByTagName(tag)
    for t in tags:
        if t.parentNode == parent:
            return t
    return None

def _get_jpp_from_filename(pom_path, jar_path = None):
    """Get resolved (groupId,artifactId) tuple from pom and jar path

    pom name and jar name have to be compatible.
    JPP.xbean-xbean-main.pom means groupId is "JPP/xbean" and artifactid
    is "xbean-main". Therefore for jar name to be compatible it has be
    in %{_javadir}/xbean/xbean-main.jar
    """
    # this is not nice, because macros can change but handling these
    # in rpm macros is ugly as hell
    javadirs=["/usr/share/java", "/usr/share/java-jni", "/usr/lib/java",
              "/usr/lib64/java"]
    pomname = basename(pom_path)
    if jar_path:
        if not os.path.isfile(jar_path):
            raise IOError("Jar path doesn't exist")
        jarpart = None
        for jdir in javadirs:
            if jdir in jar_path:
                javadir_re = re.compile(".*%s/" % jdir)
                jarpart = re.sub(javadir_re, "", jar_path)
        if not jarpart:
            raise MissingJarFile()

        if pomname[3] == '.':
            if '/' not in jarpart:
                raise IncompatibleFilenames(pom_path, jar_path)
            jpp_gid = "JPP/%s" % dirname(jarpart)
            jpp_aid = basename(jarpart)[:-4]
            # we assert that jar and pom parts match
            if not pomname == "JPP.%s-%s.pom" % (jpp_gid[4:], jpp_aid):
                raise IncompatibleFilenames(pom_path, jar_path)
        else:
            if '/' in jarpart:
                raise IncompatibleFilenames(pom_path, jar_path)
            jpp_gid = "JPP"
            jpp_aid = basename(jarpart)[:-4]
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

def parse_pom(pom_file, jar_file = None):
    """Returns Fragment class or None if pom file is invalid"""
    dom = minidom.parse(pom_file)

    projects = dom.getElementsByTagName('project')
    if len(projects) != 1:
        return None

    project = projects[0]
    proj_packaging = _get_tag_under_parent(dom, project, 'packaging')
    # if project packaging is undefined => jar
    # only "pom" packaging type can be without jar_file path otherwise
    # we bail
    if not jar_file:
        if not proj_packaging or proj_packaging.firstChild.nodeValue != "pom":
            raise PackagingTypeMissingFile(pom_path)

    proj_version = _get_tag_under_parent(dom, project, 'version')
    proj_gid = _get_tag_under_parent(dom, project, 'groupId')
    proj_aid = _get_tag_under_parent(dom, project, 'artifactId')
    if not proj_packaging:
        proj_packaging = 'jar'
    else:
        proj_packaging = proj_packaging.firstChild.nodeValue


    if not proj_aid:
        return None

    jpp_gid, jpp_aid = _get_jpp_from_filename(pom_file, jar_file)

    if proj_version and proj_gid:
        return Fragment(proj_gid.firstChild.nodeValue,
            proj_aid.firstChild.nodeValue,
            proj_version.firstChild.nodeValue,
            jpp_gid,
            jpp_aid,
            proj_packaging
            )

    parent = _get_tag_under_parent(dom, project, 'parent')
    if not parent:
        return None

    pgid = _get_tag_under_parent(dom, parent, 'groupId')
    if not proj_gid:
        proj_gid = pgid

    pversion = _get_tag_under_parent(dom, parent, 'version')
    if not proj_version:
        proj_version = pversion

    return Fragment(proj_gid.firstChild.nodeValue,
         proj_aid.firstChild.nodeValue,
         proj_version.firstChild.nodeValue,
         jpp_gid,
         jpp_aid,
         proj_packaging
    )

def create_mappings(fragment, additions = None):
    maps = [(fragment.gid, fragment.aid)]
    if additions:
        adds = additions.split(',')
        for add in adds:
            g, a = add.strip().split(':')
            maps.append((g, a))
    return maps

def output_fragment(fragment_path, fragment, mappings):
    """Writes fragment into fragment_path in specialised format
    compatible with jpp"""
    with open(fragment_path, "aw") as ffile:
        for m in mappings:
            gid, aid = m
            ffile.write("""
<dependency>
    <maven>
        <groupId>%s</groupId>
        <artifactId>%s</artifactId>
        <version>%s</version>
    </maven>
    <jpp>
        <groupId>%s</groupId>
        <artifactId>%s</artifactId>
        <version>%s</version>
    </jpp>
</dependency>
""" % (gid, aid, fragment.version, fragment.local_gid,
       fragment.local_aid, fragment.version) )


def create_maven_repo(repo_path, fragment, mappings):
    """Create maven repository layout from fragment in given repository"""

    # subdirectory under _javadir (if any)
    javadir_sub = fragment.local_gid.replace('JPP', '')
    for m in mappings:
        gid, aid = m
        repo_subdir = os.path.join(gid.replace('.', os.path.sep),
                                   aid,
                                   fragment.version)

        final_dir = os.path.join(repo_path,
                                 repo_subdir)
        # create directory structure first
        os.makedirs(final_dir)
        print final_dir

        # we want relative paths for symlinks so we need to know how many levels
        # deep we are in the repository
        gid_dircount = gid.count('.')
        relative_datadir = '..%s' % os.path.sep * (gid_dircount+4)

        os.symlink(os.path.join(relative_datadir,
                                'java',
                                javadir_sub,
                                "%s.%s" % (fragment.local_aid, fragment.packaging)),
                   os.path.join(final_dir,
                                "%s-%s.%s" % (aid,
                                              fragment.version,
                                              fragment.packaging)))
        pom_fname = "JPP"
        if javadir_sub != '':
            pom_fname = "%s.%s" % (pom_fname, javadir_sub)
        pom_fname = "%s-%s.pom" % (pom_fname, fragment.local_aid)
        os.symlink(os.path.join(relative_datadir, 'maven-poms', pom_fname),
                   os.path.join(final_dir,
                                "%s-%s.pom" % (aid,
                                               fragment.version)))

if __name__ == "__main__":

    usage="usage: %prog [options] fragment_path pom_path [jar_path]"
    parser = OptionParser(usage=usage)
    parser.add_option("-a","--append",type="str",
                      help="Additional depmaps to add (gid:aid)  [default: %default]")
    parser.add_option('-m', '--maven-repo', type="str", dest='maven_repo',
                      help='Where to create Maven repository layout')


    parser.set_defaults(append=None)

    (options, args) = parser.parse_args()
    append_deps = options.append

    if len(args) < 2:
        parser.error("Incorrect number of arguments")
    # these will fail when incorrect number of arguments is given
    fragment_path = args[0].strip()
    pom_path = args[1].strip()
    print fragment_path
    print pom_path
    if len(args) == 3:
        jar_path = args[2].strip()
        print jar_path
        fragment = parse_pom(pom_path, jar_path)
    else:
        fragment = parse_pom(pom_path)

    if fragment:
        mappings = create_mappings(fragment, append_deps)
        output_fragment(fragment_path, fragment, mappings)
        if options.maven_repo:
            create_maven_repo(options.maven_repo, fragment, mappings)
    else:
        print "Problem parsing pom file. Is it valid maven pom? Send bugreport \
        to https://fedorahosted.org/javapackages/ and attach %s to \
        this bugreport" % pom_path
        sys.exit(1)
