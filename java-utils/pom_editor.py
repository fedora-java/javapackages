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

POM_NS = {'pom': 'http://maven.apache.org/POM/4.0.0',
          'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

class Artifact(object):
    def __init__(self, specification):
        tokens = specification.split(':')
        self.parts = [(token, '') for token in tokens]

    def load(self, string):
        tokens = string.split(':')
        if len(tokens) > len(self.parts):
            raise PomException("Too many colons in artifact specification '{0}'."\
                                .format(string))
        for i, token in enumerate(tokens):
            key, _ = self.parts[i]
            self.parts[i] = (key, token)
        return self

    def get_xml(self):
        xml = ''
        for key, value in self.parts:
            if value:
                xml += "<{0}>{1}</{0}>".format(key, value)
        return xml

    def get_xpath_condition(self):
        expr = "normalize-space(pom:{0})='{1}'"
        conditions = []
        for key, value in self.parts:
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

def xpath_query(pom_tree, query):
    if not query.startswith('/'):
        query = '//' + query
    try:
        query_result = pom_tree.xpath(query, namespaces=POM_NS)
    except etree.XPathEvalError as error:
        raise PomQueryInvalid("XPath query '{0}': {1}.".format(query,
                                                           error.message))
    if len(query_result) == 0:
        raise PomQueryNoMatch("XPath query '{0}' didn't match any node."\
                            .format(query))
    elif len(query_result) > 1:
        raise PomQueryAmbigous("XPath query '{0}' matched more than one nodes."\
                            .format(query))
    parent = query_result[0]
    if not isinstance(parent, etree._Element):
        raise PomQueryNoMatch("XPath query '{0}': matched node is not an element"\
                            .format(query))
    return parent

def subtree_from_string(xml_string, root='root'):
    document = "<{root}>{0}</{root}>".format(xml_string, root=root)
    try:
        tree = etree.fromstring(document)
    except etree.XMLSyntaxError as error:
        raise PomException("Syntax error in injected XML: {0}.".format(error))
    return tree

def inject_xml(pom_tree, where, content):
    parent = xpath_query(pom_tree, where)
    if not isinstance(content, etree._Element):
        content = subtree_from_string(content)
    parent[:0] = content

def replace_xml(pom_tree, where, content):
    replaced = xpath_query(pom_tree, where)
    content = subtree_from_string(content)
    parent = replaced.getparent()
    idx = parent.index(replaced)
    del parent[idx]
    for element in content:
        parent.insert(idx, element)
        idx += 1

def replace_xml_content(pom_tree, where, content):
    parent = xpath_query(pom_tree, where)
    content = subtree_from_string(content)
    parent[:0] = content
    parent.text = content.text

def make_path(node, elements):
    if elements:
        child = node.find(elements[0], namespaces=POM_NS)
        if not child:
            child = etree.Element('{ns}{name}'.format(name=elements[0],
                                                      ns=POM_NS['pom']))
            node.append(child)
        return make_path(child, elements[1:])
    return node

def inject_artifact(pom_tree, where, node_name, artifact, aux_content=''):
    parent = make_path(pom_tree, where.split('/'))
    inject_xml(pom_tree, parent,
               "<name>{content} {aux}</name>".format(name=node_name,
                                               content=artifact.get_xml(),
                                               aux=aux_content))

def trim_whitespace(tree):
    for element in tree.iter():
        if element.tail and element.tail.strip() == '':
            element.tail = None
        if element.text and element.text.strip() == '':
            element.text = None

def patch_poms(function, args):
    (arglist, _, _, defaults) = inspect.getargspec(function)
    maxargcount = len(arglist)
    minargcount = maxargcount - len(defaults or [])
    if len(args) > maxargcount or len(args) < minargcount:
        print >> sys.stderr, "Usage: %pom_{name} {doc}".format(name=function.__name__,
                                                         doc=function.__doc__)
        sys.exit(1)
    pomspec_pos = arglist.index('pom_tree')
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
        with open(pompath) as pomfile:
            pom = re.sub(r'\<\s*project\s*\>',
                    ('<project xmlns="{pomns}" xmlns:xsi="{xsins}" '
                     'xsi:schemaLocation="{pomns} '
                     'http://maven.apache.org/xsd/maven-'
                     '4.0.0.xsd">').format(pomns=POM_NS['pom'],
                     xsins=POM_NS['xsi']), pomfile.read())
        tree = etree.fromstring(pom)
        trim_whitespace(tree)
        with open(path.join(pomdir, path.basename(pompath) + '.tmp'), 'w') as tmp:
            tmp.write(etree.tostring(tree, pretty_print=True))
        fnargs = args[:pomspec_pos] + [tree] + args[pomspec_pos + 1:]
        function(*fnargs)
        trim_whitespace(tree)
        newpom = etree.tostring(tree, pretty_print=True)
        origfile = path.join(pomdir, path.basename(pompath) + '.orig')
        shutil.move(pompath, origfile)
        with open(pompath, 'w') as pomfile:
            pomfile.write(newpom)
            pomfile.write('\n')
    except (PomException, OSError, IOError) as exception:
        print >> sys.stderr, "Error in processing {0}".format(pompath)
        print >> sys.stderr, exception.message
        sys.exit(3)

class PomEditor(object):
    @staticmethod
    def pom_xpath_inject(where, xml_string, pom_tree=None):
        inject_xml(pom_tree, where,
                   "<!-- begining of code added by maintainer -->" + xml_string
                   + "<!-- end of code added by maintainer -->")

    @staticmethod
    def pom_xpath_replace(where, xml_string, pom_tree=None):
        replace_xml(pom_tree, where, xml_string)

    @staticmethod
    def pom_xpath_remove(where, pom_tree=None):
        replace_xml(pom_tree, where, "<!-- element removed by maintainer -->")

    @staticmethod
    def pom_xpath_set(where, content, pom_tree=None):
        #TODO check content
        replace_xml_content(pom_tree, where,
                            "<!-- begining of code added by maintainer -->"
                            + content +
                            "<!-- end of code added by maintainer -->")

    @staticmethod
    def pom_remove_dep(dep, pom_tree=None):
        try:
            artifact = Artifact('groupId:artifactId:version').load(dep)
            xpath = "//pom:dependency[{0}]".format(artifact.get_xpath_condition())
            replace_xml(pom_tree, xpath, "<!-- dependency removed by maintainer -->")
        except PomQueryNoMatch:
            raise PomException("Dependency '{0}' not found.".format(dep))
        except PomQueryAmbigous:
            raise PomException("Artifact specification '{0}' matched more "
                               "dependencies.".format(dep))

    @staticmethod
    def pom_remove_plugin(plugin, pom_tree=None):
        try:
            artifact = Artifact('groupId:artifactId:version').load(plugin)
            xpath = "//pom:plugin[{0}]".format(artifact.get_xpath_condition())
            replace_xml(pom_tree, xpath, "<!-- plugin removed by maintainer -->")
        except PomQueryNoMatch:
            raise PomException("Plugin '{0}' not found.".format(plugin))
        except PomQueryAmbigous:
            raise PomException("Artifact specification '{0}' matched more "
                               "plugins.".format(plugin))

    @staticmethod
    def pom_disable_module(module, pom_tree=None):
        try:
            xpath = "//pom:module[normalize-space(text())='{0}']".format(module)
            replace_xml(pom_tree, xpath, "<!-- module removed by maintainer -->")
        except PomQueryNoMatch:
            raise PomException("Module '{0}' not found.".format(module))

    @staticmethod
    def pom_add_parent(parent, pom_tree=None):
        if pom_tree.find('pom:parent', namespaces=POM_NS):
            raise PomException("POM already has a parent.")
        artifact = Artifact('groupId:artifactId:version').load(parent)
        inject_xml(pom_tree, '/pom:project',
                   "<!-- <parent>{0}</parent>".format(artifact.get_xml()))

    @staticmethod
    def pom_remove_parent(pom_tree=None):
        try:
            replace_xml(pom_tree, "/pom:project/pom:parent",
                        "<!-- parent POM reference removed by maintainer -->")
        except PomQueryNoMatch:
            raise PomException("POM doesn't specify parent.")

    @staticmethod
    def pom_set_parent(parent, pom_tree=None):
        try:
            artifact = Artifact('groupId:artifactId:version:scope').load(parent)
            replace_xml_content(pom_tree, "/pom:project/pom:parent",
                                artifact.get_xml())
        except PomQueryNoMatch:
            raise PomException("POM doesn't specify parent.")

    @staticmethod
    def pom_add_dep(dep, pom_tree=None, xml_string=''):
        artifact = Artifact('groupId:artifactId:version:scope').load(dep)
        inject_artifact(pom_tree, 'dependencies', 'dependency', artifact,
                        xml_string)

    @staticmethod
    def pom_add_dep_mgmt(dep, pom_tree=None, xml_string=''):
        artifact = Artifact('groupId:artifactId:version:scope').load(dep)
        inject_artifact(pom_tree, 'dependencies/dependencyManagement',
                        'dependencyManagement', artifact, xml_string)

    @staticmethod
    def pom_add_plugin(plugin, pom_tree=None):
        artifact = Artifact('groupId:artifactId:version').load(plugin)
        inject_artifact(pom_tree, 'plugins', 'plugin', artifact)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print >> sys.stderr, "Usage:\n\t{0} command {{arguments}}"\
                              .format(sys.argv[0])
        sys.exit(1)

    command = getattr(PomEditor, sys.argv[1])
    patch_poms(command, sys.argv[2:])
