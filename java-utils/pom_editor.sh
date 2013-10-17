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
#          Michael Simacek <msimacek@redhat.com>


_pom_initialize()
{
    _pom_xslt_header='<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                exclude-result-prefixes="pom"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://maven.apache.org/POM/4.0.0"
                xmlns:pom="http://maven.apache.org/POM/4.0.0">
  <xsl:output method="xml"
              version="1.0"
              encoding="UTF-8"
              indent="yes"
              omit-xml-declaration="yes"/>
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

_pom_find_file()
{

    local pom="${1}"
    if ! test -f "${pom}"; then
	pom=./"${1}"/pom.xml
	test -f "${pom}" || _pom_bailout Failed to locate POM file using pattern "'${1}'"
    fi
    echo "${pom}"
}

# Find POM using pattern $1 and patch it using XSLT patch coming
# from stdin. Bailout if the patch cannot be applied.
_pom_patch()
{
    # First try find the location of the POM file.
    local pom
    pom=$(_pom_find_file "${1}") || exit 1

    # Create a backup file -- pom.xml.orig.
    test -f "${pom}".orig || cp -p "${pom}"{,.orig}

    # Most of POM files specify XML namespace explicitly, but some of
    # them don't. In order to be able to process all POMs in a uniform
    # way we force explicit namespace declaration here. (An assumption
    # is made that model version is 4.0.0.)
    sed -i 's|<project\s*>|<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">|' "${pom}"

    # Apply identity transformation.
    (xsltproc --nonet - "${pom}" >"${pom}.tmp" <<<"${_pom_xslt_header}${_pom_xslt_trailer}")

    # Try to apply the patch.
    xsltproc --nonet - "${pom}.tmp" > "${pom}"

    # Bail out if the resulting file is identical to the patched one.
    # This is to help maintainers detect unneeded patches.
    if [ "x${2}" != "xallow-noop" ]; then
       ! cmp -s "${pom}"{,.tmp} && return
       _pom_bailout Operation on POM has no effect.
    fi
}

# Returns whitespace preceding the node
#  $1 - POM location pattern
#  $2 - XPath of the node
_pom_get_indent()
{
    local pom
    pom=$(_pom_find_file "${1}") || exit 1
    (xsltproc --nonet - "${pom}" <<EOF
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="http://maven.apache.org/POM/4.0.0"
                xmlns:pom="http://maven.apache.org/POM/4.0.0">
  <xsl:output method="text"
              version="1.0"
              encoding="UTF-8"/>
<xsl:template match="${2}" priority="10">
<xsl:value-of select="preceding-sibling::text()[1]"/>
</xsl:template>
<xsl:template match="text()"/>
</xsl:stylesheet>
EOF
)|tail -n 1|sed -e "s/\(\S*\)//g"
}

_pom_get_tab()
{
    _pom_get_indent "${1}" "/pom:project/*[1]"
}

_pom_reformat_injected(){
    local indent=$(_pom_get_indent "${1}" "${2}")
    local tab="${4}"
    cat >.input.xml <<EOF
<root>
${3}
</root>
EOF
    local injected=$(
(xsltproc --nonet - .input.xml <<EOF
<xsl:stylesheet
  version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>
  <xsl:strip-space elements="*"/>
  <xsl:template match="/">
    <xsl:copy-of select="."/>
  </xsl:template>
</xsl:stylesheet>
EOF
)|tail -n +3| head -n -1| sed "s/^  //" |sed -e "s/  /${tab}/g"|sed -e "s/^\s\+$//"
)
   rm -f .input.xml
   test -n "${injected}"|| _pom_bailout Injected XML is not well-formed
   sed -e  "s|\(\s*\)\(.*\)|<xsl:text>\n${indent}\1${tab}</xsl:text>\2|" <<EOF
<xsl:comment> begin of code added by maintainer </xsl:comment>
${injected}
<xsl:comment> end of code added by maintainer </xsl:comment>
EOF
}

# Replace a particular node with given content.
#  $1 - POM location pattern
#  $2 - XPath of the element to replace
#  $3 - content to replace the element with
_pom_replace_xpath()
{
    local code=$(_pom_reformat_injected "${1}" "${2}" "${3}" "")
    test -n "${code}" || exit 1
    _pom_patch "${1}" <<EOF
${_pom_xslt_header}
  <xsl:template match="${2}">
    ${code}
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
    _pom_patch "${1}" <<EOF
${_pom_xslt_header}
  <xsl:template match="${2}">
    <xsl:comment><xsl:text> ${3} </xsl:text></xsl:comment>
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
    local code=$(_pom_reformat_injected "${1}" "${2}" "${3}" "$(_pom_get_tab ${1})")
    test -n "${code}" || exit 1
    _pom_patch "${1}" <<EOF
${_pom_xslt_header}
  <xsl:template match="${2}">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
${code}
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>
${_pom_xslt_trailer}
EOF
}

# Inject empty node as a child of element specified by XPath only if
# it doesn't exist yet.
#  $1 - POM location pattern
#  $2 - XPath of the parent element
#  $3 - injected node name
_pom_inject_node_if_not_present()
{
    local indent=$(_pom_get_indent "${1}" "${2}")
    local tab=$(_pom_get_tab "${1}")
    _pom_patch "${1}" "allow-noop" <<EOF
${_pom_xslt_header}
  <xsl:template match="${2}">
    <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:if test="not(pom:${3})">
    <xsl:text>
${indent}${tab}</xsl:text>
      <xsl:comment> section added by maintainer </xsl:comment>
    <xsl:text>
${indent}${tab}</xsl:text>
      <${3}>
    <xsl:text>
${indent}${tab}</xsl:text>
      </${3}>
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
    local gid=$(sed -e 's/:[^:]*//' -e "s/..*/[normalize-space(text())=normalize-space('&')]/" <<<"${2}")
    local aid=$(sed -e 's/[^:]*://' -e "s/..*/[normalize-space(text())=normalize-space('&')]/" <<<"${2}")
    local extra=""

    # Support cases with no groupId specified
    if test -z "${gid}"; then
	extra='
  <xsl:template match="//'"${1} [pom:artifactId${aid}]"'">
    <xsl:comment>
      <xsl:text> '"${what}"' disabled by maintainer: </xsl:text>
      <xsl:value-of select="normalize-space(pom:artifactId/text())"/>
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
      <xsl:value-of select="normalize-space(pom:groupId/text())"/>
      <xsl:text>:</xsl:text>
      <xsl:value-of select="normalize-space(pom:artifactId/text())"/>
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
    local injected=$(sed -e "s/\(.*\)/  \1/" <<<"${5}")
    local xml=$(awk '
BEGIN { FS=":" }

{
  if (!$1) { $1="org.apache.maven.plugins" }
  print "  <groupId>" $1 "</groupId>"
  print "  <artifactId>" $2 "</artifactId>"
  if (!$3) { $3="any" }
  print "  <version>" $3 "</version>"
  if ($4) { print "  <scope>" $4 "</scope>" }
}' <<<"${2}")

    _pom_inject_xpath "${3}" "${1}" "<${4}>
${xml}
${injected}
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
    _pom_disable_xpath "${2}" "//pom:modules/pom:module [normalize-space(text())=normalize-space('${1}')]" "module disabled by maintainer: ${1}"
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
    _pom_inject_node_if_not_present "${2}" "/pom:project" "dependencies"
    _pom_inject_gaid "pom:project/pom:dependencies" "${1}" "${2}" "dependency" "${3}"
    set -x
}


pom_add_dep_mgmt()
{
    set +x
    _pom_initialize
    _pom_inject_node_if_not_present "${2}" "/pom:project" "dependencyManagement"
    _pom_inject_node_if_not_present "${2}" "pom:dependencyManagement" "dependencies"
    _pom_inject_gaid "pom:project/pom:dependencyManagement/pom:dependencies" "${1}" "${2}" "dependency" "${3}"
    set -x
}


pom_add_plugin()
{
    set +x
    _pom_initialize
    _pom_inject_node_if_not_present "${2}" "/pom:project" "build"
    _pom_inject_node_if_not_present "${2}" "/pom:project/pom:build" "plugins"
    _pom_inject_gaid "pom:project/pom:build/pom:plugins" "${1}" "${2}" "plugin" "${3}"
    set -x
}
