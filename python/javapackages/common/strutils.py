#
# Copyright (c) 2015, Red Hat, Inc.
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
# Authors:  Michal Srb <msrb@redhat.com>


def get_mvn_str(gid, aid, ext=None, cla=None, ver=None):
    """Construct and return Maven coordinates.

    At least groupId (gid) and artifactId (aid) needs to be provided.

    >>> get_mvn_str("org.example", "artifact")
    'org.example:artifact'
    >>> get_mvn_str("org.example", "artifact", ver="1")
    'org.example:artifact:1'
    >>> get_mvn_str("org.example", "artifact", cla="test")
    'org.example:artifact::test:'
    """

    mvnstr = "{gid}:{aid}".format(gid=gid, aid=aid)

    # "jar" is a default extension in Maven world, we can omit it
    if ext == "jar":
        ext = ""

    if ext:
        mvnstr = mvnstr + ":{ext}".format(ext=ext)

    if cla:
        if not ext:
            mvnstr = mvnstr + ":"
        mvnstr = mvnstr + ":{cla}".format(cla=cla)

    if ver:
        mvnstr = mvnstr + ":{ver}".format(ver=ver)
    elif cla or ext:
        mvnstr = mvnstr + ":"

    return mvnstr


def get_rpm_str(gid, aid, ext=None, cla=None, namespace=None,
                compat_ver=None, pkg_ver=None):
    """Construct and return string representing RPM's "virtual provide"
    of a given Maven artifact.

    >>> get_rpm_str("org.example", "artifact")
    'mvn(org.example:artifact)'
    >>> get_rpm_str("org.example", "artifact", pkg_ver="1")
    'mvn(org.example:artifact) = 1'
    >>> get_rpm_str("org.example", "artifact", namespace="myns", compat_ver="1")
    'myns-mvn(org.example:artifact:1)'
    """

    mvnstr = get_mvn_str(gid, aid, ext=ext, cla=cla,
                         ver=compat_ver if compat_ver is not None else None)
    rpmstr = "mvn({mvnstr})".format(mvnstr=mvnstr)

    if namespace:
        rpmstr = "{ns}-".format(ns=namespace) + rpmstr

    if pkg_ver:
        pkg_ver = _sanitize_version(pkg_ver)
        rpmstr = rpmstr + " = {ver}".format(ver=pkg_ver)

    return rpmstr


def _sanitize_version(ver):
    """Sanitize version so it can be properly handled by YUM/DNF.

    RPM package managers seem to have a problem with versioned "Provides"
    containing dashes, e.g. "mvn(g:a) = 1.0-SNAPSHOT".

    >>> _sanitize_version("1.0-SNAPSHOT")
    '1.0.SNAPSHOT'
    >>> _sanitize_version("1.0")
    '1.0'
    """
    if ver:
        return ver.replace("-", ".")
    return ""


if __name__ == "__main__":
    import doctest
    doctest.testmod()
