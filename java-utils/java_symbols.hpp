// Copyright (c) 2022, Red Hat, Inc.
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the
//    distribution.
// 3. Neither the name of Red Hat nor the names of its
//    contributors may be used to endorse or promote products derived
//    from this software without specific prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
// 
// Author:  Marián Konček <mkoncek@redhat.com>
////////////////////////////////////////////////////////////////////////////////

#pragma once

#include <cctype>
#include <cstddef>

#include <filesystem>
#include <fstream>
#include <regex>
#include <span>
#include <vector>
#include <set>
#include <string_view>
#include <syncstream>
#include <tuple>

#include <iostream>

namespace fedora::java::javapackages::java_utils::java_symbols
{
// Allows comparison between string and string_view
struct transparent_string_cmp : std::less<std::string_view>
{
    using is_transparent = void;
};

using transparent_string_set = std::set<std::string, transparent_string_cmp>;

using parameter_dict = std::map<std::string, std::vector<std::string>, transparent_string_cmp>;

struct Parameters
{
    std::vector<std::regex> patterns_;
    transparent_string_set names_;
    bool also_remove_annotations_ = false;
    bool dry_run_ = false;
};

inline std::ptrdiff_t ignore_whitespace_comments(std::string_view string, std::ptrdiff_t position)
{
    while (position != std::ssize(string))
    {
        std::ptrdiff_t result = position;
        
        while (std::isspace(string[position]))
        {
            ++position;
        }
        
        if (position == std::ssize(string))
        {
            return position;
        }
        
        if (auto subst = string.substr(position, 2); subst == "//")
        {
            position = string.find('\n', position + 2);
            if (position == std::ptrdiff_t(string.npos))
            {
                return std::ssize(string);
            }
            ++position;
        }
        else if (subst == "/*")
        {
            position = string.find("*/", position + 2) + 2;
        }
        
        if (result == position)
        {
            return result;
        }
    }
    
    return position;
}

inline std::string_view next_symbol(std::string_view string, std::ptrdiff_t position = 0)
{
    std::ptrdiff_t word_length = 0;
    
    if (position < std::ssize(string))
    {
        position = ignore_whitespace_comments(string, position);
        if (position < std::ssize(string))
        {
            word_length = 1;
            if (std::isalnum(string[position]))
            {
                while (position + word_length != std::ssize(string) and std::isalnum(string[position + word_length]))
                {
                    ++word_length;
                }
            }
        }
    }
    
    return string.substr(position, word_length);
}

inline std::ptrdiff_t find_token(std::string_view string, std::string_view token,
    std::ptrdiff_t position = 0, bool alphanumeric = false, std::ptrdiff_t stack = 0)
{
    while (position < std::ssize(string))
    {
        position = ignore_whitespace_comments(string, position);
        auto subst = string.substr(position, token.length());
        if ((token != ")" or stack == 0) and subst == token
            and not (alphanumeric
                and ((position > 0 and (std::isalnum(string[position - 1]) or string[position - 1] == '_'))
                    or (position + std::ssize(token) <= std::ssize(string) and ((std::isalnum(string[position + token.length()]) or string[position + token.length()] == '_'))))))
        {
            return position;
        }
        else if (string[position] == '\'')
        {
            if (string.substr(position, 4) == "'\\''")
            {
                position += 3;
            }
            else
            {
                ++position;
                while (string[position] != '\'')
                {
                    ++position;
                }
            }
        }
        else if (string[position] == '"')
        {
            ++position;
            while (string[position] != '"')
            {
                if (string.substr(position, 2) == "\\\\")
                {
                    position += 2;
                }
                else if (string.substr(position, 2) == "\\\"")
                {
                    position += 2;
                }
                else
                {
                    ++position;
                }
            }
        }
        else if (stack != 0 and string[position] == ')')
        {
            --stack;
        }
        else if (string[position] == '(')
        {
            ++stack;
        }
        
        ++position;
    }
    
    return std::ssize(string);
}

inline std::tuple<std::string_view, std::string> next_annotation(std::string_view string, std::ptrdiff_t position = 0)
{
    std::string result;
    std::ptrdiff_t end_pos = std::ssize(string);
    position = find_token(string, "@", position);
    bool expecting_dot = false;
    
    if (position < std::ssize(string))
    {
        std::string_view symbol;
        symbol = next_symbol(string, position + 1);
        end_pos = symbol.end() - string.begin();
        std::ptrdiff_t new_end_pos = end_pos;
        
        while (true)
        {
            if (expecting_dot and symbol != ".")
            {
                if (symbol == "(")
                {
                    end_pos = find_token(string, ")", new_end_pos) + 1;
                }
                break;
            }
            
            result += symbol;
            expecting_dot = not expecting_dot;
            end_pos = new_end_pos;
            symbol = next_symbol(string, new_end_pos);
            new_end_pos = symbol.end() - string.begin();
        }
    }
    
    return {string.substr(position, end_pos - position), result};
}

inline std::string_view name_matches(std::string_view name, std::span<const std::regex> patterns,
    const transparent_string_set& names, const transparent_string_set& imported_names)
{
    std::string_view class_name = name;
    if (auto pos = name.rfind('.'); pos != name.npos)
    {
        class_name = name.substr(pos + 1);
    }
    
    if (names.contains(class_name) or imported_names.contains(class_name))
    {
        return class_name;
    }
    
    for (const auto& pattern : patterns)
    {
        if (std::regex_search(name.begin(), name.end(), pattern))
        {
            return class_name;
        }
    }
    
    return {};
}

inline std::tuple<std::string, transparent_string_set> remove_imports(
    std::string_view content, std::span<const std::regex> patterns, const transparent_string_set& names)
{
    std::ptrdiff_t position = 0;
    std::string result;
    result.reserve(content.size());
    transparent_string_set removed_classes;
    
    while (position < std::ssize(content))
    {
        std::ptrdiff_t next_position = find_token(content, "import", position, true);
        std::ptrdiff_t copy_end = std::ssize(content);
        
        if (next_position < std::ssize(content))
        {
            std::string import_name;
            std::string_view symbol = next_symbol(content, next_position + 6);
            std::ptrdiff_t end_pos = symbol.end() - content.begin();
            
            const transparent_string_set empty_set;
            const transparent_string_set* names_passed = &names;
            
            if (symbol == "static")
            {
                names_passed = &empty_set;
                symbol = next_symbol(content, end_pos);
                end_pos = symbol.end() - content.begin();
            }
            
            while (symbol != ";")
            {
                import_name += symbol;
                symbol = next_symbol(content, end_pos);
                end_pos = symbol.end() - content.begin();
            }
            
            // Skip whitespace until one newline but only if newline is found
            {
                std::ptrdiff_t skip_space = end_pos;
                while (skip_space != std::ssize(content) and std::isspace(content[skip_space]))
                {
                    ++skip_space;
                    if (content[skip_space - 1] == '\n')
                    {
                        end_pos = skip_space;
                        break;
                    }
                }
            }
            
            copy_end = end_pos;
            
            std::string_view class_name = name_matches(import_name, patterns, *names_passed, {});
            
            if (not class_name.empty())
            {
                copy_end = next_position;
                
                if (class_name != "*")
                {
                    removed_classes.emplace(class_name);
                }
            }
            
            next_position = end_pos;
        }
        
        result += content.substr(position, copy_end - position);
        position = next_position;
    }
    
    return {result, removed_classes};
}

inline std::string remove_annotations(std::string_view content, std::span<const std::regex> patterns,
    const transparent_string_set& names, const transparent_string_set& imported_names)
{
    std::ptrdiff_t position = 0;
    std::string result;
    result.reserve(content.size());
    
    while (position < std::ssize(content))
    {
        auto [annotation, annotation_name] = next_annotation(content, position);
        std::ptrdiff_t next_position = std::ssize(content);
        std::ptrdiff_t copy_end = std::ssize(content);
        
        if (annotation.begin() != content.end())
        {
            copy_end = annotation.end() - content.begin();
            next_position = copy_end;
            
            if (not name_matches(annotation_name, patterns, names, imported_names).empty())
            {
                copy_end = annotation.begin() - content.begin();
                
                std::ptrdiff_t skip_space = next_position;
                while (skip_space != std::ssize(content) and std::isspace(content[skip_space]))
                {
                    ++skip_space;
                }
                
                if (skip_space != std::ssize(content))
                {
                    next_position = skip_space;
                }
            }
        }
        
        result += content.substr(position, copy_end - position);
        position = next_position;
    }
    
    return result;
}

inline std::string handle_file(std::filesystem::path path, const Parameters& parameters)
{
    std::string original_content;
    
    {
        auto ifs = std::ifstream(path);
        original_content = std::string(std::istreambuf_iterator<char>(ifs), {});
    }
    
    auto [content, removed_classes] = remove_imports(original_content, parameters.patterns_, parameters.names_);
    
    if (parameters.also_remove_annotations_)
    {
        content = remove_annotations(content, parameters.patterns_, parameters.names_, removed_classes);
    }
    
    if (not parameters.dry_run_ and content.size() < original_content.size())
    {
        std::osyncstream(std::cerr) << "Removing symbols from file " << path.native() << "\n";
        auto ofs = std::ofstream(path);
        ofs.write(content.c_str(), content.size());
    }
    
    return content;
}

inline parameter_dict parse_arguments(std::span<const char*> args, const transparent_string_set& no_argument_flags)
{
    parameter_dict result;
    const parameter_dict::iterator unflagged_parameters = result.try_emplace("").first;
    parameter_dict::iterator last_flag = unflagged_parameters;
    
    for (std::string_view arg : args)
    {
        if (arg == "--")
        {
            last_flag = unflagged_parameters;
        }
        else if (arg.size() >= 2 and arg[0] == '-' and (std::isalnum(arg[1]) or (arg[1] == '-')))
        {
            last_flag = result.try_emplace(std::string(arg)).first;
            if (no_argument_flags.contains(arg))
            {
                last_flag = unflagged_parameters;
            }
        }
        else
        {
            last_flag->second.emplace_back(arg);
        }
    }
    
    return result;
}

inline Parameters interpret_args(const parameter_dict& parameters)
{
    Parameters result;
    
    if (auto it = parameters.find("-p"); it != parameters.end())
    {
        result.patterns_.reserve(it->second.size());
        
        for (const auto& pattern : it->second)
        {
            result.patterns_.emplace_back(pattern);
        }
    }
    
    if (auto it = parameters.find("-n"); it != parameters.end())
    {
        for (const auto& name : it->second)
        {
            result.names_.insert(std::move(name));
        }
    }
    
    if (parameters.contains("-a"))
    {
        result.also_remove_annotations_ = true;
    }
    
    if (parameters.contains("--dry-run"))
    {
        result.dry_run_ = true;
    }
    
    return result;
}
} // namespace fedora::java::javapackages::java_utils::java_symbols
