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

--! Iterates over @p string starting from @p position until a character
--! is found which is neither a whitespace nor a Java comment
--! @return The position of the first non-whitespace non-comment charater or
--! #string + 1 if none is found
local function ignore_whitespace_comments(string, position)
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
local function next_symbol(string, position)
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

--! Searches within @p string starting from @p position to find a string
--! @param token which is present in the source code neither inside a comment
--! nor inside a string nor inside a character literal. Special case when
--! @p token == ')', this function counts opening and closing parentheses
--! and returns the first parethesis outside.
--! @param alphanumeric If true, considers only tokens that are surrounded by
--! whitespace, comments or are at the boundaries of @p string
--! @return The starting index or #string + 1.
local function find_token(string, token, position, alphanumeric, stack)
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
        elseif (token ~= ")" or stack == 0) and string.sub(string, position, position + #token - 1) == token
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
local function next_annotation(string, position)
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

--! @param name Class name found in code, may be fully-qualified or simple.
--! @param patterns A table of patterns.
--! @param names A table of names, these are matched exactly by the simple class
--! names.
--! @param imported_names Names that have their import declarations removed. In
--! this case, we match the full name and this will only remove names that are
--! used in their simple form in code (therefore they refer to the removed
--! import declaration. If a name is used in its fully-qualified form in the
--! code, it will be catched by the other matchers.
--! @return The simple class name.
local function name_matches(name, patterns, names, imported_names)
    local class_name = select(3, string.find(name, ".*[.](.*)")) or name
    
    if names[class_name] then
        return class_name
    end
    
    if imported_names[name] then
        return class_name
    end
    
    for _, pattern in ipairs(patterns) do
        if string.find(name, pattern) then
            return class_name
        end
    end
    
    return nil
end

local function remove_imports(content, patterns, names)
    local position = 1
    local result = ""
    local removed_classes = {}
    names = names or {}
    
    while position <= #content do
        local next_position = find_token(content, "import", position, true)
        local copy_end = #content + 1
        
        if next_position <= #content then
            local import_name = ""
            local symbol, end_pos
            symbol, end_pos = next_symbol(content, next_position + 6)
            local names_passed = names
            
            if symbol == "static" then
                names_passed = {}
                symbol, end_pos = next_symbol(content, end_pos)
            end
            while symbol ~= ";" do
                import_name = import_name..symbol
                symbol, end_pos = next_symbol(content, end_pos)
            end
            _, end_pos = string.find(content, "%s-\n?", end_pos)
            copy_end = end_pos + 1
            
            local class_name = name_matches(import_name, patterns, names_passed, {})
            
            if class_name then
                copy_end = next_position
                if class_name ~= "*" then
                    removed_classes[class_name] = true
                end
            end
            
            next_position = end_pos + 1
        end
        
        result = result..string.sub(content, position, copy_end - 1)
        position = next_position
    end
    
    return result, removed_classes
end

local function remove_annotations(content, patterns, names, imported_names)
    local position = 1
    local result = ""
    names = names or {}
    imported_names = imported_names or {}
    
    while position <= #content do
        local an_pos, an_end, annotation_name = next_annotation(content, position)
        local next_position = #content + 1
        local copy_end = #content + 1
        
        if an_pos <= #content then
            copy_end = an_end
            next_position = an_end
            if name_matches(annotation_name, patterns, names, imported_names) then
                copy_end = an_pos
                next_position = string.find(content, "[^%s]", next_position) or next_position
            end
        end
        
        result = result..string.sub(content, position, copy_end - 1)
        position = next_position
    end
    
    return result
end

local function handle_file(filename, parameters)
    local patterns = parameters["patterns"]
    local names = parameters["names"]
    local file = io.open(filename, "r")
    local original_content = file:read("*a")
    file:close()
    local content = original_content
    local content, removed_classes = remove_imports(content, patterns, names)
    
    if parameters["-a"] then
        -- a new table of patterns + class names of fully-qualified imports
        -- which were removed
        content = remove_annotations(content, patterns, names, removed_classes)
    end
    
    if not parameters["--dry-run"] and #content < #original_content then
        print("Removing symbols from file: "..filename)
        local file = io.open(filename, "w")
        file:write(content)
        file:flush()
        file:close()
    end
    
    return content
end

local function parse_arguments(args, no_argument_flags)
    local result = {}
    local last_flag = nil
    
    for _, value in ipairs(args) do
        if string.find(value, "^[-][%w]$") or string.find(value, "^[-][-].+$") then
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

--! The patterns table is used in two ways simultaneously:
--! 1. as a list of patterns
--! 2. as a dictionary of simple class names
local function interpret_args(args_table)
    local files = {}
    local names = {}
    local patterns = args_table["-p"] or {}
    
    for _, class_name in ipairs(args_table["-n"] or {}) do
        names[class_name] = true
    end
    
    if #args_table == 0 then
        table.insert(args_table, ".")
    end
    
    for _, root in ipairs(args_table) do
        local popen = io.popen("find '"..root.."' -type f -name '*.java'")
        for line in popen:lines() do
            table.insert(files, line)
        end
        popen:close()
    end
    
    return files, {
        patterns = patterns,
        names = names,
        ["-a"] = args_table["-a"],
        ["--dry-run"] = args_table["--dry-run"],
    }
end

local function main(args)
    local files, parameters = interpret_args(parse_arguments(args, {["-a"] = true, ["--dry-run"] = true}))
    local is_dry_run = (parameters["--dry-run"] ~= nil)
    local result = ""
    
    for _, filename in ipairs(files) do
        single_result = handle_file(filename, parameters)
        if is_dry_run then
            result = result..single_result
        end
    end
    
    return result
end

return {
    main = main,
    
    -- Used for testing
    ignore_whitespace_comments = ignore_whitespace_comments,
    next_symbol = next_symbol,
    find_token = find_token,
    next_annotation = next_annotation,
    remove_imports = remove_imports,
    remove_annotations = remove_annotations,
}
