#-
from __future__ import print_function

import inspect
import re
import shutil
import sys
import optparse
import pyxb.utils.six as six
import io

from lxml import etree
from os import path
from textwrap import dedent

# all macro fuctions that can be called from external world
macros = {}


BEGIN_COMMENT = etree.Comment(' begin of code added by maintainer ')
END_COMMENT = etree.Comment(' end of code added by maintainer ')

def annotate(elements):
    if isinstance(elements, etree._Element):
        elements[:0] = [BEGIN_COMMENT]
        elements.append(END_COMMENT)
        return elements
    return [BEGIN_COMMENT] + elements + [END_COMMENT]

class PomException(Exception):
    pass
class PomQueryNoMatch(PomException):
    pass
class PomQueryAmbigous(PomException):
    pass
class PomQueryInvalid(PomException):
    pass

def MetaArtifact(specification, attributes=False, namespace=None, **defaults):
    parts = specification.split(':')
    class Artifact(object):
        def __init__(self, **values):
            self.values = values

        @classmethod
        def from_mvn_str(cls, string):
            values = {}
            for key, value in zip(parts, string.split(':')):
                if value:
                    values[key] = value
            return cls(**values)

        def update(self, artifact):
            for key, value in six.iteritems(artifact.values):
                if key not in parts:
                    raise KeyError(key + ' not defined')
                if value:
                    self[key] = value

        def remove_items(self, fn):
            for prop, val in six.iteritems(dict(self.values)):
                if fn(val):
                    del self.values[prop]

        def __getitem__(self, key):
            return self.values.get(key, '')

        def __setitem__(self, key, value):
            if key not in parts:
                raise KeyError(key + ' not defined')
            self.values[key] = value

    class NodeArtifact(Artifact):
        @classmethod
        def from_xml(cls, element):
            values = {}
            for part in parts:
                if namespace:
                    subelements = element.xpath('ns:' + part,
                                               namespaces={'ns': namespace})
                else:
                    subelements = element.xpath(part)
                if subelements:
                    values[part] = subelements[0].text.strip()
            return cls(**values)

        def get_xml(self, node='artifact', extra=''):
            xml = ['<{0}>'.format(node)]
            for key in parts:
                value = self.values.get(key, defaults.get(key, ''))
                if value:
                    xml.append("<{0}>{1}</{0}>".format(key, value))
            xml.append(extra)
            xml.append('</{0}>'.format(node))
            return etree.fromstring('\n'.join(xml))

        def get_xpath_condition(self):
            expr = "normalize-space(pom:{0})='{1}'"
            conditions = []
            for key in parts:
                value = self.values.get(key, '')
                if value and value != '*':
                    conditions.append(expr.format(key, value))
            return ' and '.join(conditions) if conditions else 'true()'

    class AttributeArtifact(Artifact):
        @classmethod
        def from_xml(cls, element):
            values = dict([(key, val) for key, val
                          in six.iteritems(element.attrib) if key in parts])
            return cls(**values)

        def get_xml(self, node='artifact', extra=''):
            xml = []
            for key in parts:
                value = self.values.get(key, defaults.get(key, ''))
                if value:
                    xml.append('{0}="{1}"'.format(key, value))
            return etree.fromstring('<{0} {1}>{2}</{0}>'.format(node,
                ' '.join(xml), extra))

        def get_xpath_condition(self):
            expr = "@{0}='{1}'"
            conditions = []
            for key in parts:
                value = self.values.get(key, '')
                if value and value != '*':
                    conditions.append(expr.format(key, value))
            return ' and '.join(conditions) if conditions else 'true()'

    return AttributeArtifact if attributes else NodeArtifact

def find_xml(xmlpath):
    if path.isfile(xmlpath):
        return xmlpath
    if path.isdir(xmlpath):
        subxmlpath = path.join(xmlpath, 'pom.xml')
        if path.isfile(subxmlpath):
            return subxmlpath
        subxmlpath = path.join(xmlpath, 'ivy.xml')
        if path.isfile(subxmlpath):
            return subxmlpath
    raise PomException("Couldn't locate XML file using pattern '{0}'"\
                        .format(xmlpath))

