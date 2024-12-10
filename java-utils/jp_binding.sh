#!/bin/sh
# Copyright (c) 2024, Red Hat, Inc.
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
# Authors:  Mikolaj Izdebski <mizdebsk@redhat.com>

set -eu
jpbindingdir="@{jpbindingdir}"

if [ -z "${RPM_BUILD_ROOT:-}" ]; then
    echo RPM_BUILD_ROOT env variable has not been set >&2
    exit 1
fi
if [ -z "${RPM_SPECPARTS_DIR:-}" ]; then
    echo RPM_SPECPARTS_DIR env variable has not been set >&2
    exit 1
fi

rpmname=""
basepkg=""
pkg=""
ghost=""
target=""
variant=""
provides=""
requires=""
recommends=""
with_meta_requires=true
description=""
with_description=true
summary=""
with_summary=true
with_files=true
with_package=true
with_install=true
verbose=false

while [ $# -gt 0 ]; do
    case "$1" in
        --rpm-name)
            rpmname="$2"
            shift
            ;;
        --base-pkg)
            basepkg="$2"
            shift
            ;;
        --binding-pkg)
            pkg="$2"
            shift
            ;;
        --ghost)
            ghost="$2"
            shift
            ;;
        --target)
            target="$2"
            shift
            ;;
        --variant)
            variant="$2"
            shift
            ;;
        --provides)
            provides="${provides}
Provides: $2"
            shift
            ;;
        --requires)
            requires="${requires}
Requires: $2"
            shift
            ;;
        --recommends)
            recommends="${recommends}
Recommends: $2"
            shift
            ;;
        --no-meta-requires)
            with_meta_requires=false
            ;;
        --description)
            description="$2"
            shift
            ;;
        --no-description)
            with_description=false
            ;;
        --summary)
            summary="$2"
            shift
            ;;
        --no-summary)
            with_summary=false
            ;;
        --no-files)
            with_files=false
            ;;
        --no-package)
            with_package=false
            ;;
        --no-install)
            with_install=false
            ;;
        --verbose)
            verbose=true
            ;;
        *)
            echo "Unknown option $1" >&2
            exit 1
    esac
    shift
done

debug()
{
    if ${verbose}; then
        echo "$@" >&2
    fi
}

if [ -z "${basepkg}" ]; then
    if [ -n "${rpmname}" ]; then
        basepkg="${rpmname}"
        debug "Assuming default --base-pkg ${basepkg}"
    else
        echo "Missing required option --base-pkg" >&2
        exit 1
    fi
fi

if [ -z "${ghost}" ]; then
    echo "Missing required option --ghost" >&2
    exit 1
fi

if [ -z "${target}" ]; then
    echo "Missing required option --target" >&2
    exit 1
fi

if [ -z "${variant}" ]; then
    echo "Missing required option --variant" >&2
    exit 1
fi

if [ -z "${pkg}" ]; then
    pkg="${basepkg}-${variant}"
    debug "Assuming default --binding-pkg ${pkg}"
fi

if [ -z "${summary}" ]; then
    summary="${basepkg} binding for ${variant}"
fi

if [ -z "${description}" ]; then
    description="Configures ${basepkg} to work with ${variant}."
fi

sp=${RPM_SPECPARTS_DIR}/${pkg}.specpart
: >${sp}

if ${with_package}; then
    echo "%package -n ${pkg}" >>${sp}
    if ${with_summary}; then
        echo "Summary: ${summary}" >>${sp}
    fi
    echo "${provides}" >>${sp}
    echo "${requires}" >>${sp}
    echo "${recommends}" >>${sp}
    echo "Requires: javapackages-tools" >>${sp}
    if ${with_meta_requires}; then
        echo "Requires(meta): ${basepkg}" >>${sp}
    fi
    echo "" >>${sp}
fi

if ${with_description}; then
    echo "%description -n ${pkg}" >>${sp}
    echo "${description}" | fold >>${sp}
    echo "" >>${sp}
fi

if ${with_files}; then
    echo "%files -n ${pkg}" >>${sp}
    echo "%ghost ${jpbindingdir}/${ghost}" >>${sp}
    echo "%dir ${jpbindingdir}/${ghost}.d" >>${sp}
    echo "${jpbindingdir}/${ghost}.d/${variant}" >>${sp}
fi

if ${verbose}; then
    debug "Added the following package:"
    sed 's/./    :: &/' ${sp} >&2
fi

if ${with_install}; then
    install -d -m 755 ${RPM_BUILD_ROOT}${jpbindingdir}/${ghost}.d/
    ln -sf ${target} ${RPM_BUILD_ROOT}${jpbindingdir}/${ghost}.d/${variant}
fi
