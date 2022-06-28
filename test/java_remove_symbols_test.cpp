#include <cassert>

#include <java-utils/java_symbols.hpp>

using namespace fedora::java::javapackages::java_utils::java_symbols;

int main(int argc, const char** argv)
{
    using next_annotation_t = std::tuple<std::string_view, std::string>;
    
    assert((ignore_whitespace_comments("a", 0) == 0));
    assert((ignore_whitespace_comments("ab", 1) == 1));
    assert((ignore_whitespace_comments("//", 0) == 2));
    assert((ignore_whitespace_comments("/**/", 0) == 4));
    assert((ignore_whitespace_comments("/* a */", 0) == 7));
    assert((ignore_whitespace_comments("/**/ a", 0) == 5));
    assert((ignore_whitespace_comments("//a\n", 0) == 4));
    
    assert((next_symbol("") == ""));
    assert((next_symbol(" ") == ""));
    assert((next_symbol("(foo") == "("));
    assert((next_symbol("foo") == "foo"));
    assert((next_symbol(" foo ") == "foo"));
    assert((next_symbol("//\n\nfoo") == "foo"));
    assert((next_symbol("/* */ foo ") == "foo"));
    
    assert((find_token("@", "@") == 0));
    assert((find_token(" @", "@") == 1));
    assert((find_token("(@)", "@") == 1));
    assert((find_token("//\n@", "@") == 3));
    assert((find_token("/*\n*/\n@", "@") == 6));
    
    assert((find_token("' '@", "@") == 3));
    assert((find_token("'\''@", "@") == 4));
    assert((find_token("'\\uFFFE'@", "@") == 8));
    assert((find_token("\"//\"@", "@") == 4));
    assert((find_token("\"/*\"@", "@") == 4));
    
    assert((find_token("())", ")") == 2));
    assert((find_token("()", ")", 1) == 1));
    assert((find_token("(()))", ")") == 4));
    assert((find_token("'\"'@", "@") == 3));
    
    assert((find_token("// @", "@") == 4));
    assert((find_token("// @\n", "@") == 5));
    
    assert((find_token("/*@*/", "@") == 5));
    assert((find_token("/* @ */", "@") == 7));
    assert((find_token("/*\n@ */", "@") == 7));
    assert((find_token("// /*@", "@") == 6));
    assert((find_token("/**//*@ */", "@") == 10));
    assert((find_token("/**///@", "@") == 7));
    
    assert((find_token("'@'", "@") == 3));
    assert((find_token(R"('\uFFFE')", R"(\u)") == 8));
    assert((find_token(R"('\'')", R"(\')") == 4));
    assert((find_token(R"("@")", "@") == 3));
    assert((find_token(R"("""@")", "@") == 5));
    assert((find_token(R"("" "@")", "@") == 6));
    assert((find_token(R"("\\" "@")", "@") == 8));
    assert((find_token(R"("\\\"" "@")", "@") == 10));
    
    assert((find_token("()", ")") == 2));
    assert((find_token("(())", ")") == 4));
    
    assert((find_token("noimport", "import", 0, true) == 8));
    assert((find_token("_import", "import", 0, true) == 7));
    assert((find_token("/import", "import", 0, true) == 1));
    assert((find_token("+import", "import", 0, true) == 1));
    
    assert((find_token("importnot", "import", 0, true) == 9));
    assert((find_token("import_", "import", 0, true) == 7));
    assert((find_token("import/", "import", 0, true) == 0));
    assert((find_token("import+", "import", 0, true) == 0));
    
    assert((next_annotation("@A") == next_annotation_t("@A", "A")));
    assert((next_annotation("@A\n") == next_annotation_t("@A", "A")));
    assert((next_annotation("@A()") == next_annotation_t("@A()", "A")));
    
    assert((next_annotation("@A class B {}") == next_annotation_t("@A", "A")));
    
    assert((next_annotation("@A(a = ')')") == next_annotation_t("@A(a = ')')", "A")));
    assert((next_annotation("@A(a = ')') class B {}") == next_annotation_t("@A(a = ')')", "A")));
    
    assert((next_annotation("@A(a = \")\")") == next_annotation_t("@A(a = \")\")", "A")));
    assert((next_annotation("@A(a = \")))\" /*)))*/) class B {}") == next_annotation_t("@A(a = \")))\" /*)))*/)", "A")));
    assert((next_annotation("@A(/* ) */)") == next_annotation_t("@A(/* ) */)", "A")));
    assert((next_annotation("method(@A Object o)") == next_annotation_t("@A", "A")));
    
    assert((next_annotation("@A(\nvalue = \")\" /* ) */\n// )\n)\n") == next_annotation_t("@A(\nvalue = \")\" /* ) */\n// )\n)", "A")));
    
    assert((next_annotation(" // @A\n/* @B */\nvalue = \"@C\";\n@D") == next_annotation_t("@D", "D")));
    
    assert((next_annotation("@a.b.C") == next_annotation_t("@a.b.C", "a.b.C")));
    assert((next_annotation("@a/**/.B") == next_annotation_t("@a/**/.B", "a.B")));
    
    assert((next_annotation("@A(value = /* ) */ \")\")//)") == next_annotation_t("@A(value = /* ) */ \")\")", "A")));
    
    {
        constexpr std::string_view original_content = R"(
import java.lang.Runnable;
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;)";
        
        std::vector<std::regex> args;
        
        args.emplace_back("Runnable");
        assert((std::get<0>(remove_imports(original_content, args, {})) == R"(
import java.util.List;
import static java.util.*;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;)"));
        args.clear();
        
        args.emplace_back("[*]");
        
        assert((std::get<0>(remove_imports(original_content, args, {})) == R"(
import java.lang.Runnable;
import java.util.List;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;)"));
        args.clear();
        
        args.emplace_back("java[.]util");
        assert((std::get<0>(remove_imports(original_content, args, {})) == R"(
import java.lang.Runnable;
import static java.lang.String.valueOf;
import com.google.common.util.concurrent.Service;)"));
        args.clear();
        
        args.emplace_back("util");
        assert((std::get<0>(remove_imports(original_content, args, {})) == R"(
import java.lang.Runnable;
import static java.lang.String.valueOf;
)"));
        args.clear();
        
        args.emplace_back("java");
        assert((std::get<0>(remove_imports(original_content, args, {})) == R"(
import com.google.common.util.concurrent.Service;)"));
        args.clear();
        
        args.emplace_back("static");
        assert((std::get<0>(remove_imports(original_content, args, {})) == original_content));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import A ;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import A ; ", args, {})) == " "));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import/**/A;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import/**/A/**/;/**/", args, {})) == "/**/"));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import//\nA;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("A[.]C");
        assert((std::get<0>(remove_imports("import A./*B;*/C;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import static A;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import static a . b /**/ . A;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("static");
        assert((std::get<0>(remove_imports("import xstatic .A;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("static");
        assert((std::get<0>(remove_imports("import staticx.A;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import static/**/A;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import/**/static/**/A;", args, {})) == ""));
        args.clear();
        
        args.emplace_back("A");
        assert((std::get<0>(remove_imports("import/* A */B;", args, {})) == "import/* A */B;"));
        args.clear();
    }
    
    {
        std::vector<std::regex> patterns;
        
        patterns.emplace_back("Nullable");
        assert((remove_annotations("new @Nullable Object[initialCapacity];", patterns, {}, {}) == "new Object[initialCapacity];"));
        patterns.clear();
        
        patterns.emplace_back("A");
        assert((remove_annotations("@A(value = /* ) */ \")\")//)", patterns, {}, {}) == "//)"));
        patterns.clear();
        
        patterns.emplace_back("A");
        assert((remove_annotations(R"(
@A
class C {})", patterns, {}, {}) == "\nclass C {}"));
        patterns.clear();
    
        patterns.emplace_back("A");
        assert((remove_annotations(R"(
    @A
    class C {})", patterns, {}, {}) == "\n    class C {}"));
        patterns.clear();
        
        constexpr std::string_view original_content = R"(
@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
@org.junit.Test
@org.junit.jupiter.api.Test)";
        
        patterns.emplace_back("SuppressWarnings");
        assert((remove_annotations(original_content, patterns, {}, {}) == R"(
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
@org.junit.Test
@org.junit.jupiter.api.Test)"));
        patterns.clear();
        
        patterns.emplace_back("Suppress");
        assert((remove_annotations(original_content, patterns, {}, {}) == R"(
@org.junit.Test
@org.junit.jupiter.api.Test)"));
        patterns.clear();
        
        patterns.emplace_back("org[.]junit[.]Test");
        assert((remove_annotations(original_content, patterns, {}, {}) == R"(
@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
@org.junit.jupiter.api.Test)"));
        patterns.clear();
        
        patterns.emplace_back("Test");
        assert((remove_annotations(original_content, patterns, {}, {}) == R"(
@SuppressWarnings
@SuppressFBWarnings(value = {"EI_EXPOSE_REP", "EI_EXPOSE_REP2"})
)"));
        patterns.clear();
        
        patterns.emplace_back("@SuppressWarnings");
        assert((remove_annotations(original_content, patterns, {}, {}) == original_content));
        patterns.clear();
        
        patterns.emplace_back("EI_EXPOSE_REP");
        assert((remove_annotations(original_content, patterns, {}, {}) == original_content));
        patterns.clear();
        
        patterns.emplace_back("A");
        assert((remove_annotations("@a/*A*/.B", patterns, {}, {}) == "@a/*A*/.B"));
        patterns.clear();
        
        patterns.emplace_back("B");
        assert((remove_annotations("@a/*A*/.B", patterns, {}, {}) == ""));
        patterns.clear();
        
        patterns.emplace_back("A");
        assert((remove_annotations("@ A", patterns, {}, {}) == ""));
        patterns.clear();
        
        patterns.emplace_back("A");
        assert((remove_annotations("@//\nA", patterns, {}, {}) == ""));
        patterns.clear();
        
        patterns.emplace_back("B");
        assert((remove_annotations("@A/*(B)*/", patterns, {}, {}) == "@A/*(B)*/"));
        patterns.clear();
    }
}
