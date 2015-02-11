#!/bin/sh

. `dirname $0`/common.sh

set_flags "-XX:OnOutOfMemoryError=kill -9 %p" -Xmx2048m
set_options "-Dfoo.bar=baz" "arg1 arg2 \"' \$(echo eval-me)"

run "some command" help
