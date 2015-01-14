#-
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
# Authors:  Michal Srb <msrb@redhat.com>

from javapackages.common.util import sanitize_version

class Printer(object):
    @staticmethod
    def get_mvn_str(gid, aid, ext="", cla="", ver=""):
        mvnstr = "{gid}:{aid}".format(gid=gid, aid=aid)

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

    @staticmethod
    def get_rpm_str(gid, aid, ext="", cla="", ver="", namespace="",
                    compat=None, pkgver=None):

        mvnstr = Printer.get_mvn_str(gid, aid, ext, cla,
                                     compat if compat is not None else "")
        rpmstr = "mvn({mvnstr})".format(mvnstr=mvnstr)

        if namespace:
            rpmstr = "{ns}-{rpmstr}".format(ns=namespace, rpmstr=rpmstr)

        if pkgver is not None:
            pkgver = sanitize_version(pkgver)
            rpmstr = "{rpmstr} = {ver}".format(rpmstr=rpmstr, ver=pkgver)

        return rpmstr
