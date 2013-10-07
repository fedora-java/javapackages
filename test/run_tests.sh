#!/usr/bin/env bash

nosetests --exclude=maven_prov_test_fuzzed.py

if [ "x${1}" = "x--all" ]; then
    nosetests maven_prov_test_fuzzed.py
fi

