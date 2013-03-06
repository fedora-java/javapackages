#!/bin/bash -e
# Copyright (c) 2013, Red Hat, Inc
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
# Authors: Mikolaj Izdebski <mizdebsk@redhat.com>


# Write XMvn reactor configuration file.
#  $1 - name of the macro or script that generated the config file
#       (for documentation purposes only)
#  $2 - 2nd leven major XML tag name (eg. resolverSettings)
#  $3 - 3rd level minor XML tag name (eg. jarRepositories)
#  $4 (optional) - 4th level micro XML tag name (eg. repository)
#  $5 (or $4 if micro tag is not specified) - XML contents
_write_xmvn_config()
{
    mkdir -p .xmvn/config.d

    # index := ++index_file
    local index_file=.xmvn/javapackages-rule-index
    local index=$(($(cat $index_file 2>/dev/null || :) + 1))
    echo $index >$index_file

    # Write common header
    cat >.xmvn/config.d/javapackages-config-$index.xml <<EOF
<?xml version="1.0" encoding="US-ASCII"?>
<!-- XMvn configuration file generated with $1
     from maven-local package (part of javapackages-tools). -->
<configuration xmlns="http://fedorahosted.org/xmvn/CONFIG/0.4.0">
EOF

    if [[ $# -eq 4 ]]; then
	cat >>.xmvn/config.d/javapackages-config-$index.xml <<EOF
  <$2>
    <$3>
      $4
    </$3>
  </$2>
</configuration>
EOF
    elif [[ $# -eq 5 ]]; then
	cat >>.xmvn/config.d/javapackages-config-$index.xml <<EOF
  <$2>
    <$3>
      <$4>
        $5
      </$4>
    </$3>
  </$2>
</configuration>
EOF
    else
	echo "_write_xmvn_config(): Requires either 4 or 5 arguments"
	exit 1
    fi
}
