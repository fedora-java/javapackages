#!/bin/bash

xunit_param=""
nose_version=`nosetests --version | awk '{ print $3}' | awk -F'.' '{print $1}'`
if [[ ${nose_version} -ge 1 ]]; then
    xunit_param="--with-xunit"
fi

PYTHONPATH="../python" nosetests ${xunit_param} --exclude="mvn_alias_test.py"

exit $?

