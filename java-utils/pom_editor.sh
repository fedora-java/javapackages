#!/bin/bash -e
# Copyright (c) 2012-2013, Red Hat, Inc
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


_pom_initialize()
{
    _pom_xslt_header='<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://maven.apache.org/POM/4.0.0"
                xmlns:pom="http://maven.apache.org/POM/4.0.0">
  <xsl:output method="xml"
              version="1.0"
              encoding="UTF-8"
              indent="yes"
              omit-xml-declaration="yes"/>
    <xsl:strip-space elements="*"/>
'

    _pom_xslt_trailer='<xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
'
}


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
    test -f "${pom}".orig || cp -p "${pom}"{,.orig}

    # Most of POM files specify XML namespace explicitly, but some of
    # them don't. In order to be able to process all POMs in a uniform
    # way we force explicit namespace declaration here. (An assumption
    # is made that model version is 4.0.0.)
    sed -i 's|<project>|<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">|' "${pom}"

    # Apply identity transformation.
    xsltproc --nonet - "${pom}" >"${pom}".tmp <<<"${_pom_xslt_header}${_pom_xslt_trailer}"

    # Try to apply the patch.
    xsltproc --nonet - "${pom}".tmp >"${pom}.unindented"
    xsltproc --nonet - "${pom}.unindented" >"${pom}" <<<"${_pom_xslt_header}${_pom_xslt_trailer}"
    rm "${pom}.unindented"

    # Bail out if the resulting file is identical to the patched one.
    # This is to help maintainers detect unneeded patches.
    if [ "x${2}" != "xallow-noop" ]; then
       cmp -s "${pom}"{,.tmp} && _pom_bailout Operation on POM has no effect.
    fi
    rm -f "${pom}".tmp
}


# Replace a particular node with given content.
#  $1 - POM location pattern
#  $2 - XPath of the element to replace
#  $3 - content to replace the element with
_pom_replace_xpath()
{
    _pom_patch "${1}" <<EOF
${_pom_xslt_header}
  <xsl:template match="${2}">
    ${3}
  </xsl:template>
${_pom_xslt_trailer}
EOF
}


# Replace a particular node with a comment.
#  $1 - POM location pattern
#  $2 - XPath of the element to replace
#  $3 - comment to replace the element with
_pom_disable_xpath()
{
    _pom_replace_xpath "${1}" "${2}" "<xsl:comment><xsl:text> ${3} </xsl:text></xsl:comment>"
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
    <xsl:comment>begin of code added by maintainer</xsl:comment>
<xsl:text>
</xsl:text>
${3}
<xsl:text>
</xsl:text>
    <xsl:comment>end of code added by maintainer</xsl:comment>
<xsl:text>
</xsl:text>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>
${_pom_xslt_trailer}
EOF
}

# Injects empty node as a child of element specified by XPath only if it doesn't exist yet
# $1 - POM location pattern
# $2 - XPath of the parent element
# $3 - ijected node name
_pom_inject_node_if_not_present()
{
    _pom_patch "${1}" "allow-noop" <<EOF
${_pom_xslt_header}
  <xsl:template match="${2}">
    <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:if test="not(pom:${3})">
      <xsl:comment>section added by maintainer</xsl:comment>
      <${3}/>
    </xsl:if>
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
    local extra=""

    # Support cases with no groupId specified
    if test -z "${gid}"; then
	extra='
  <xsl:template match="//'"${1} [pom:artifactId${aid}]"'">
    <xsl:comment>
      <xsl:text> '"${what}"' disabled by maintainer: </xsl:text>
      <xsl:apply-templates select="pom:artifactId"/>
      <xsl:text> </xsl:text>
    </xsl:comment>
  </xsl:template>'
    fi

    _pom_patch "${3}" <<EOF
${_pom_xslt_header}
  ${extra}
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


# Add a new XML element referencing given artifact.
#  $1 - XPath of parent node
#  $2 - groupId:artifactId[:version[:scope]]
#  $3 - POM location pattern
#  $4 - XML tag name
#  $5 - additional XML contents
_pom_inject_gaid()
{
    local xml=$(awk '
BEGIN { FS=":" }

{
  if (!$1) { $1="org.apache.maven.plugins" }
  print "<groupId>" $1 "</groupId>"
  print "<artifactId>" $2 "</artifactId>"
  if (!$3) { $3="any" }
  print "<version>" $3 "</version>"
  if ($4) { print "<scope>" $4 "</scope>" }
}' <<<"${2}")

    _pom_inject_xpath "${3}" "${1}" "<${4}>
${xml}
${5}
</${4}>"
}


pom_remove_dep()
{
    set +x
    _pom_initialize
    _pom_disable_gaid pom:dependencies/pom:dependency "${@}"
    set -x
}


pom_remove_plugin()
{
    set +x
    _pom_initialize
    _pom_disable_gaid pom:plugins/pom:plugin "${@}"
    set -x
}


pom_disable_module()
{
    set +x
    _pom_initialize
    _pom_disable_xpath "${2}" "//pom:modules/pom:module [text()='${1}']" "module disabled by maintainer: ${1}"
    set -x
}


pom_xpath_remove()
{
    set +x
    _pom_initialize
    _pom_disable_xpath "${2}" "${1}" "element removed by maintainer: ${1}"
    set -x
}


pom_xpath_inject()
{
    set +x
    _pom_initialize
    _pom_inject_xpath "${3}" "${1}" "${2}"
    set -x
}


pom_xpath_replace()
{
    set +x
    _pom_initialize
    _pom_replace_xpath "${3}" "${1}" "${2}"
    set -x
}


pom_xpath_set()
{
    set +x
    _pom_initialize
    _pom_replace_xpath "${3}" "${1}/text()" "${2}"
    set -x
}


pom_add_parent()
{
    set +x
    _pom_initialize
    _pom_inject_gaid "pom:project" "${1}" "${2}" "parent" "${3}"
    set -x
}


pom_remove_parent()
{
    set +x
    _pom_initialize
    _pom_disable_xpath "${1}" "//pom:project/pom:parent" "parent POM reference removed by maintainer"
    set -x
}


pom_set_parent()
{
    set +x
    _pom_initialize
    _pom_disable_xpath "${2}" "//pom:project/pom:parent" "parent POM reference replaced by maintainer"
    _pom_inject_gaid "pom:project" "${1}" "${2}" "parent" "${3}"
    set -x
}


pom_add_dep()
{
    set +x
    _pom_initialize
    _pom_inject_node_if_not_present "${2}" "pom:project" "dependencies"
    _pom_inject_gaid "pom:project/pom:dependencies" "${1}" "${2}" "dependency" "${3}"
    set -x
}


pom_add_dep_mgmt()
{
    set +x
    _pom_initialize
    _pom_inject_node_if_not_present "${2}" "pom:project" "dependencyManagement"
    _pom_inject_gaid "pom:project/pom:dependencyManagement" "${1}" "${2}" "dependency" "${3}"
    set -x
}


pom_add_plugin()
{
    set +x
    _pom_initialize
    _pom_inject_node_if_not_present "${2}" "pom:project" "build"
    _pom_inject_node_if_not_present "${2}" "pom:build" "plugins"
    _pom_inject_gaid "pom:project/pom:build/pom:plugins" "${1}" "${2}" "plugin" "${3}"
    set -x
}
