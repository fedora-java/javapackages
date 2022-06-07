#!/usr/bin/lua

require("java_remove_symbols")

local function eq(lt, rt)
    for i = 1, #lt do
        if lt[i] ~= rt[i] then
            return false
        end
    end
    
    return true
end

tests = {
function()
    print("test_ignore_whitespace_comments...")
    
    assert(ignore_whitespace_comments([[a]], 1) == 1)
    assert(ignore_whitespace_comments([[ab]], 2) == 2)
    assert(ignore_whitespace_comments([[//]], 1) == 3)
    assert(ignore_whitespace_comments([[/**/]], 1) == 5)
    assert(ignore_whitespace_comments([[/* a */]], 1) == 8)
    assert(ignore_whitespace_comments([[/**/ a]], 1) == 6)
    assert(ignore_whitespace_comments([[//a
]], 1) == 5)
end,

function()
    print("test_next_symbol...")
    
    assert(eq({next_symbol([[]])}, {[[]], 1}))
    assert(eq({next_symbol([[ ]])}, {[[]], 2}))
    assert(eq({next_symbol([[foo]])}, {[[foo]], 4}))
    assert(eq({next_symbol([[ foo ]])}, {[[foo]], 5}))
    assert(eq({next_symbol([[//

foo]])}, {[[foo]], 8}))
    assert(eq({next_symbol("/* */ foo ")}, {[[foo]], 10}))
end,

function()
    print("test_find_token...")
    
    assert(find_token([[@]], "@") == 1)
    assert(find_token([[ @]], "@") == 2)
    assert(find_token([[//
@]], "@") == 4)
    assert(find_token([[/*
*/
@]], "@") == 7)
    
    assert(find_token([[' '@]], "@") == 4)
    assert(find_token([['\''@]], "@") == 5)
    assert(find_token([['\uFFFE'@]], "@") == 9)
    assert(find_token([["//"@]], "@") == 5)
    assert(find_token([["/*"@]], "@") == 5)
    assert(find_token([[())]], ")") == 3)
    assert(find_token([[()]], ")", 2) == 2)
    assert(find_token([[(()))]], ")") == 5)
    assert(find_token([['"'@]], "@") == 4)
    
    assert(find_token([[// @]], "@") == 5)
    assert(find_token([[// @
]], "@") == 6)
    
    assert(find_token([[/*@*/]], "@") == 6)
    assert(find_token([[/* @ */]], "@") == 8)
    assert(find_token([[/*
@ */]], "@") == 8)
    assert(find_token([[// /*
@]], "@") == 7)
    assert(find_token([[/**//*@ */]], "@") == 11)
    assert(find_token([[/**///@]], "@") == 8)
    
    assert(find_token([['@']], "@") == 4)
    assert(find_token([['\uFFFE']], "\\u") == 9)
    assert(find_token([['\'']], "\\'") == 5)
    assert(find_token([["@"]], "@") == 4)
    assert(find_token([["""@"]], "@") == 6)
    assert(find_token([["" "@"]], "@") == 7)
    assert(find_token([["\\" "@"]], "@") == 9)
    assert(find_token([["\\\"" "@"]], "@") == 11)
    
    assert(find_token([[()]], ")") == 3)
    assert(find_token([[(())]], ")") == 5)
    
    assert(find_token([[noimport]], "import", 1, true) == 9)
    assert(find_token([[_import]], "import", 1, true) == 8)
    assert(find_token([[/import]], "import", 1, true) == 2)
    assert(find_token([[+import]], "import", 1, true) == 2)
    
    assert(find_token([[importnot]], "import", 1, true) == 10)
    assert(find_token([[import_]], "import", 1, true) == 8)
    assert(find_token([[import/]], "import", 1, true) == 1)
    assert(find_token([[import+]], "import", 1, true) == 1)
end,

function()
    print("test_next_annotation...")
    
    assert(eq({next_annotation([[@A]])}, {1, 3, [[A]]}))
    assert(eq({next_annotation([[@A
]])}, {1, 3, [[A]]}))
    assert(eq({next_annotation([[@A()]])}, {1, 5, [[A]]}))
    
    assert(eq({next_annotation([[@A class B {}]])}, {1, 3, [[A]]}))
    assert(eq({next_annotation([[@A(a = ')')]])}, {1, 12, [[A]]}))
    assert(eq({next_annotation([[@A(a = ')') class B {}]])}, {1, 12, [[A]]}))
    assert(eq({next_annotation([[@A(a = ")")]])}, {1, 12, [[A]]}))
    assert(eq({next_annotation([[@A(a = ")))" /*)))*/) class B {}]])}, {1, 22, [[A]]}))
    assert(eq({next_annotation([[@A(/* ) */)]])}, {1, 12, [[A]]}))
    
    assert(eq({next_annotation([[@A(
value = ")" /* ) */
// )
)
]])}, {1, 31, [[A]]}))
    
    assert(eq({next_annotation([[ // @A
/* @B */
value = "@C";
@D]])}, {31, 33, [[D]]}))
    
    assert(eq({next_annotation([[@a.b.C]])}, {1, 7, [[a.b.C]]}))
    assert(eq({next_annotation([[@a/**/.B]])}, {1, 9, [[a.B]]}))
    
    assert(eq({next_annotation([[@A(value = /* ) */ ")")//)]])}, {1, 24, [[A]]}))
end,

function()
    print("test_remove_imports_simple...")
    
    local original_content = [[
import java.lang.Runnable;
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;]]
    
    assert(remove_imports(original_content, {"Runnable"}) == [[
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;]])
    
    assert(remove_imports(original_content, {"[*]"}) == [[
import java.lang.Runnable;
import java.util.List;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;]])
    
    assert(remove_imports(original_content, {"java[.]util"}) == [[
import java.lang.Runnable;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;]])
    
    assert(remove_imports(original_content, {"util"}) == [[
import java.lang.Runnable;
import static java.lang.String.valueOf;
]])
    
    assert(remove_imports(original_content, {"java"}) == [[
import com.google.common.util.concurrent.Service;]])
    
    assert(remove_imports(original_content, {"static"}) == original_content)
end,

function()
    print("test_remove_imports_whitespace_comments...")
    
    assert(remove_imports([[import A ;]], {"A"}) == [[]])
    assert(remove_imports([[import A ; ]], {"A"}) == [[ ]])
    assert(remove_imports([[import/**/A;]], {"A"}) == [[]])
    assert(remove_imports([[import/**/A/**/;/**/]], {"A"}) == [[/**/]])
    assert(remove_imports([[import//
A;]], {"A"}) == [[]])
    assert(remove_imports([[import A./*B;*/C;]], {"A[.]C"}) == [[]])
    
    assert(remove_imports([[import static A;]], {"A"}) == [[]])
    assert(remove_imports([[import static a . b /**/ . A;]], {"A"}) == [[]])
    
    assert(remove_imports([[import xstatic .A;]], {"static"}) == [[]])
    assert(remove_imports([[import staticx.A;]], {"static"}) == [[]])
    assert(remove_imports([[import static/**/A;]], {"A"}) == [[]])
    assert(remove_imports([[import/**/static/**/A;]], {"A"}) == [[]])
    assert(remove_imports([[import/* A */B;]], {"A"}) == [[import/* A */B;]])
end,

function()
    print("test_remove_annotations_simple...")
    
    assert(remove_annotations([[new @Nullable Object[initialCapacity];]], {"Nullable"}) == [[new Object[initialCapacity];]])
    assert(remove_annotations([[@A(value = /* ) */ ")")//)]], {"A"}) == [[//)]])
    
    assert(remove_annotations([[
@A
class C {}]], {"A"}) == [[class C {}]])
    
    assert(remove_annotations([[
    @A
    class C {}]], {"A"}) == [[    class C {}]])
    
    local original_content = [[
@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
@org.junit.Test
@org.junit.jupiter.api.Test]]
    
    assert(remove_annotations(original_content, {"SuppressWarnings"}) == [[
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
@org.junit.Test
@org.junit.jupiter.api.Test]])
    
    assert(remove_annotations(original_content, {"Suppress"}) == [[
@org.junit.Test
@org.junit.jupiter.api.Test]])
    
    assert(remove_annotations(original_content, {"org[.]junit[.]Test"}) == [[
@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
@org.junit.jupiter.api.Test]])
    
    assert(remove_annotations(original_content, {"Test"}) == [[
@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
]])
    
    assert(remove_annotations(original_content, {"@SuppressWarnings"}) == original_content)
    assert(remove_annotations(original_content, {"EI_EXPOSE_REP"}) == original_content)
end,

function()
    print("test_remove_annotations_whitespace_comments...")
    
    assert(remove_annotations([[@a/*A*/.B]], {"A"}) == [[@a/*A*/.B]])
    assert(remove_annotations([[@a/*A*/.B]], {"B"}) == [[]])
    assert(remove_annotations([[@ A]], {"A"}) == [[]])
    assert(remove_annotations([[@//
A]], {"A"}) == [[]])
    assert(remove_annotations([[@A/*(B)*/]], {"B"}) == [[@A/*(B)*/]])
end,
}

for _, test in ipairs(tests) do
    test()
end

print("PASS")
