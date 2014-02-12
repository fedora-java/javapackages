#!/usr/bin/python
import inspect
import re
import shutil
import sys
import optparse

from lxml import etree
from os import path
from textwrap import dedent

# all macro fuctions that can be called from external world
macros = {}

class PomException(Exception):
    pass
class PomQueryNoMatch(PomException):
    pass
class PomQueryAmbigous(PomException):
    pass
class PomQueryInvalid(PomException):
    pass

def MetaArtifact(specification, **defaults):
    parts = specification.split(':')
    class Artifact(object):
        def __init__(self, **values):
            self.values = dict.fromkeys(parts, '')
            self.values.update(defaults)
            self.values.update(values)

        @classmethod
        def from_mvn_str(cls, string):
            values = {}
            for key, value in zip(parts, string.split(':')):
                if value:
                    values[key] = value
            return cls(**values)

        @classmethod
        def from_xml(cls, element):
            values = {}
            for part in parts:
                subelement = element.find('{*}' + part)
                if subelement is not None:
                    values[part] = subelement.text.strip()
            return cls(**values)

        def get_xml(self):
            xml = ''
            for key in parts:
                value = self.values[key]
                if value:
                    xml += "<{0}>{1}</{0}>".format(key, value)
            return xml

        def get_xpath_condition(self):
            expr = "normalize-space(pom:{0})='{1}'"
            conditions = []
            for key in parts:
                value = self.values[key]
                if value and value != '*':
                    conditions.append(expr.format(key, value))
            return ' and '.join(conditions) if conditions else 'true()'

        def update(self, artifact):
            for key, value in artifact.values.iteritems():
                if key not in parts:
                    raise KeyError(key + ' not defined')
                if value:
                    self[key] = value

        def __getitem__(self, key):
            return self.values[key]

        def __setitem__(self, key, value):
            if key not in parts:
                raise KeyError(key + ' not defined')
            self.values[key] = value

    return Artifact

def find_pom(pompath):
    if path.isfile(pompath):
        return pompath
    if path.isdir(pompath):
        subpompath = path.join(pompath, 'pom.xml')
        if path.isfile(subpompath):
            return subpompath
    raise PomException("Couldn't locate POM file using pattern '{0}'"\
                        .format(pompath))

def find_poms_recursive(pomspec):
    modules = [find_pom(pomspec)]
    found = set(modules)
    module_xpath =  '/pom:project/pom:modules/pom:module |\
            /pom:project/pom:profile/pom:modules/pom:module'
    try:
        while modules:
            pompath = find_pom(modules.pop())
            found.add(pompath)
            pom_xml = etree.parse(pompath)
            modules += [path.join(path.dirname(pompath), node.text.strip())
                        for node in pom_xml.xpath(module_xpath,
                        namespaces=Pom.NSMAP)]
        return found

    except (PomException, IOError):
        raise PomException("Cannot read POM file '{0}'".format(pompath))

def get_indent(node):
    if node is None or not node.text:
        return ''
    text = node.text.split('\n')[-1]
    return re.sub(r'\S.*', '', text)

def print_usage(function):
    print >> sys.stderr, "Usage: %{name} {doc}".format(name=function.__name__,
                                                       doc=function.__doc__)

def parse_args(function, args):
    (arglist, _, _, defaults) = inspect.getargspec(function)
    option_parser = optparse.OptionParser()
    option_parser.add_option('-r', '--recursive', action="store_true")
    option_parser.add_option('-f', '--force', action="store_true")
    options, arguments = option_parser.parse_args(list(args))
    min_arg_count = len(arglist) - len(defaults)
    fnargs = dict(zip(arglist, arguments[:min_arg_count]))
    poms = arguments[min_arg_count:]
    print defaults
    if len(defaults or [] > 1) and poms:
        last = poms[-1]
        if '<' in last:
            del poms[-1]
            fnargs[arglist[-1]] = last
    if not poms:
        poms = ['.']
    return options, fnargs, poms

