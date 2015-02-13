#!/bin/sh

assert() {
    if [ "$1" != "$2" ]; then
        echo "FAILURE: '$1' != '$2'" >&2
        exit 1
    fi
}

if [ "$1" != "mock" ]; then
    # ignore warning about missing config. We cannot set it because unexpanded
    # macro confuses the shell
    . `dirname $0`/../../java-utils/java-functions 2>/dev/null

    JAVACMD="`dirname $0`/`basename $0 ".sh"`_mock.sh"

    MAIN_CLASS="com.example.Main"
    CLASSPATH="jars"
fi
