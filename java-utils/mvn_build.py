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
# Authors:  Stanislav Ochotnicky <sochotnicky@redhat.com>

from __future__ import print_function

import base64
import gzip
import os
import optparse
import subprocess
import sys

from javapackages.maven.artifact import Artifact
from javapackages.xmvn.xmvn_config import XMvnConfig
from javapackages.common.util import command_exists
from javapackages.common.mock import socket_path as mock_socket


def goal_callback(option, opt_str, value, parser):
    assert value is None
    value = []

    for arg in parser.rargs:
        if arg[:2] == "--" and len(arg) > 2:
            break
        if arg[:1] == "-" and len(arg) > 1:
            break
        value.append(arg)

    del parser.rargs[:len(value)]
    setattr(parser.values, option.dest, value)

usage = "usage: %prog [options] [-- maven-arguments]"

if __name__ == "__main__":
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-b", "--bootstrap", action="store_true",
                      help="Enable bootstrap mode letting XMvn download artifacts online.")
    parser.add_option("-d", "--xmvn-debug", action="store_true",
                      help="Enable debugging output for maven local resolver.")
    parser.add_option("-E", "--disable-effective-poms",
                      action="store_true",
                      help="Disable resolution of effective POMs.")
    parser.add_option("-f", "--force", "--skip-tests",
                      action="store_true",
                      help="Skip test compilation and execution.")
    parser.add_option("-g", "--goal-before", "--pre",
                      dest="goal_before",
                      action="callback",
                      callback=goal_callback,
                      help="Run Maven goals before default XMvn goals.")
    parser.add_option("-G", "--goal-after", "--post",
                      dest="goal_after",
                      action="callback",
                      callback=goal_callback,
                      help="Run Maven goals after default XMvn goals.")
    parser.add_option("--gradle",
                      action="store_true",
                      help="Invoke Gradle instead of Maven.")
    parser.add_option("-i", "--skip-install",
                      action="store_true",
                      help="Skip artifact installation.")
    parser.add_option("-j", "--skip-javadoc",
                      action="store_true",
                      help="Skip javadoc generation and installation.")
    parser.add_option("-s", "--singleton",
                      action="store_true",
                      help="Singleton packaging (one artifact per package).")
    parser.add_option("-X", "--debug",
                      action="store_true",
                      help="Enable Maven debugging output (implies -d).")
    parser.add_option("--xmvn-javadoc",
                      action="store_true",
                      help="Use experimental XMvn javadoc MOJO to generate javadocs.")

    (options, args) = parser.parse_args()
    xc = XMvnConfig()

    if options.gradle:
        base_goal = "build"
        mvn_args = ["gradle-local", "--no-daemon"]
    else:
        base_goal = "verify"
        mvn_args = ["xmvn", "--batch-mode"]

    if not command_exists(mvn_args[0]):
        if options.gradle:
            print("gradle-local package is not installed, please install it to proceed", file=sys.stderr)
        else:
            # xmvn command is provided by xmvn package, but maven-local
            # pulls in bunch of maven plugins which may come handy
            print("maven-local package is not installed, please install it to proceed", file=sys.stderr)
        sys.exit(1)

    if not options.bootstrap:
        mvn_args.append("--offline")

    if options.disable_effective_poms:
        mvn_args.append("-Dxmvn.compat=20-rpmbuild-raw")

    if options.debug:
        mvn_args.append("--debug")

    if options.xmvn_debug or options.debug:
        mvn_args.append("-Dxmvn.debug")

    if options.force:
        mvn_args.append("-Dmaven.test.skip=true")
        xc.add_custom_option("buildSettings/skipTests", "true")
        if options.gradle:
            base_goal = "assemble"
        else:
            base_goal = "package"

    if mock_socket and os.path.exists(mock_socket):
        interpreter = sys.executable
        java_utils = os.path.dirname(os.path.abspath(__file__))
        cmd = "%s %s/request-artifact.py" % (interpreter, java_utils)
        mvn_args.append("-Dxmvn.resolver.requestArtifactCmd='%s'" % cmd)

    mvn_args.extend(args)

    if options.goal_before:
        mvn_args.extend(options.goal_before)

    mvn_args.append(base_goal)

    if not options.skip_install:
        if options.gradle:
            mvn_args.append("xmvnInstall")
        else:
            mvn_args.append("org.fedoraproject.xmvn:xmvn-mojo:install")

    if not options.skip_javadoc:
        if options.gradle:
            # Automatic javadoc generation for Gradle is not yet implemented in XMvn
            pass
        elif options.xmvn_javadoc:
            mvn_args.append("org.fedoraproject.xmvn:xmvn-mojo:javadoc")
        else:
            mvn_args.append("org.apache.maven.plugins:maven-javadoc-plugin:aggregate")

    if not options.gradle:
        # Build dependency generation for Gradle is not yet implemented in XMvn
        mvn_args.append("org.fedoraproject.xmvn:xmvn-mojo:builddep")

    if options.goal_after:
        mvn_args.extend(options.goal_after)

    if options.singleton:
        # make sure we don't install artifacts with non-empty classifiers
        xc.add_package_mapping(Artifact.from_mvn_str(":::*?:"), "__noinstall",
                               optional=True)
        xc.add_package_mapping(Artifact.from_mvn_str(":{*}"), "@1")

    print("Executing:", " ".join(mvn_args), file=sys.stderr)
    print(mvn_args, file=sys.stderr)
    sys.stderr.flush()
    p = subprocess.Popen(" ".join(mvn_args), shell=True, env=os.environ)
    p.wait()

    builddep_file = ".xmvn-builddep"
    if os.path.isfile(builddep_file):
        with open(builddep_file, "b") as file:
            contents = file.read()

        output = "\n".join([
            "-----BEGIN MAVEN BUILD DEPENDENCIES-----",
            base64.b64encode(gzip.compress(contents)).decode(),
            "-----END MAVEN BUILD DEPENDENCIES-----",
        ])

        print(output, flush=True)

    sys.exit(p.returncode)
