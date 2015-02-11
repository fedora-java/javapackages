#!/bin/sh

. `dirname $0`/common.sh

set_flags
set_options

run "some command" help
