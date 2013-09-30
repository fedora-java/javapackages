#!/usr/bin/bash
if [ "x${1}" = "x--all" ]; then
    python -m unittest discover -p '*_test*.py'
else
    python -m unittest discover -p '*_test.py'
fi
