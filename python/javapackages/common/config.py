#
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

import os
import json
from javapackages.common.exception import JavaPackagesToolsException

# name of the cache file for metadata
metadata_cache_f = "metadata.cache"
# name of the cache file for OSGi stuff
osgi_cache_f = "osgi.cache"


def get_config():
    """Return dictionary representing configuration file,
    None if no valid configuration was found.

    Paths specified in JAVACONFDIRS environment variable are searched for
    configuration file named 'javapackages-config.json'. Only first successfully
    read configuration file is taken into account, rest is ignored. Paths in
    JAVACONFDIRS are expected to be separated by 'os.pathsep'.

    If the JAVACONFDIRS is not defined, '/etc/java/' is assumed.
    """
    if "JAVACONFDIRS" in os.environ:
        config_paths = os.environ["JAVACONFDIRS"].split(os.pathsep)
    else:
        config_paths = ["/etc/java/"]

    for config_path in config_paths:
        try:
            file_path = os.path.join(config_path, "javapackages-config.json")
            with open(file_path) as config_file:
                return json.load(config_file)
        except (OSError, IOError):
            pass

    return None


def get_buildroot():
    """Return buildroot path, raise JavaPackagesToolsException if the path
    couldn't be determined.
    """
    try:
        buildroot = os.environ["RPM_BUILD_ROOT"]
    except KeyError:
        raise JavaPackagesToolsException("RPM_BUILD_ROOT environment "
                                         "variable is not set")
    return os.path.abspath(buildroot)
