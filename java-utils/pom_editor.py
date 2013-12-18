#!/usr/bin/python
import inspect
import re
import shutil
import sys

from lxml import etree
from os import path

class PomException(Exception):
    pass
class PomQueryNoMatch(PomException):
    pass
class PomQueryAmbigous(PomException):
    pass
class PomQueryInvalid(PomException):
    pass

class Artifact(object):
    def __init__(self, specification, **defaults):
        self.parts = specification.split(':')
        self.values = dict.fromkeys(self.parts, '')
        self.values.update(defaults)
        print self.values

    def __getitem__(self, name):
        return self.values[name]

    def __setitem__(self, name, newval):
        self.values[name] = newval

    def load(self, string):
        tokens = string.split(':')
        if len(tokens) > len(self.parts):
            raise PomException("Too many colons in artifact specification '{0}'."\
                                .format(string))
        for i, token in enumerate(tokens):
            if token:
                self.values[self.parts[i]] = token
        return self

    def get_xml(self):
        xml = ''
        for key in self.parts:
            value = self.values[key]
            if value:
                xml += "<{0}>{1}</{0}>".format(key, value)
        return xml

    def get_xpath_condition(self):
        expr = "normalize-space(pom:{0})='{1}'"
        conditions = []
        for key in self.parts:
            value = self.values[key]
            if value and value != '*':
                conditions.append(expr.format(key, value))
        return ' and '.join(conditions)

def find_pom(pompath):
    if path.isfile(pompath):
        return pompath
    if path.isdir(pompath):
        subpompath = path.join(pompath, 'pom.xml')
        if path.isfile(subpompath):
            return subpompath
    raise PomException("Couldn't locate POM file using pattern '{0}'"\
                        .format(pompath))

def get_indent(node):
    if node is None or not node.text:
        return ''
    text = node.text.split('\n')[-1]
    return re.sub(r'\S.*', '', text)

def patch_poms(function, args):
    (arglist, _, _, defaults) = inspect.getargspec(function)
    maxargcount = len(arglist)
    minargcount = maxargcount - len(defaults or [])
    if len(args) > maxargcount or len(args) < minargcount:
        print >> sys.stderr, "Usage: %pom_{name} {doc}".format(name=function.__name__,
                                                         doc=function.__doc__)
        sys.exit(1)
    pomspec_pos = arglist.index('pom')
    if pomspec_pos < len(args):
        pomspec = args[pomspec_pos]
    else:
        pomspec = 'pom.xml'
    try:
        pompath = find_pom(pomspec)
    except PomException as exception:
        print >> sys.stderr, exception.message
        sys.exit(2)
    try:
        pomdir = path.dirname(pompath) or '.'
        pom = Pom(pompath)
        pom.write(path.join(pomdir, path.basename(pompath) + '.tmp'))
        fnargs = args[:pomspec_pos] + [pom] + args[pomspec_pos + 1:]
        function(*fnargs)
        origfile = path.join(pomdir, path.basename(pompath) + '.orig')
        shutil.move(pompath, origfile)
        pom.write(pompath)
    except (PomException, OSError, IOError) as exception:
        print >> sys.stderr, "Error in processing {0}".format(pompath)
        print >> sys.stderr, exception.message
        sys.exit(3)

