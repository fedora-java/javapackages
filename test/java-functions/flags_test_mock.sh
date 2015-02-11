#!/bin/sh
assert() {
    if [ "$1" != "$2" ]; then
        echo "FAILURE: '$1' != '$2'" >&2
        exit 1
    fi
}

assert "$1" "-XX:OnOutOfMemoryError=kill -9 %p"
assert "$2" "-Xmx2048m"
assert "$3" "-classpath"
assert "$4" "jars"
assert "$5" "-Dfoo.bar=baz"
assert "$6" "arg1 arg2 \"' \$(echo eval-me)"
assert "$7" "com.example.Main"
assert "$8" "some command"
assert "$9" "help"
echo "PASS"
