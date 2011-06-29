#!/usr/bin/python
# Copyright (c) 2011, Red Hat, Inc
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# * Neither the name of the <ORGANIZATION> nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Stanislav Ochotnicky <sochotnicky@redhat.com>
#
# this script is used by add_maven_depmap rpm macro to generate
# mapping between maven groupId:artifactId and jar file in our local
# filesystem (i.e. %{_javadir})
# rpm macro expects to find this file as %{_datadir}/java-utils/maven_depmap.py

from optparse import OptionParser
import sys
import re
import xml.dom.minidom as minidom
from os.path import basename, dirname

class Fragment:
    """simple structure to hold fragment information"""
    def __init__(self, gid, aid, version, local_gid, local_aid):
        self.gid = gid
        self.aid = aid
        self.version = version
        self.local_gid = local_gid
        self.local_aid = local_aid

class PackagingTypeMissingFile(Exception):
    def __init__(self, pom_path):
        self.args=("Packaging type is not 'pom' and no artifact path has been provided for pom %s" % pom_path,)

class IncompatibleFilenames(Exception):
    def __init__(self, pom_path, jar_path):
        self.args=("Filenames of pom %s and jar %s does not match properly. Check that jar subdirectories match '.' in pom name." % (pom_path, jar_path),)

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
    pomname = basename(pom_path)
    if jar_path:
        if pomname[3] == '.':
            jpp_gid = "JPP/%s" % basename(dirname(jar_path))
            jpp_aid = basename(jar_path)[:-4]
            # we assert that jar and pom parts match
            if not pomname == "JPP.%s-%s.pom" % (jpp_gid[4:], jpp_aid):
                raise IncompatibleFilenames(pom_path, jar_path)
        else:
            jpp_gid = "JPP"
            jpp_aid = basename(jar_path)[:-4]
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

    if not proj_aid:
        return None

    jpp_gid, jpp_aid = _get_jpp_from_filename(pom_file, jar_file)

    if proj_version and proj_gid:
        return Fragment(proj_gid.firstChild.nodeValue,
            proj_aid.firstChild.nodeValue,
            proj_version.firstChild.nodeValue,
            jpp_gid,
            jpp_aid
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
         jpp_aid
    )

def output_fragment(fragment_path, fragment, additions = None):
    """Writes fragment into fragment_path in specialised format
    compatible with jpp"""

    maps = [(fragment.gid, fragment.aid)]
    if additions:
        adds = additions.split(',')
        for add in adds:
            g, a = add.strip().split(':')
            maps.append((g, a))

    with open(fragment_path, "aw") as ffile:
        for m in maps:
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
""" % (m[0], m[1], fragment.version, fragment.local_gid,
       fragment.local_aid, fragment.version) )


if __name__ == "__main__":

    usage="usage: %prog [options] fragment_path pom_path [jar_path]"
    parser = OptionParser(usage=usage)
    parser.add_option("-a","--append",type="str",help="Additional depmaps to add (gid:aid)  [default: %default]")


    parser.set_defaults(append=None)

    (options, args) = parser.parse_args()
    append_deps = options.append

    if len(args) < 2:
        parser.error("Incorrect number of arguments")
    # these will fail when incorrect number of arguments is given
    fragment_path = args[0].strip()
    pom_path = args[1].strip()
    if len(args) == 3:
        jar_path = args[2].strip()
        fragment = parse_pom(pom_path, jar_path)
    else:
        fragment = parse_pom(pom_path)

    if fragment:
        output_fragment(fragment_path, fragment, append_deps)
    else:
        print "Problem parsing pom file. Is it valid maven pom? Send bugreport \
        to https://fedorahosted.org/javapackages/ and attach %s to \
        this bugreport" % pom_path
        sys.exit(1)
