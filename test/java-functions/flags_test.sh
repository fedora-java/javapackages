#!/bin/sh

# ignore warning about missing config. We cannot set it because unexpanded
# macro confuses the shell
. `dirname $0`/../../java-utils/java-functions 2>/dev/null

JAVACMD="`dirname $0`/flags_test_mock.sh"

MAIN_CLASS="com.example.Main"
CLASSPATH="jars"
set_flags "-XX:OnOutOfMemoryError=kill -9 %p" -Xmx2048m
set_options "-Dfoo.bar=baz" "arg1 arg2 \"' \$(echo eval-me)"

run "some command" help
