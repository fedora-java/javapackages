#!/bin/sh
. `dirname $0`/common.sh mock

assert "$1" "-classpath"; shift
assert "$1" "jars"; shift
assert "$1" "com.example.Main"; shift
assert "$1" "some command"; shift
assert "$1" "help"; shift
echo "PASS"
