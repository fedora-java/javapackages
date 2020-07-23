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

import optparse
import sys

from javapackages.maven.artifact import (Artifact, ArtifactFormatException,
                                         ArtifactValidationException)
from javapackages.xmvn.xmvn_config import XMvnConfig, XMvnConfigException
from javapackages.common.exception import JavaPackagesToolsException


class SaneParser(optparse.OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

usage = "usage: %prog [options] <MVN spec> path [path ...]"
epilog = """
MVN spec:
Specification of Maven artifact in following format:

      groupId:artifactId[:extension[:classifier]][:version]

Wildcards (*) and empty parts in specifications are allowed (treated as wildcard).

Examples of valid specifications:
commons-lang:commons-lang:1.2
commons-lang:commons-lang:war:
commons-lang:commons-lang:war:test-jar:
commons-lang:commons-lang:war:test-jar:3.1
*:commons-lang (equivalent to ':commons-lang')
"""

if __name__ == "__main__":
    parser = SaneParser(usage=usage,
                        epilog=epilog)

    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.error("At least 2 arguments are required")

    try:
        orig = Artifact.from_mvn_str(args[0])
        orig.validate(allow_backref=False)
        XMvnConfig().add_file_mapping(orig, args[1:])
    except (ArtifactValidationException, ArtifactFormatException) as e:
        parser.error("{e}: Provided artifact strings were invalid. "
                     "Please see help  and check your arguments".format(e=e))
        sys.exit(1)
    except XMvnConfigException as e:
        parser.error("Incorrect configuration: {e}".format(e=e))
        sys.exit(1)
    except JavaPackagesToolsException as e:
        sys.exit(e)
