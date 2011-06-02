#!/usr/bin/python
# Copyright (c) 2011 Red Hat, Inc
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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

class IncompatibleFilenames(Exception):
    def __init__(self):
        self.args=("Filenames of pom and jar does not match properly. Check that jar subdirectories match '.' in pom name.",)

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
                raise IncompatibleFilenames()
        else:
            jpp_gid = "JPP"
            jpp_aid = basename(jar_path)[:-4]
            # we assert that jar and pom parts match
            if not pomname == "JPP-%s.pom" % jpp_aid:
                raise IncompatibleFilenames()
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
        print "Unknown error while generating fragment. Send bugreport \
        to https://fedorahosted.org/javapackages/"
        sys.exit(1)
