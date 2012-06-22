#!/bin/bash -e
# Copyright (c) 2012, Red Hat, Inc
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


_pom_xslt_header='<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://maven.apache.org/POM/4.0.0"
                xmlns:pom="http://maven.apache.org/POM/4.0.0">
  <xsl:output method="xml"
              version="1.0"
              encoding="UTF-8"
              omit-xml-declaration="yes"/>
'

_pom_xslt_trailer='<xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
'


# Print an error message followed by backtrace and exit.
_pom_bailout()
{
    echo "${@}" >&2
    echo "=== Backtrace: ===" >&2
    i=0
    while caller $i >&2
    do
	i=$((i+1))
    done
    exit 1
}


# Find POM using pattern $1 and patch it using XSLT patch coming
# from stdin. Bailout if the patch cannot be applied.
_pom_patch()
{
    # First try find the location of the POM file.
    local pom="${1}"
    if ! test -f "${pom}"; then
	pom=./"${1}"/pom.xml
	test -f "${pom}" || _pom_bailout Failed to locate POM file using pattern "'${1}'"
    fi

    # Create a backup file -- pom.xml.orig.
    test -f "${pom}".orig || cp "${pom}"{,.orig}

    # Apply identity transformation.
    xsltproc --nonet - "${pom}" >"${pom}".tmp <<<"${_pom_xslt_header}${_pom_xslt_trailer}"

    # Try to apply the patch.
    xsltproc --nonet - "${pom}".tmp >"${pom}"

    # Bail out if the resulting file is identical to the patched one.
    # This is to help maintainers detect unneeded patches.
    cmp -s "${pom}"{,.tmp} && _pom_bailout Operation on POM has no effect.
    rm -f "${pom}".tmp
}


# Replace a particular node with a comment.
#  $1 - POM location pattern
#  $2 - XPath of the element to replace
#  $3 - comment to replace the element with
_pom_disable_xpath()
{
    _pom_patch "${1}" <<EOF
${_pom_xslt_header}
  <xsl:template match="${2}">
    <xsl:comment>
      <xsl:text> ${3} </xsl:text>
    </xsl:comment>
  </xsl:template>
${_pom_xslt_trailer}
EOF
}


# Inject some code into a POM file.
# The code is put as a child of element specified by XPath.
#  $1 - POM location pattern
#  $2 - XPath of the parent element
#  $3 - code to inject
_pom_inject_xpath()
{
    _pom_patch "${1}" <<EOF
${_pom_xslt_header}
  <xsl:template match="${2}">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
<xsl:text>

</xsl:text>
    <xsl:comment>
      <xsl:text> begin of code added by maintainer </xsl:text>
    </xsl:comment>
<xsl:text>
</xsl:text>
${3}
<xsl:text>
</xsl:text>
    <xsl:comment>
      <xsl:text> end of code added by maintainer </xsl:text>
    </xsl:comment>
<xsl:text>
</xsl:text>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>
${_pom_xslt_trailer}
EOF
}


# Replace by a comment any XML node that has childreen nodes
# groupId and artifactId with given contents.
#  $1 - XPath of parent node
#  $2 - groupId:artifactId
#  $3 - POM location pattern
_pom_disable_gaid()
{
    local what=$(sed 's/[^ ]*://' <<<"${1}")
    local gid=$(sed -e 's/:[^:]*//' -e "s/..*/[text()='&']/" <<<"${2}")
    local aid=$(sed -e 's/[^:]*://' -e "s/..*/[text()='&']/" <<<"${2}")

    # TODO: support cases with no groupId specified
    _pom_patch "${3}" <<EOF
${_pom_xslt_header}
  <xsl:template match="//${1} [pom:groupId${gid} and pom:artifactId${aid}]">
    <xsl:comment>
      <xsl:text> ${what} disabled by maintainer: </xsl:text>
      <xsl:apply-templates select="pom:groupId"/>
      <xsl:text>:</xsl:text>
      <xsl:apply-templates select="pom:artifactId"/>
      <xsl:text> </xsl:text>
    </xsl:comment>
  </xsl:template>
${_pom_xslt_trailer}
EOF
}


pom_remove_dep()
{
    _pom_disable_gaid pom:dependencies/pom:dependency "${@}"
}


pom_remove_plugin()
{
    _pom_disable_gaid pom:plugins/pom:plugin "${@}"
}


pom_disable_module()
{
    _pom_disable_xpath "${2}" "//pom:modules/pom:module [text()='${1}']" "module disabled by maintainer: ${1}"
}


pom_xpath_remove()
{
    _pom_disable_xpath "${2}" "${1}" "element removed by maintainer: ${1}"
}


pom_xpath_inject()
{
    _pom_inject_xpath "${3}" "${1}" "${2}"
}