def submodule_info(module_xml, module_path):
    module_xpath = '/pom:project/pom:modules/pom:module |'\
                   '/pom:project/pom:profile/pom:modules/pom:module'
    submodules = module_xml.xpath(module_xpath, namespaces=Pom.NSMAP)
    submodules = [node.text.strip() for node in submodules]
    if module_path:
        submod_paths = [path.join(path.dirname(module_path), submod)
                        for submod in submodules]
    else:
        submod_paths = list(submodules)
    return submodules, submod_paths

def find_xml_recursive(module_path):
    try:
        module_path = find_xml(module_path)
        module_xml = etree.parse(module_path)
        _, submod_paths = submodule_info(module_xml, module_path)
        found = [module_path]
        for submod_path in submod_paths:
            found += find_xml_recursive(submod_path)
        return found
    except IOError:
        raise PomException("Cannot read POM file '{0}'".format(module_path))

def get_indent(node):
    if node is None or not node.text:
        return ''
    text = node.text.split('\n')[-1]
    return re.sub(r'\S.*', '', text)

def print_usage(function):
    print("Usage: %{name} {doc}".format(name=function.__name__, doc=function.__doc__),
          file=sys.stderr)

def parse_args(function, args):
    (arglist, _, _, defaults) = inspect.getargspec(function)
    option_parser = optparse.OptionParser()
    option_parser.add_option('-r', '--recursive', action="store_true")
    option_parser.add_option('-f', '--force', action="store_true")
    options, arguments = option_parser.parse_args(list(args))
    min_arg_count = len(arglist) - len(defaults)
    if len(arguments) < min_arg_count:
        raise PomException('Too few arguments given to {0}'.format(function.__name__))
    fnargs = dict(zip(arglist, arguments[:min_arg_count]))
    poms = arguments[min_arg_count:]
    if len(defaults or [] > 1) and poms:
        last = poms[-1]
        if '<' in last:
            del poms[-1]
            fnargs[arglist[-1]] = last
    if not poms:
        poms = ['.']
    return options, fnargs, poms

class XmlFile(object):
    default_name = None
    NSMAP = {}
    XMLNS = ''

    def __init__(self, xmlpath):
        self.xmlpath = xmlpath
        self.root = None
        self._load_file()
        self.tab = get_indent(self.root)

    def _load_file(self):
        self.root = etree.parse(self.xmlpath).getroot()

    def write(self, filename):
        with open(filename, 'wb') as xmlfile:
            xmlfile.write(etree.tostring(self.root))
            xmlfile.write(b'\n')

    def patch(self, function, fnargs):
        xmldir = path.dirname(self.xmlpath)
        xmlfile = path.basename(self.xmlpath)
        try:
            self.write(path.join(xmldir, xmlfile + '.tmp'))
            function(**fnargs)
        finally:
            origfile = path.join(xmldir, xmlfile + '.orig')
            shutil.move(self.xmlpath, origfile)
            self.write(self.xmlpath)

    def inject_xml(self, parent, content):
        items = len(content)
        parent[:0] = content
        self.reformat(parent, parent[:items])

    def replace_xml(self, replaced, content):
        parent = replaced.getparent()
        if not isinstance(replaced, etree._Element):
            parent.extend(content)
            if content.tag is not etree.Comment:
                parent.text = content.text
            return
        idx = parent.index(replaced)
        items = len(content)
        del parent[idx]
        for i, element in enumerate(content):
            parent.insert(idx + i, element)
        self.reformat(parent, parent[idx: idx + items])

    def replace_xml_content(self, parent, content, replace_attrib=False):
        if hasattr(parent, 'is_attribute'):
            if parent.is_attribute:
                parent.getparent().attrib[parent.attrname] = content.text
                return
        parent[:] = content
        if replace_attrib and hasattr(content, 'attrib'):
            parent.attrib.clear()
            parent.attrib.update(content.attrib.iteritems())
        parent.text = content.text
        self.reformat(parent, parent)

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
        return query_result[0]

    def xpath_query(self, query, boolean=False):
        if not query.startswith('/'):
            query = '//' + query
        if boolean:
            query = 'boolean({0})'.format(query)
        try:
            nsmap = dict(self.NSMAP)
            nsmap.update(self.root.nsmap)
            if None in nsmap:
                nsmap['default'] = nsmap[None]
                del nsmap[None]
            query_result = self.root.xpath(query, namespaces=nsmap)
        except etree.XPathEvalError as error:
            raise PomQueryInvalid("XPath query '{0}': {1}.".format(query,
                                                               error))
        if not boolean:
            if len(query_result) == 0:
                raise PomQueryNoMatch(dedent("""\
                        XPath query '{0}' didn't match any node.
                        (Did you forget to specify 'pom:' namespace?)""").format(query))
            for i, element in enumerate(query_result):
                if hasattr(element, 'is_attribute') and element.is_attribute:
                    if not hasattr(element, 'attrname'):
                        element.attrname = self.root.xpath('name({q}[{i1}])'.format(q=query, i1=i + 1),
                                                           namespaces=nsmap)
        return query_result

    def subtree_from_string(self, xml_string):
        document = "<root {ns}>{0}</root>".format(xml_string, ns=self.XMLNS)
        try:
            tree = etree.fromstring(document)
        except etree.XMLSyntaxError as error:
            raise PomException("Syntax error in injected XML: {0}.".format(error))
        return tree

    def make_path(self, node, elements):
        if elements:
            elem = elements[0]
            children = node.xpath(elem, namespaces=self.NSMAP)
            if not children:
                name = elements[0]
                for ns, url in six.iteritems(self.NSMAP):
                    ns_token = ns + ':'
                    url_token = '{' + url + '}'
                    name = name.replace(ns_token, url_token)
                child = etree.Element(name)
                node.insert(0, child)
                node.insert(0, etree.Comment(" section added by maintainer "))
                self.reformat(node, node[:2])
            else:
                child = children[0]
            return self.make_path(child, elements[1:])
        return node

    def inject_artifact(self, where, node_name, artifact, aux_content=''):
        path_parts = [part for part in where.split('/') if part]
        parent = self.make_path(self.root, path_parts)
        content = annotate([artifact.get_xml(node_name, aux_content)])
        self.inject_xml(parent, content)


