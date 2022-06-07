#!/usr/bin/lua
--
-- Copyright (c) 2022, Red Hat, Inc.
-- All rights reserved.
--
-- Redistribution and use in source and binary forms, with or without
-- modification, are permitted provided that the following conditions
-- are met:
--
-- 1. Redistributions of source code must retain the above copyright
--    notice, this list of conditions and the following disclaimer.
-- 2. Redistributions in binary form must reproduce the above copyright
--    notice, this list of conditions and the following disclaimer in the
--    documentation and/or other materials provided with the
--    distribution.
-- 3. Neither the name of Red Hat nor the names of its
--    contributors may be used to endorse or promote products derived
--    from this software without specific prior written permission.
--
-- THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
-- "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
-- LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
-- A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
-- OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
-- SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
-- LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
-- DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
-- THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
-- (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
-- OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--
-- Author:  Marián Konček <mkoncek@redhat.com>
--------------------------------------------------------------------------------

--! Iterates over @param string starting from @param position until a character
--! is found which is neither a whitespace nor a Java comment
--! @return The position of the first non-whitespace non-comment charater or
--! #string + 1 if none is found
function ignore_whitespace_comments(string, position)
    while position <= #string do
        local result = position
        position = string.find(string, "[^%s]", position)
        if position == nil then
            return #string + 1
        end
        if string.sub(string, position, position + 1) == "//" then
            position = string.find(string, "\n", position + 2)
            if position == nil then
                return #string + 1
            end
            position = position + 1
        elseif string.sub(string, position, position + 1) == "/*" then
            _, position = string.find(string, "*/", position + 2)
            position = position + 1
        end
        if result == position then
            return result
        end
    end
    
    return position
end

--! Finds the next uncommented symbol and returns it and an index pointing past
--! it. The symbol is wither a sequence of alphanumeric characters or a single
--! non-aphanumeric character or an empty string if the end has been reached.
function next_symbol(string, position)
    position = position or 1
    local next_position = position
    local word_end = #string
    
    if position <= #string then
        next_position = ignore_whitespace_comments(string, position)
        if next_position <= #string then
            _, word_end = string.find(string, "%w*", next_position)
            if word_end < next_position then
                word_end = next_position
            end
        end
    end
    
    return string.sub(string, next_position, word_end), word_end + 1
end

--! Searches within @param string starting from @param position to find a string
--! @param token which is present in the source code neither inside a comment
--! nor inside a string nor inside a character literal. Special case when
--! @param token == ')', this function counts opening and closing parentheses
--! and returns the first parethesis outside.
--! @param alphanumeric If true, considers only tokens that are surrounded by
--! whitespace, comments or are at the boundaries of @param string
--! @return The starting index or #string + 1.
function find_token(string, token, position, alphanumeric, stack)
    position = position or 1
    alphanumeric = alphanumeric or false
    stack = stack or 0
    
    while position <= #string do
        position = ignore_whitespace_comments(string, position)
        if false then
        elseif string.sub(string, position, position) == "\'" then
            if string.sub(string, position, position + 3) == "\'\\\'\'" then
                position = position + 3
            else
                position = position + 1
                while string.sub(string, position, position) ~= "\'" do
                    position = position + 1
                end
            end
        elseif stack == 0 and string.sub(string, position, position + #token - 1) == token
            and not (alphanumeric
            --  NOTE string.sub outsde of valid range returns an empty string
                and (string.find(string.sub(string, position - 1, position - 1), "[%w_]")
                    or string.find(string.sub(string, position + #token, position + #token), "[%w_]"))) then
            return position
        elseif string.sub(string, position, position) == "\"" then
            position = position + 1
            while string.sub(string, position, position) ~= "\"" do
                if string.sub(string, position, position + 1) == "\\\\" then
                    position = position + 2
                elseif string.sub(string, position, position + 1) == "\\\"" then
                    position = position + 2
                else
                    position = position + 1
                end
            end
        elseif stack ~= 0 and string.sub(string, position, position) == ")" then
            stack = stack - 1
        elseif string.sub(string, position, position) == "(" then
            stack = stack + 1
        end
        
        position = position + 1
    end
    
    return #string + 1
end

--! @return A triple of values:
--! 1: The index of the starting '@' symbol or #string + 1
--! 2: The index pointing past the annotation name or #string + 1
--! 3: The extracted annotation name with all whitespace characters and comments
--! stripped
function next_annotation(string, position)
    local result = ""
    local end_pos = #string + 1
    position = find_token(string, "@", position)
    local expecting_dot = false
    
    if position <= #string then
        local symbol
        symbol, end_pos = next_symbol(string, position + 1)
        local new_end_pos = end_pos
        
        while true do
            if expecting_dot and symbol ~= "." then
                if symbol == "(" then
                    end_pos = find_token(string, ")", new_end_pos) + 1
                end
                break
            end
            
            result = result..symbol
            expecting_dot = not expecting_dot
            end_pos = new_end_pos
            symbol, new_end_pos = next_symbol(string, new_end_pos)
        end
    end
    
    return position, end_pos, result
end

function remove_imports(content, patterns)
    local position = 1
    local result = ""
    local removed_classes = {}
    
    while position <= #content do
        local next_position = find_token(content, "import", position, true)
        local copy_end = #content + 1
        
        if next_position <= #content then
            local import_name = ""
            local symbol, end_pos
            symbol, end_pos = next_symbol(content, next_position + 6)
            
            if symbol == "static" then
                symbol, end_pos = next_symbol(content, end_pos)
            end
            while symbol ~= ";" do
                import_name = import_name..symbol
                symbol, end_pos = next_symbol(content, end_pos)
            end
            _, end_pos = string.find(content, "%s-\n?", end_pos)
            copy_end = end_pos + 1
            for _, pattern in ipairs(patterns) do
                if string.find(import_name, pattern) then
                    copy_end = next_position
                    local class_name = select(3, string.find(import_name, ".*[.](.*)"))
                    if class_name == nil then
                        class_name = import_name
                    end
                    if class_name ~= "*" then
                        removed_classes[class_name] = true
                    end
                    break
                end
            end
            
            next_position = end_pos + 1
        end
        
        result = result..string.sub(content, position, copy_end - 1)
        position = next_position
    end
    
    return result, removed_classes
end

function remove_annotations(content, patterns)
    local position = 1
    local result = ""
    
    while position <= #content do
        local an_pos, an_end, annotation_name = next_annotation(content, position)
        local next_position = #content + 1
        local copy_end = #content + 1
        
        if an_pos <= #content then
            copy_end = an_end
            next_position = an_end
            for _, pattern in ipairs(patterns) do
                if string.find(annotation_name, pattern) then
                    copy_end = an_pos
                    next_position = string.find(content, "[^%s]", next_position) or next_position
                    break
                end
            end
        end
        
        result = result..string.sub(content, position, copy_end - 1)
        position = next_position
    end
    
    return result
end

local function handle_file(filename, patterns)
    local file = io.open(filename, "r")
    local original_content = file:read("*a")
    file:close()
    local content = original_content
    local content, removed_classes = remove_imports(content, patterns)
    if patterns["-a"] then
        -- a new table of patterns + class names of fully-qualified imports
        -- which were removed
        local removed_annotations = table.move(patterns, 1, #patterns, 1, {})
        for class_name in pairs(removed_classes) do
            table.insert(removed_annotations, "^"..class_name.."$")
        end
        content = remove_annotations(content, removed_annotations)
    end
    if #content < #original_content then
        print("Removing symbols from file: "..filename)
        local file = io.open(filename, "w")
        file:write(content)
        file:flush()
        file:close()
    end
end

local function parse_arguments(args, no_argument_flags)
    local result = {}
    local last_flag = nil
    
    for _, value in ipairs(args) do
        if string.find(value, "^-[%w]$") then
            result[value] = {}
            last_flag = value
            if no_argument_flags[value] then
                last_flag = nil
            end
        elseif value == "--" then
            last_flag = nil
        elseif last_flag then
            table.insert(result[last_flag], value)
        else
            table.insert(result, value)
        end
    end
    
    return result
end

local function interpret_flags(args)
    local patterns = args["-p"]
    local files = {}
    
    if args["-a"] then
        patterns["-a"] = true
    end
    
    if #args == 0 then
        table.insert(args, ".")
    end
    
    for _, root in ipairs(args) do
        local popen = io.popen("find '"..root.."' -type f -name '*.java'")
        for line in popen:lines() do
            table.insert(files, line)
        end
        popen:close()
    end
    
    return patterns, files
end

local function main(patterns, files)
    if #patterns == 0 then
        return
    end
    
    for _, filename in ipairs(files) do
        handle_file(filename, patterns)
    end
end

if arg and string.find(arg[0], "/java_remove_symbols.lua$") then
    local help_usage = [[
Usage: java_remove_symbols.lua [-a] [list of filepaths]... -p <list of patterns>...
    -a      Also remove annotations used in code]]
    
    if #arg == 0 or arg[1] == "-h" or arg[1] == "--help" then
        print(help_usage)
        return
    end
    
    main(interpret_flags(parse_arguments(arg, {["-a"] = true})))
end
