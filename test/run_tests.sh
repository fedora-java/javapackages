#!/bin/bash

nosetests --exclude=maven_prov_test_fuzzed.py
r1=$?
r2=0

if [ "x${1}" = "x--all" ]; then
    nosetests maven_prov_test_fuzzed.py
    r2=$?
fi

if [ ${r1} -lt ${r2} ]; then
    r1=${r2}
fi

exit ${r1}

