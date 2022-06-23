#!/usr/bin/lua

local lib = require("java_symbols_lib")

local help_usage = [[
Usage: java_remove_symbols.lua [-a] [list of file paths]... [-n <list of class names>...] [-p <list of patterns>...]
    -a      Also remove annotations used in code
    -n      List of simple (not fully-qualified) class names
    -p      List of patterns to match names used in code]]

if #arg == 0 or arg[1] == "-h" or arg[1] == "--help" then
    print(help_usage)
    return
end

lib.main(arg)