class Pom(XmlFile):
    default_name = 'pom.xml'
    NSMAP = {'pom': 'http://maven.apache.org/POM/4.0.0',
              'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    NS = '{' + NSMAP['pom'] + '}'
    XMLNS = ('xmlns="http://maven.apache.org/POM/4.0.0" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
    'xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 '
    'http://maven.apache.org/xsd/maven-4.0.0.xsd"')
    DEPENDENCY_NODE = 'pom:dependency'
    DEPENDENCIES_NODE = 'pom:dependencies'

    def __init__(self, pompath):
        super(Pom, self).__init__(pompath)

    def _load_file(self):
        with io.open(self.xmlpath, encoding="UTF-8") as pomfile:
            pom = re.sub(r'\<\s*project\s*\>',
                         u'<project {ns}>'.format(ns=self.XMLNS), pomfile.read())
        self.root = etree.fromstring(pom.encode("utf-8"))

    @classmethod
    def create_artifact(cls, *args, **kwargs):
        plugin = kwargs.get('plugin', False)
        if 'plugin' in kwargs:
            del kwargs['plugin']
        if plugin:
            pom_plugin_spec = 'groupId:artifactId:version'
            ArtifactClass = MetaArtifact(pom_plugin_spec,
                                         namespace=cls.NSMAP['pom'],
                                         version='any',
                                         groupId='org.apache.maven.plugins')
        else:
            pom_dependency_spec = 'groupId:artifactId:version:scope'
            ArtifactClass = MetaArtifact(pom_dependency_spec,
                                         namespace=cls.NSMAP['pom'],
                                         version='any')
        return ArtifactClass(*args, **kwargs)


class Ivy(XmlFile):
    DEPENDENCY_NODE = 'dependency'
    DEPENDENCIES_NODE = 'dependencies'

    def __init__(self, pompath):
        super(Ivy, self).__init__(pompath)

    @classmethod
    def create_artifact(cls, *args, **kwargs):
        if 'plugin' in kwargs:
            del kwargs['plugin']
        ivy_dependency_spec = 'org:name:rev:conf:transitive'
        IvyDependency = MetaArtifact(ivy_dependency_spec, attributes=True)
        return IvyDependency(*args, **kwargs)


def create_xml_object(filepath):
    tree = etree.parse(filepath)
    root = tree.getroot()
    pom_detect = '/pom:project/pom:modelVersion|/project/modelVersion'
    if root.xpath(pom_detect, namespaces=Pom.NSMAP):
        return Pom(filepath)
    if root.tag == 'ivy-module':
        return Ivy(filepath)
    return XmlFile(filepath)

def macro(types=(XmlFile,)):
    def decorator(function):
        def decorated(*args):
            try:
                xmlpath = None
                options, fnargs, xmls = parse_args(function, args)

                stored_exception = None
                for xmlspec in xmls:
                    if options.recursive:
                        xmlpaths = find_xml_recursive(xmlspec)
                    else:
                        xmlpaths = [find_xml(xmlspec)]

                    matches = 0
                    for xmlpath in xmlpaths:
                        try:
                            xml = create_xml_object(xmlpath)
                            if not any([isinstance(xml, allowed) for allowed in types]):
                                raise PomException('Operation not supported on '
                                                   'given file type.')
                            fnargs['pom'] = xml
                            xml.patch(function, fnargs)
                            matches += 1
                        except PomQueryNoMatch as exception:
                            stored_exception = exception
                    if matches == 0 and not options.force:
                        # pylint: disable=E0702
                        raise stored_exception

            except (PomException, etree.XMLSyntaxError, IOError) as exception:
                if xmlpath:
                    print("Error in processing {0}".format(xmlpath), file=sys.stderr)
                print(exception, file=sys.stderr)
                print_usage(function)
                sys.exit(3)

        macros[function.__name__] = decorated
        return decorated
    return decorator

def disable_module(pom, module):
    xpath = "//pom:module[normalize-space(text())='{0}']".format(module)
    elements = pom.xpath_query(xpath)
    for element in elements:
        pom.replace_xml(element, etree.Comment(" module removed by maintainer: {0} ".format(module)))

@macro()
def pom_xpath_inject(where, xml_string, pom=None):
    """<XPath> [XML code] [POM location]"""
    for element in pom.xpath_query(where):
        pom.inject_xml(element, annotate(pom.subtree_from_string(xml_string)))

@macro()
def pom_xpath_replace(where, xml_string, pom=None):
    """<XPath> <XML code> [POM location]"""
    for element in pom.xpath_query(where):
        pom.replace_xml(element, annotate(pom.subtree_from_string(xml_string)))

@macro()
def pom_xpath_remove(where, pom=None):
    """<XPath> [POM location]"""
    for element in pom.xpath_query(where):
        if hasattr(element, 'is_attribute') and element.is_attribute:
            del element.getparent().attrib[element.attrname]
        else:
            pom.replace_xml(element, etree.Comment(" element removed by maintainer: {0} ".format(where)))

@macro()
def pom_xpath_set(where, content, pom=None):
    """<XPath> <new contents> [POM location]"""
    for element in pom.xpath_query(where):
        pom.replace_xml_content(element, pom.subtree_from_string(content))

@macro(types=(Pom,))
def pom_xpath_disable(when, pom=None):
    """<XPath> [POM location]"""
    to_disable = []
    def disable_recursive(pom):
        if pom.xpath_query(when, boolean=True):
            return True
        for submodule, submod_path in zip(*submodule_info(pom.root, pom.xmlpath)):
            realpath = find_xml(submod_path)
            subpom = Pom(realpath)
            if disable_recursive(subpom):
                to_disable.append((pom, submodule))

    if disable_recursive(pom):
        raise PomException("Main POM satisfies the condition")
    if not to_disable:
        raise PomQueryNoMatch("Condition didn't match any module")
    for pom, module in to_disable:
        pom.patch(disable_module, {'pom': pom, 'module': module})

@macro(types=(Pom, Ivy))
def pom_remove_dep(dep, pom=None):
    """[groupId]:[artifactId] [POM location]"""
    try:
        artifact = pom.create_artifact().from_mvn_str(dep)
        xpath = "//{0}[{1}]".format(pom.DEPENDENCY_NODE, artifact.get_xpath_condition())
        elements = pom.xpath_query(xpath)
        for element in elements:
            pom.replace_xml(element, etree.Comment(" dependency removed by maintainer: {0} ".format(dep)))
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Dependency '{0}' not found.".format(dep))

@macro(types=(Pom,))
def pom_remove_plugin(plugin, pom=None):
    """[groupId]:[artifactId] [POM location]"""
    try:
        artifact = pom.create_artifact(plugin=True).from_mvn_str(plugin)
        xpath = "//pom:plugin[{0}]".format(artifact.get_xpath_condition())
        elements = pom.xpath_query(xpath)
        for element in elements:
            pom.replace_xml(element, etree.Comment(" plugin removed by maintainer: {0} ".format(plugin)))
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Plugin '{0}' not found.".format(plugin))

@macro(types=(Pom,))
def pom_disable_module(module, pom=None):
    """<module name> [POM location]"""
    try:
        disable_module(pom, module)
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Module '{0}' not found.".format(module))

@macro(types=(Pom,))
def pom_add_parent(parent, pom=None):
    """groupId:artifactId[:version] [POM location]"""
    if pom.xpath_query('/pom:parent', boolean=True):
        raise PomException("POM already has a parent.")
    artifact = pom.create_artifact().from_mvn_str(parent)
    pom.inject_artifact('', 'parent', artifact)

@macro(types=(Pom,))
def pom_remove_parent(pom=None):
    """[POM location]"""
    try:
        pom.replace_xml(pom.xpath_query_element("/pom:project/pom:parent"),
                        etree.Comment(" parent POM reference removed by maintainer --> "))
    except PomQueryNoMatch:
        raise PomQueryNoMatch("POM doesn't specify parent.")

@macro(types=(Pom,))
def pom_set_parent(parent, pom=None):
    """groupId:artifactId[:version] [POM location]"""
    try:
        artifact = pom.create_artifact().from_mvn_str(parent)
        element = pom.xpath_query_element("/pom:project/pom:parent")
        pom.replace_xml_content(element, artifact.get_xml())
    except PomQueryNoMatch:
        raise PomQueryNoMatch("POM doesn't specify parent.")

@macro(types=(Pom, Ivy))
def pom_add_dep(dep, pom=None, xml_string=''):
    """groupId:artifactId[:version[:scope]] [POM location] [extra XML]"""
    artifact = pom.create_artifact().from_mvn_str(dep)
    pom.inject_artifact(pom.DEPENDENCIES_NODE, 'dependency', artifact,
                        xml_string)

@macro(types=(Pom,))
def pom_add_dep_mgmt(dep, pom=None, xml_string=''):
    """groupId:artifactId[:version[:scope]] [POM location] [extra XML]"""
    artifact = pom.create_artifact().from_mvn_str(dep)
    pom.inject_artifact('pom:dependencyManagement/pom:dependencies',
                        'dependency', artifact, xml_string)

@macro(types=(Pom,))
def pom_add_plugin(plugin, pom=None, xml_string=''):
    """groupId:artifactId[:version] [POM location] [extra XML]"""
    artifact = pom.create_artifact(plugin=True).from_mvn_str(plugin)
    pom.inject_artifact('pom:build/pom:plugins', 'plugin', artifact,
                        xml_string)

@macro()
def pom_change_dep(old, new, pom=None, xml_string=''):
    """groupId:artifactId[:version] groupId:artifactId[:version[:scope]]
       [POM location] [extra XML]"""
    try:
        old_artifact = pom.create_artifact().from_mvn_str(old)
        xpath = "//{0}[{1}]".format(pom.DEPENDENCY_NODE, old_artifact.get_xpath_condition())
        elements = pom.xpath_query(xpath)
        for element in elements:
            new_artifact = pom.create_artifact().from_xml(element)
            new_artifact.update(pom.create_artifact().from_mvn_str(new))
            new_artifact.remove_items(lambda x: x == '-')
            new_xml = new_artifact.get_xml(extra=xml_string)
            pom.replace_xml_content(element, new_xml, replace_attrib=True)
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Dependency '{0}' not found.".format(old))

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Usage:\n\t{0} command {{arguments}}".format(sys.argv[0]),
              file=sys.stderr)
        sys.exit(1)

    macros[sys.argv[1]](*sys.argv[2:])