class Pom(object):
    NSMAP = {'pom': 'http://maven.apache.org/POM/4.0.0',
              'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    POM_NS = '{' + NSMAP['pom'] + '}'
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
        self.root = etree.fromstring(pom)
        self.tab = get_indent(self.root)

    def write(self, filename):
        with open(filename, 'w') as pomfile:
            pomfile.write(etree.tostring(self.root))
            pomfile.write('\n')

    def inject_xml(self, parent, content):
        content = self.subtree_from_string(content)
        items = len(content)
        parent[:0] = content
        self.reformat(parent, parent[:items])

    def replace_xml(self, replaced, content):
        content = self.subtree_from_string(content)
        parent = replaced.getparent()
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
                name = re.sub(r'pom:', self.POM_NS, elements[0])
                child = etree.Element(name)
                node.insert(0, child)
                node.insert(0, etree.Comment(" section added by maintainer "))
                self.reformat(node, node[:2])
            return self.make_path(child, elements[1:])
        return node

    def inject_artifact(self, where, node_name, artifact, aux_content=''):
        parent = self.make_path(self.root, where.split('/') or [])
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
            raise PomQueryNoMatch("XPath query '{0}' didn't match any node."\
                                  .format(query))
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

class PomEditor(object):
    @staticmethod
    def pom_xpath_inject(where, xml_string, pom=None):
        pom.inject_xml(pom.xpath_query_element(where), Pom.comment(xml_string))

    @staticmethod
    def pom_xpath_replace(where, xml_string, pom=None):
        pom.replace_xml(pom.xpath_query_element(where), Pom.comment(xml_string))

    @staticmethod
    def pom_xpath_remove(where, pom=None):
        pom.replace_xml(pom.xpath_query_element(where), "<!-- element removed by maintainer -->")

    @staticmethod
    def pom_xpath_set(where, content, pom=None):
        #TODO check content
        pom.replace_xml_content(pom.xpath_query_element(where), Pom.comment(content))

    @staticmethod
    def pom_remove_dep(dep, pom=None):
        try:
            artifact = Artifact('groupId:artifactId:version').load(dep)
            xpath = "//pom:dependency[{0}]".format(artifact.get_xpath_condition())
            elements = pom.xpath_query(xpath)
            for element in elements:
                pom.replace_xml(element, "<!-- dependency removed by maintainer -->")
        except PomQueryNoMatch:
            raise PomException("Dependency '{0}' not found.".format(dep))

    @staticmethod
    def pom_remove_plugin(plugin, pom=None):
        try:
            artifact = Artifact('groupId:artifactId:version').load(plugin)
            xpath = "//pom:plugin[{0}]".format(artifact.get_xpath_condition())
            elements = pom.xpath_query(xpath)
            for element in elements:
                pom.replace_xml(element, "<!-- plugin removed by maintainer -->")
        except PomQueryNoMatch:
            raise PomException("Plugin '{0}' not found.".format(plugin))

    @staticmethod
    def pom_disable_module(module, pom=None):
        try:
            xpath = "//pom:module[normalize-space(text())='{0}']".format(module)
            elements = pom.xpath_query(xpath)
            for element in elements:
                pom.replace_xml(element, "<!-- module removed by maintainer -->")
        except PomQueryNoMatch:
            raise PomException("Module '{0}' not found.".format(module))

    @staticmethod
    def pom_add_parent(parent, pom=None):
        if pom.root.find('pom:parent', namespaces=Pom.NSMAP) is not None:
            raise PomException("POM already has a parent.")
        artifact = Artifact('groupId:artifactId:version', version='any').load(parent)
        pom.inject_artifact('', 'parent', artifact)

    @staticmethod
    def pom_remove_parent(pom=None):
        try:
            pom.replace_xml(pom.xpath_query_element("/pom:project/pom:parent"),
                            "<!-- parent POM reference removed by maintainer -->")
        except PomQueryNoMatch:
            raise PomException("POM doesn't specify parent.")

    @staticmethod
    def pom_set_parent(parent, pom=None):
        try:
            artifact = Artifact('groupId:artifactId:version:scope', version='any').load(parent)
            element = pom.xpath_query_element("/pom:project/pom:parent")
            pom.replace_xml_content(element, artifact.get_xml())
        except PomQueryNoMatch:
            raise PomException("POM doesn't specify parent.")

    @staticmethod
    def pom_add_dep(dep, pom=None, xml_string=''):
        artifact = Artifact('groupId:artifactId:version:scope', version='any').load(dep)
        pom.inject_artifact('pom:dependencies', 'dependency', artifact,
                            xml_string)

    @staticmethod
    def pom_add_dep_mgmt(dep, pom=None, xml_string=''):
        artifact = Artifact('groupId:artifactId:version:scope', version='any').load(dep)
        pom.inject_artifact('pom:dependencyManagement/pom:dependencies',
                            'dependency', artifact, xml_string)

    @staticmethod
    def pom_add_plugin(plugin, pom=None):
        artifact = Artifact('groupId:artifactId:version', version='any',
                            groupId='org.apache.maven.plugins').load(plugin)
        pom.inject_artifact('pom:build/pom:plugins', 'plugin', artifact)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print >> sys.stderr, "Usage:\n\t{0} command {{arguments}}"\
                              .format(sys.argv[0])
        sys.exit(1)

    command = getattr(PomEditor, sys.argv[1])
    patch_poms(command, sys.argv[2:])
