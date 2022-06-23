local lib = require("java_symbols_lib")

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
    
    assert(lib.ignore_whitespace_comments([[a]], 1) == 1)
    assert(lib.ignore_whitespace_comments([[ab]], 2) == 2)
    assert(lib.ignore_whitespace_comments([[//]], 1) == 3)
    assert(lib.ignore_whitespace_comments([[/**/]], 1) == 5)
    assert(lib.ignore_whitespace_comments([[/* a */]], 1) == 8)
    assert(lib.ignore_whitespace_comments([[/**/ a]], 1) == 6)
    assert(lib.ignore_whitespace_comments([[//a
]], 1) == 5)
end,

function()
    print("test_next_symbol...")
    
    assert(eq({lib.next_symbol([[]])}, {[[]], 1}))
    assert(eq({lib.next_symbol([[ ]])}, {[[]], 2}))
    assert(eq({lib.next_symbol([[foo]])}, {[[foo]], 4}))
    assert(eq({lib.next_symbol([[ foo ]])}, {[[foo]], 5}))
    assert(eq({lib.next_symbol([[//

foo]])}, {[[foo]], 8}))
    assert(eq({lib.next_symbol("/* */ foo ")}, {[[foo]], 10}))
end,

function()
    print("test_find_token...")
    
    assert(lib.find_token([[@]], "@") == 1)
    assert(lib.find_token([[ @]], "@") == 2)
    assert(lib.find_token([[(@)]], "@") == 2)
    assert(lib.find_token([[//
@]], "@") == 4)
    assert(lib.find_token([[/*
*/
@]], "@") == 7)
    
    assert(lib.find_token([[' '@]], "@") == 4)
    assert(lib.find_token([['\''@]], "@") == 5)
    assert(lib.find_token([['\uFFFE'@]], "@") == 9)
    assert(lib.find_token([["//"@]], "@") == 5)
    assert(lib.find_token([["/*"@]], "@") == 5)
    assert(lib.find_token([[())]], ")") == 3)
    assert(lib.find_token([[()]], ")", 2) == 2)
    assert(lib.find_token([[(()))]], ")") == 5)
    assert(lib.find_token([['"'@]], "@") == 4)
    
    assert(lib.find_token([[// @]], "@") == 5)
    assert(lib.find_token([[// @
]], "@") == 6)
    
    assert(lib.find_token([[/*@*/]], "@") == 6)
    assert(lib.find_token([[/* @ */]], "@") == 8)
    assert(lib.find_token([[/*
@ */]], "@") == 8)
    assert(lib.find_token([[// /*
@]], "@") == 7)
    assert(lib.find_token([[/**//*@ */]], "@") == 11)
    assert(lib.find_token([[/**///@]], "@") == 8)
    
    assert(lib.find_token([['@']], "@") == 4)
    assert(lib.find_token([['\uFFFE']], "\\u") == 9)
    assert(lib.find_token([['\'']], "\\'") == 5)
    assert(lib.find_token([["@"]], "@") == 4)
    assert(lib.find_token([["""@"]], "@") == 6)
    assert(lib.find_token([["" "@"]], "@") == 7)
    assert(lib.find_token([["\\" "@"]], "@") == 9)
    assert(lib.find_token([["\\\"" "@"]], "@") == 11)
    
    assert(lib.find_token([[()]], ")") == 3)
    assert(lib.find_token([[(())]], ")") == 5)
    
    assert(lib.find_token([[noimport]], "import", 1, true) == 9)
    assert(lib.find_token([[_import]], "import", 1, true) == 8)
    assert(lib.find_token([[/import]], "import", 1, true) == 2)
    assert(lib.find_token([[+import]], "import", 1, true) == 2)
    
    assert(lib.find_token([[importnot]], "import", 1, true) == 10)
    assert(lib.find_token([[import_]], "import", 1, true) == 8)
    assert(lib.find_token([[import/]], "import", 1, true) == 1)
    assert(lib.find_token([[import+]], "import", 1, true) == 1)
end,

function()
    print("test_next_annotation...")
    
    assert(eq({lib.next_annotation([[@A]])}, {1, 3, [[A]]}))
    assert(eq({lib.next_annotation([[@A
]])}, {1, 3, [[A]]}))
    assert(eq({lib.next_annotation([[@A()]])}, {1, 5, [[A]]}))
    
    assert(eq({lib.next_annotation([[@A class B {}]])}, {1, 3, [[A]]}))
    assert(eq({lib.next_annotation([[@A(a = ')')]])}, {1, 12, [[A]]}))
    assert(eq({lib.next_annotation([[@A(a = ')') class B {}]])}, {1, 12, [[A]]}))
    assert(eq({lib.next_annotation([[@A(a = ")")]])}, {1, 12, [[A]]}))
    assert(eq({lib.next_annotation([[@A(a = ")))" /*)))*/) class B {}]])}, {1, 22, [[A]]}))
    assert(eq({lib.next_annotation([[@A(/* ) */)]])}, {1, 12, [[A]]}))
    assert(eq({lib.next_annotation([[method(@A Object o)]])}, {8, 10, [[A]]}))
    
    assert(eq({lib.next_annotation([[@A(
value = ")" /* ) */
// )
)
]])}, {1, 31, [[A]]}))
    
    assert(eq({lib.next_annotation([[ // @A
/* @B */
value = "@C";
@D]])}, {31, 33, [[D]]}))
    
    assert(eq({lib.next_annotation([[@a.b.C]])}, {1, 7, [[a.b.C]]}))
    assert(eq({lib.next_annotation([[@a/**/.B]])}, {1, 9, [[a.B]]}))
    
    assert(eq({lib.next_annotation([[@A(value = /* ) */ ")")//)]])}, {1, 24, [[A]]}))
end,

function()
    print("test_remove_imports_simple...")
    
    local original_content = [[
import java.lang.Runnable;
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;]]
    
    assert(lib.remove_imports(original_content, {"Runnable"}) == [[
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;]])
    
    assert(lib.remove_imports(original_content, {"[*]"}) == [[
import java.lang.Runnable;
import java.util.List;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;]])
    
    assert(lib.remove_imports(original_content, {"java[.]util"}) == [[
import java.lang.Runnable;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;]])
    
    assert(lib.remove_imports(original_content, {"util"}) == [[
import java.lang.Runnable;
import static java.lang.String.valueOf;
]])
    
    assert(lib.remove_imports(original_content, {"java"}) == [[
import com.google.common.util.concurrent.Service;]])
    
    assert(lib.remove_imports(original_content, {"static"}) == original_content)
end,

function()
    print("test_remove_imports_whitespace_comments...")
    
    assert(lib.remove_imports([[import A ;]], {"A"}) == [[]])
    assert(lib.remove_imports([[import A ; ]], {"A"}) == [[ ]])
    assert(lib.remove_imports([[import/**/A;]], {"A"}) == [[]])
    assert(lib.remove_imports([[import/**/A/**/;/**/]], {"A"}) == [[/**/]])
    assert(lib.remove_imports([[import//
A;]], {"A"}) == [[]])
    assert(lib.remove_imports([[import A./*B;*/C;]], {"A[.]C"}) == [[]])
    
    assert(lib.remove_imports([[import static A;]], {"A"}) == [[]])
    assert(lib.remove_imports([[import static a . b /**/ . A;]], {"A"}) == [[]])
    
    assert(lib.remove_imports([[import xstatic .A;]], {"static"}) == [[]])
    assert(lib.remove_imports([[import staticx.A;]], {"static"}) == [[]])
    assert(lib.remove_imports([[import static/**/A;]], {"A"}) == [[]])
    assert(lib.remove_imports([[import/**/static/**/A;]], {"A"}) == [[]])
    assert(lib.remove_imports([[import/* A */B;]], {"A"}) == [[import/* A */B;]])
end,

function()
    print("test_remove_annotations_simple...")
    
    assert(lib.remove_annotations([[new @Nullable Object[initialCapacity];]], {"Nullable"}) == [[new Object[initialCapacity];]])
    assert(lib.remove_annotations([[@A(value = /* ) */ ")")//)]], {"A"}) == [[//)]])
    
    assert(lib.remove_annotations([[
@A
class C {}]], {"A"}) == [[class C {}]])
    
    assert(lib.remove_annotations([[
    @A
    class C {}]], {"A"}) == [[    class C {}]])
    
    local original_content = [[
@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
@org.junit.Test
@org.junit.jupiter.api.Test]]
    
    assert(lib.remove_annotations(original_content, {"SuppressWarnings"}) == [[
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
@org.junit.Test
@org.junit.jupiter.api.Test]])
    
    assert(lib.remove_annotations(original_content, {"Suppress"}) == [[
@org.junit.Test
@org.junit.jupiter.api.Test]])
    
    assert(lib.remove_annotations(original_content, {"org[.]junit[.]Test"}) == [[
@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
@org.junit.jupiter.api.Test]])
    
    assert(lib.remove_annotations(original_content, {"Test"}) == [[
@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
]])
    
    assert(lib.remove_annotations(original_content, {"@SuppressWarnings"}) == original_content)
    assert(lib.remove_annotations(original_content, {"EI_EXPOSE_REP"}) == original_content)
end,

function()
    print("test_remove_annotations_whitespace_comments...")
    
    assert(lib.remove_annotations([[@a/*A*/.B]], {"A"}) == [[@a/*A*/.B]])
    assert(lib.remove_annotations([[@a/*A*/.B]], {"B"}) == [[]])
    assert(lib.remove_annotations([[@ A]], {"A"}) == [[]])
    assert(lib.remove_annotations([[@//
A]], {"A"}) == [[]])
    assert(lib.remove_annotations([[@A/*(B)*/]], {"B"}) == [[@A/*(B)*/]])
end,

function()
    print("test_main...")
    
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class1.java", "-n", "D"}) == [[
import a.b.D.A;
import static a.b.C.D;

@D
class Class1 {
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class1.java", "-a", "-n", "D"}) == [[
import a.b.D.A;
import static a.b.C.D;

class Class1 {
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class2.java", "-n", "Runnable"}) == [[
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;

class Class2 {
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class2.java", "-n", "*"}) == [[
import java.lang.Runnable;
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;

class Class2 {
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class2.java", "-n", "valueOf"}) == [[
import java.lang.Runnable;
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;

class Class2 {
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class2.java", "-p", "java"}) == [[
import com.google.common.util.concurrent.Service;

class Class2 {
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class2.java", "-p", "util", "-n", "Runnable"}) == [[
import static java.lang.String.valueOf;

class Class2 {
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class2.java", "-p", "static"}) == [[
import java.lang.Runnable;
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;

class Class2 {
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class3.java", "-a", "-p", "Test"}) == [[
import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
class Class3 {
    public void test1() {
    }
    
    public void test2() {
    }
    
    public void test3() {
    }
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class3.java", "-a", "-n", "Test"}) == [[
import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
class Class3 {
    public void test1() {
    }
    
    public void test2() {
    }
    
    public void test3() {
    }
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class3.java", "-a", "-p", "api[.]Test"}) == [[
import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
class Class3 {
    public void test1() {
    }
    
    @org.junit.Test
    public void test2() {
    }
    
    public void test3() {
    }
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class3.java", "-a", "-p", "Suppress"}) == [[
import org.junit.jupiter.api.Test;

class Class3 {
    @Test
    public void test1() {
    }
    
    @org.junit.Test
    public void test2() {
    }
    
    @org.junit.jupiter.api.Test
    public void test3() {
    }
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class3.java", "-a", "-p", "EI_EXPOSE_REP"}) == [[
import org.junit.jupiter.api.Test;
import edu.umd.cs.findbugs.annotations.SuppressFBWarnings;

@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
class Class3 {
    @Test
    public void test1() {
    }
    
    @org.junit.Test
    public void test2() {
    }
    
    @org.junit.jupiter.api.Test
    public void test3() {
    }
}
]])
    assert(lib.main({"--dry-run", "./test/data/java_remove_symbols/Class4.java", "-a", "-n", "Nullable"}) == [[
 /*;*/ // ;

class Class4 {
    <T extends Object> T method(Object o) {
        new Object();
    }
}
]])
end,
}

for _, test in ipairs(tests) do
    test()
end

print("PASS")