def macro():
    def decorator(function):
        def decorated(*args):
            try:
                pompath = None
                options, fnargs, poms = parse_args(function, args)

                for pomspec in poms:
                    if options.recursive:
                        pompaths = find_poms_recursive(pomspec)
                    else:
                        pompaths = [find_pom(pomspec)]

                    matches = 0
                    for pompath in pompaths:
                        try:
                            pom = Pom(pompath)
                            fnargs['pom'] = pom
                            pom.patch(function, fnargs)
                            matches += 1
                        except PomQueryNoMatch as exception:
                            pass
                    if matches == 0 and not options.force:
                        raise exception

            except (PomException, etree.XMLSyntaxError, IOError, TypeError) as exception:
                if pompath:
                    print >> sys.stderr, "Error in processing {0}".format(pompath)
                print >> sys.stderr, exception.message
                print_usage(function)
                sys.exit(3)

        macros[function.__name__] = decorated
        return decorated
    return decorator

class Pom(object):
    NSMAP = {'pom': 'http://maven.apache.org/POM/4.0.0',
              'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    NS = '{' + NSMAP['pom'] + '}'
    XMLNS = ('xmlns="http://maven.apache.org/POM/4.0.0"'
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
    'xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 '
    'http://maven.apache.org/xsd/maven-4.0.0.xsd"')

    BEGIN_COMMENT = "<!-- begin of code added by maintainer -->"
    END_COMMENT = "<!-- end of code added by maintainer -->"

    def __init__(self, pompath):
        with open(pompath) as pomfile:
            pom = re.sub(r'\<\s*project\s*\>',
                    ('<project {ns}>').format(ns=self.XMLNS), pomfile.read())
        self.pompath = pompath
        self.root = etree.fromstring(pom)
        self.tab = get_indent(self.root)

    def write(self, filename):
        with open(filename, 'w') as pomfile:
            pomfile.write(etree.tostring(self.root))
            pomfile.write('\n')

    def patch(self, function, fnargs):
        pomdir = path.dirname(self.pompath)
        pomfile = path.basename(self.pompath)
        try:
            self.write(path.join(pomdir, pomfile + '.tmp'))
            function(**fnargs)
        finally:
            origfile = path.join(pomdir, pomfile + '.orig')
            shutil.move(self.pompath, origfile)
            self.write(self.pompath)

    def inject_xml(self, parent, content):
        content = self.subtree_from_string(content)
        items = len(content)
        parent[:0] = content
        self.reformat(parent, parent[:items])

    def replace_xml(self, replaced, content):
        content = self.subtree_from_string(content)
        parent = replaced.getparent()
        parent.text = content.text
        if not isinstance(replaced, etree._Element):
            parent.extend(content)
        else:
            idx = parent.index(replaced)
            items = len(content)
            del parent[idx]
            for i, element in enumerate(content):
                parent.insert(idx + i, element)
            self.reformat(parent, parent[idx: idx + items])

    def replace_xml_content(self, parent, content):
        content = self.subtree_from_string(content)
        parent[:] = content
        parent.text = content.text
        self.reformat(parent, parent)

    def make_path(self, node, elements):
        if elements:
            child = node.find(elements[0], namespaces=self.NSMAP)
            if child is None:
                name = re.sub(r'pom:', self.NS, elements[0])
                child = etree.Element(name)
                node.insert(0, child)
                node.insert(0, etree.Comment(" section added by maintainer "))
                self.reformat(node, node[:2])
            return self.make_path(child, elements[1:])
        return node

    def inject_artifact(self, where, node_name, artifact, aux_content=''):
        path_parts = [part for part in where.split('/') if part]
        parent = self.make_path(self.root, path_parts)
        self.inject_xml(parent, Pom.comment("<{name}>{content} {aux}</{name}>")\
                                .format(name=node_name,
                                        content=artifact.get_xml(),
                                        aux=aux_content))

    def reformat(self, parent_node, elements):
        level = 0
        element = parent_node
        while element is not None:
            level += 1
            element = element.getparent()
        base = self.tab * level
        def prettify_node(node, parent, indent):
            if parent[0] == node:
                text = parent.text or ''
                parent.text = text.strip() + '\n' + indent
            tail = node.tail or ''
            if parent[-1] == node:
                node.tail = tail.strip() + '\n' + indent[:len(indent) - len(self.tab)]
            else:
                node.tail = tail.strip() + '\n' + indent
            for child in node:
                prettify_node(child, node, indent + self.tab)
        for element in elements:
            prettify_node(element, parent_node, base)

    def xpath_query_element(self, query):
        query_result = self.xpath_query(query)
        if len(query_result) > 1:
            raise PomQueryAmbigous("XPath query '{0}' matched more than one nodes."\
                                  .format(query))
        parent = query_result[0]
        if not isinstance(parent, etree._Element):
            raise PomQueryNoMatch("XPath query '{0}': matched node is not an element"\
                                  .format(query))
        return parent

    def xpath_query(self, query):
        if not query.startswith('/'):
            query = '//' + query
        try:
            query_result = self.root.xpath(query, namespaces=self.NSMAP)
        except etree.XPathEvalError as error:
            raise PomQueryInvalid("XPath query '{0}': {1}.".format(query,
                                                               error.message))
        if len(query_result) == 0:
            raise PomQueryNoMatch(dedent("""\
                    XPath query '{0}' didn't match any node.
                    (Did you forget to specify 'pom:' namespace?)""").format(query))
        return query_result

    def subtree_from_string(self, xml_string, root='root'):
        document = "<{root} {ns}>{0}</{root}>".format(xml_string, root=root, ns=self.XMLNS)
        try:
            tree = etree.fromstring(document)
        except etree.XMLSyntaxError as error:
            raise PomException("Syntax error in injected XML: {0}.".format(error))
        return tree

    @staticmethod
    def comment(content):
        return Pom.BEGIN_COMMENT + content + Pom.END_COMMENT

artifact_spec = 'groupId:artifactId:version'
artifact_spec_scoped = artifact_spec + ':scope'
VersionedArtifact = MetaArtifact(artifact_spec)
DefaultVersionedArtifact = MetaArtifact(artifact_spec, version='any')
ScopedArtifact = MetaArtifact(artifact_spec_scoped)
DefaultScopedArtifact = MetaArtifact(artifact_spec_scoped, version='any')

@macro()
def pom_xpath_inject(where, xml_string, pom=None):
    """<XPath> [XML code] [POM location]"""
    for element in pom.xpath_query(where):
        pom.inject_xml(element, Pom.comment(xml_string))

@macro()
def pom_xpath_replace(where, xml_string, pom=None):
    """<XPath> <XML code> [POM location]"""
    for element in pom.xpath_query(where):
        pom.replace_xml(element, Pom.comment(xml_string))

@macro()
def pom_xpath_remove(where, pom=None):
    """<XPath> [POM location]"""
    for element in pom.xpath_query(where):
        pom.replace_xml(element,
                "<!-- element removed by maintainer: {0} -->".format(where))

@macro()
def pom_xpath_set(where, content, pom=None):
    """<XPath> <new contents> [POM location]"""
    for element in pom.xpath_query(where):
        pom.replace_xml_content(element, Pom.comment(content))

@macro()
def pom_remove_dep(dep, pom=None):
    """[groupId]:[artifactId] [POM location]"""
    try:
        artifact = VersionedArtifact.from_mvn_str(dep)
        xpath = "//pom:dependency[{0}]".format(artifact.get_xpath_condition())
        elements = pom.xpath_query(xpath)
        for element in elements:
            pom.replace_xml(element,
                    "<!-- dependency removed by maintainer: {0} -->".format(dep))
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Dependency '{0}' not found.".format(dep))

@macro()
def pom_remove_plugin(plugin, pom=None):
    """[groupId]:[artifactId] [POM location]"""
    try:
        artifact = VersionedArtifact.from_mvn_str(plugin)
        xpath = "//pom:plugin[{0}]".format(artifact.get_xpath_condition())
        elements = pom.xpath_query(xpath)
        for element in elements:
            pom.replace_xml(element,
                    "<!-- plugin removed by maintainer: {0} -->".format(plugin))
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Plugin '{0}' not found.".format(plugin))

@macro()
def pom_disable_module(module, pom=None):
    """<module name> [POM location]"""
    try:
        xpath = "//pom:module[normalize-space(text())='{0}']".format(module)
        elements = pom.xpath_query(xpath)
        for element in elements:
            pom.replace_xml(element,
                    "<!-- module removed by maintainer: {0} -->".format(module))
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Module '{0}' not found.".format(module))

@macro()
def pom_add_parent(parent, pom=None):
    """groupId:artifactId[:version] [POM location]"""
    if pom.root.find('pom:parent', namespaces=Pom.NSMAP) is not None:
        raise PomException("POM already has a parent.")
    artifact = DefaultVersionedArtifact.from_mvn_str(parent)
    pom.inject_artifact('', 'parent', artifact)

@macro()
def pom_remove_parent(pom=None):
    """[POM location]"""
    try:
        pom.replace_xml(pom.xpath_query_element("/pom:project/pom:parent"),
                        "<!-- parent POM reference removed by maintainer -->")
    except PomQueryNoMatch:
        raise PomQueryNoMatch("POM doesn't specify parent.")

@macro()
def pom_set_parent(parent, pom=None):
    """groupId:artifactId[:version] [POM location]"""
    try:
        artifact = DefaultVersionedArtifact.from_mvn_str(parent)
        element = pom.xpath_query_element("/pom:project/pom:parent")
        pom.replace_xml_content(element, artifact.get_xml())
    except PomQueryNoMatch:
        raise PomQueryNoMatch("POM doesn't specify parent.")

@macro()
def pom_add_dep(dep, pom=None, xml_string=''):
    """groupId:artifactId[:version[:scope]] [POM location] [extra XML]"""
    artifact = DefaultScopedArtifact.from_mvn_str(dep)
    pom.inject_artifact('pom:dependencies', 'dependency', artifact,
                        xml_string)

@macro()
def pom_add_dep_mgmt(dep, pom=None, xml_string=''):
    """groupId:artifactId[:version[:scope]] [POM location] [extra XML]"""
    artifact = DefaultScopedArtifact.from_mvn_str(dep)
    pom.inject_artifact('pom:dependencyManagement/pom:dependencies',
                        'dependency', artifact, xml_string)

@macro()
def pom_add_plugin(plugin, pom=None, xml_string=''):
    """groupId:artifactId[:version] [POM location] [extra XML]"""
    artifact = MetaArtifact(artifact_spec, version='any',
                        groupId='org.apache.maven.plugins').from_mvn_str(plugin)
    pom.inject_artifact('pom:build/pom:plugins', 'plugin', artifact,
                        xml_string)

@macro()
def pom_change_dep(old, new, pom=None, xml_string=''):
    """groupId:artifactId[:version] groupId:artifactId[:version[:scope]]
       [POM location] [extra XML]"""
    try:
        old_artifact = VersionedArtifact.from_mvn_str(old)
        xpath = "//pom:dependency[{0}]".format(old_artifact.get_xpath_condition())
        elements = pom.xpath_query(xpath)
        for element in elements:
            new_artifact = DefaultScopedArtifact.from_xml(element)
            new_artifact.update(ScopedArtifact.from_mvn_str(new))
            new_xml = new_artifact.get_xml() + xml_string
            pom.replace_xml_content(element, new_xml)
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Dependency '{0}' not found.".format(old))

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print >> sys.stderr, "Usage:\n\t{0} command {{arguments}}"\
                              .format(sys.argv[0])
        sys.exit(1)

    macros[sys.argv[1]](*sys.argv[2:])
