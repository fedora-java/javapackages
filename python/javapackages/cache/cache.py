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

import os
import logging
import pickle
import javapackages.common.config as config


class Cache(object):
    def __init__(self, rpmconf):
        self._cachedir = rpmconf.cachedir
        self._rpm_pid = rpmconf.rpm_pid
        self._scl = rpmconf.scl

    def _process_buildroot(self):
        cache = {}
        # TODO: implement in subclass
        return cache

    def _find_paths(self):
        buildroot = config.get_buildroot()
        paths = []
        for dirpath, _, filenames in os.walk(buildroot):
            for filename in filenames:
                fpath = os.path.abspath(os.path.join(dirpath, filename))
                if self._check_path(fpath):
                    paths.append(fpath)
        return paths

    def _check_path(self, path):
        # TODO: implement in subclass
        return False

    def _read_cache(self):
        try:
            cachepath = os.path.join(self._cachedir, self._config_name)
            cachefile = open(cachepath, 'rb')
            cached_pid, cache = pickle.load(cachefile)
            cachefile.close()
            # check if the cache was most likely created during current build
            if cached_pid != self._rpm_pid:
                logging.warning("Cache in {path} is outdated, skipping"
                                .format(path=cachepath))
                return None
        except IOError:
            return None
        return cache

    def _write_cache(self, cache):
        try:
            cachefile = open(os.path.join(self._cachedir,
                                          self._config_name), 'wb')
            content = (self._rpm_pid, cache)
            pickle.dump(content, cachefile)
            cachefile.close()
        except IOError:
            return None
        return cache
