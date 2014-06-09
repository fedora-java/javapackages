#!/bin/bash

xunit_param=""
nose_version=`nosetests --version | awk '{ print $3}' | awk -F'.' '{print $1}'`
if [[ ${nose_version} -ge 1 ]]; then
    xunit_param="--with-xunit"
fi

PYTHONPATH="../python" nosetests ${xunit_param} --exclude="(maven_prov)|(maven_depmap)|(mvn_artifact)_test.py"
r1=$?
r2=0

# we don't have new metadata for fuzz tests, disable them for now
#if [ "x${1}" = "x--all" ]; then
#    nosetests maven_prov_test_fuzzed.py
#    r2=$?
#fi
#
#if [ ${r1} -lt ${r2} ]; then
#    r1=${r2}
#fi

exit ${r1}

