#!/usr/bin/python
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
import signal
import sys
import pyxb.utils.six as six
import subprocess
import logging
from javapackages.common.pypath import _parse_argv


def kill_parent_process():
    # mock may kill us immediately after rpmbuild dies, before output
    # is flushed. To avoid this race condiditon we must explicitly
    # flush any pending output before trying to kill parent.
    sys.stdout.flush()
    sys.stderr.flush()
    # rpmbuild ignores non-zero exit codes, but this is bad. Make sure
    # the build fails and doesn't silently ignore problems
    os.kill(os.getppid(), signal.SIGTERM)


def args_to_unicode(args):
    if six.PY2:
        for index, arg in enumerate(args):
            args[index] = arg.decode(sys.getfilesystemencoding())
    return args


def execute_command(command, input=None):
    proc = subprocess.Popen([command], shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = proc.communicate(input=input)
    proc.wait()
    return proc.returncode, stdout, stderr


def init_rpmgen(argv):
    _init_rpmgen_logging()
    return _parse_rpmgen_args(argv)


class _SkipPyXBWarningsFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith("Unable to convert DOM node")


def _init_rpmgen_logging():
    # Omit PyXB "Unable to convert DOM node to binding" warnings
    logger = logging.getLogger("pyxb.binding.basis")
    f = _SkipPyXBWarningsFilter()
    logger.addFilter(f)


def _parse_rpmgen_args(argv):
    options = _parse_argv(argv)[0]

    if not options.cachedir:
        raise Exception("Missing option: --cachedir")
    options.cachedir = _get_cachedir(options.cachedir)

    return options


def _get_cachedir(path, create_if_not_exists=True):
    cachedir_path = os.path.join(path, ".javapackages_cache")
    if not os.path.exists(cachedir_path) and create_if_not_exists:
        os.makedirs(cachedir_path)
    return cachedir_path


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s %(name)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
