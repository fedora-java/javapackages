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


BEGIN_COMMENT = "<!-- begin of code added by maintainer -->"
END_COMMENT = "<!-- end of code added by maintainer -->"
COMMENT = (BEGIN_COMMENT, END_COMMENT)


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

def find_xml_recursive(xmlspec):
    modules = [find_xml(xmlspec)]
    found = set(modules)
    module_xpath = '/pom:project/pom:modules/pom:module |'\
                   '/pom:project/pom:profile/pom:modules/pom:module'
    try:
        while modules:
            pompath = find_xml(modules.pop())
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
        with open(filename, 'w') as xmlfile:
            xmlfile.write(etree.tostring(self.root))
            xmlfile.write('\n')

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

    def inject_xml(self, parent, content, comment=''):
        content = self.subtree_from_string(content, comment)
        items = len(content)
        parent[:0] = content
        self.reformat(parent, parent[:items])

    def replace_xml(self, replaced, content='', comment=''):
        content = self.subtree_from_string(content, comment)
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

    def replace_xml_content(self, parent, content, comment=''):
        if hasattr(parent, 'is_attribute'):
            if parent.is_attribute:
                parent.getparent().attrib[parent.attrname] = content
                return
        content = self.subtree_from_string(content, comment)
        parent[:] = content
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

    def subtree_from_string(self, xml_string, comment=('', ''), root='root'):
        if type(comment) == tuple:
            begin, end = comment
        else:
            begin, end = comment, ''
        document = "<{root} {ns}>{begin}{0}{end}</{root}>".format(xml_string,
                    root=root, ns=self.XMLNS, begin=begin, end=end)
        try:
            tree = etree.fromstring(document)
        except etree.XMLSyntaxError as error:
            raise PomException("Syntax error in injected XML: {0}.".format(error))
        return tree

    def make_path(self, node, elements):
        if elements:
            child = node.find(elements[0], namespaces=self.NSMAP)
            if child is None:
                name = elements[0]
                for ns, url in self.NSMAP.iteritems():
                    ns_token = ns + ':'
                    url_token = '{' + url + '}'
                    name = name.replace(ns_token, url_token)
                child = etree.Element(name)
                node.insert(0, child)
                node.insert(0, etree.Comment(" section added by maintainer "))
                self.reformat(node, node[:2])
            return self.make_path(child, elements[1:])
        return node

class Pom(XmlFile):
    default_name = 'pom.xml'
    NSMAP = {'pom': 'http://maven.apache.org/POM/4.0.0',
              'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    NS = '{' + NSMAP['pom'] + '}'
    XMLNS = ('xmlns="http://maven.apache.org/POM/4.0.0"'
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
    'xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 '
    'http://maven.apache.org/xsd/maven-4.0.0.xsd"')

    def __init__(self, pompath):
        super(Pom, self).__init__(pompath)

    def _load_file(self):
        with open(self.xmlpath) as pomfile:
            pom = re.sub(r'\<\s*project\s*\>',
                    ('<project {ns}>').format(ns=self.XMLNS), pomfile.read())
        self.root = etree.fromstring(pom)


    def inject_artifact(self, where, node_name, artifact, aux_content=''):
        path_parts = [part for part in where.split('/') if part]
        parent = self.make_path(self.root, path_parts)
        self.inject_xml(parent, "<{name}>{content} {aux}</{name}>"\
                                .format(name=node_name,
                                        content=artifact.get_xml(),
                                        aux=aux_content),
                                comment=COMMENT)

artifact_spec = 'groupId:artifactId:version'
artifact_spec_scoped = artifact_spec + ':scope'
VersionedArtifact = MetaArtifact(artifact_spec)
DefaultVersionedArtifact = MetaArtifact(artifact_spec, version='any')
ScopedArtifact = MetaArtifact(artifact_spec_scoped)
DefaultScopedArtifact = MetaArtifact(artifact_spec_scoped, version='any')

def create_xml_object(filepath):
    tree = etree.parse(filepath)
    root = tree.getroot()
    pom_detect = '/pom:project/pom:modelVersion|/project/modelVersion'
    if root.xpath(pom_detect, namespaces=Pom.NSMAP):
        return Pom(filepath)
    if root.tag == 'ivy-module':
        pass
    return XmlFile(filepath)

def macro(types=(XmlFile,)):
    def decorator(function):
        def decorated(*args):
            try:
                xmlpath = None
                options, fnargs, xmls = parse_args(function, args)

                for xmlspec in xmls:
                    if options.recursive:
                        xmlpaths = find_xml_recursive(xmlspec)
                    else:
                        xmlpaths = [find_xml(xmlspec)]

                    matches = 0
                    for xmlpath in xmlpaths:
                        try:
                            xml = create_xml_object(xmlpath)
                            if not any(isinstance(xml, allowed) for allowed in types):
                                raise PomException('Operation not supported on '
                                                   'given file type.')
                            fnargs['pom'] = xml
                            xml.patch(function, fnargs)
                            matches += 1
                        except PomQueryNoMatch as exception:
                            pass
                    if matches == 0 and not options.force:
                        raise exception

            except (PomException, etree.XMLSyntaxError, IOError, TypeError) as exception:
                if xmlpath:
                    print >> sys.stderr, "Error in processing {0}".format(xmlpath)
                print >> sys.stderr, exception.message
                print_usage(function)
                sys.exit(3)

        macros[function.__name__] = decorated
        return decorated
    return decorator


@macro()
def pom_xpath_inject(where, xml_string, pom=None):
    """<XPath> [XML code] [POM location]"""
    for element in pom.xpath_query(where):
        pom.inject_xml(element, xml_string, comment=COMMENT)

@macro()
def pom_xpath_replace(where, xml_string, pom=None):
    """<XPath> <XML code> [POM location]"""
    for element in pom.xpath_query(where):
        pom.replace_xml(element, xml_string, comment=COMMENT)

@macro()
def pom_xpath_remove(where, pom=None):
    """<XPath> [POM location]"""
    for element in pom.xpath_query(where):
        pom.replace_xml(element,
                comment="<!-- element removed by maintainer: {0} -->".format(where))

@macro()
def pom_xpath_set(where, content, pom=None):
    """<XPath> <new contents> [POM location]"""
    for element in pom.xpath_query(where):
        pom.replace_xml_content(element, content, comment=COMMENT)

@macro()
def pom_remove_dep(dep, pom=None):
    """[groupId]:[artifactId] [POM location]"""
    try:
        artifact = VersionedArtifact.from_mvn_str(dep)
        xpath = "//pom:dependency[{0}]".format(artifact.get_xpath_condition())
        elements = pom.xpath_query(xpath)
        for element in elements:
            pom.replace_xml(element,
                    comment="<!-- dependency removed by maintainer: {0} -->".format(dep))
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Dependency '{0}' not found.".format(dep))

@macro(types=(Pom,))
def pom_remove_plugin(plugin, pom=None):
    """[groupId]:[artifactId] [POM location]"""
    try:
        artifact = VersionedArtifact.from_mvn_str(plugin)
        xpath = "//pom:plugin[{0}]".format(artifact.get_xpath_condition())
        elements = pom.xpath_query(xpath)
        for element in elements:
            pom.replace_xml(element,
                    comment="<!-- plugin removed by maintainer: {0} -->".format(plugin))
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Plugin '{0}' not found.".format(plugin))

@macro(types=(Pom,))
def pom_disable_module(module, pom=None):
    """<module name> [POM location]"""
    try:
        xpath = "//pom:module[normalize-space(text())='{0}']".format(module)
        elements = pom.xpath_query(xpath)
        for element in elements:
            pom.replace_xml(element,
                    comment="<!-- module removed by maintainer: {0} -->".format(module))
    except PomQueryNoMatch:
        raise PomQueryNoMatch("Module '{0}' not found.".format(module))

@macro(types=(Pom,))
def pom_add_parent(parent, pom=None):
    """groupId:artifactId[:version] [POM location]"""
    if pom.root.find('pom:parent', namespaces=Pom.NSMAP) is not None:
        raise PomException("POM already has a parent.")
    artifact = DefaultVersionedArtifact.from_mvn_str(parent)
    pom.inject_artifact('', 'parent', artifact)

@macro(types=(Pom,))
def pom_remove_parent(pom=None):
    """[POM location]"""
    try:
        pom.replace_xml(pom.xpath_query_element("/pom:project/pom:parent"),
                        comment="<!-- parent POM reference removed by maintainer -->")
    except PomQueryNoMatch:
        raise PomQueryNoMatch("POM doesn't specify parent.")

@macro(types=(Pom,))
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

@macro(types=(Pom,))
def pom_add_dep_mgmt(dep, pom=None, xml_string=''):
    """groupId:artifactId[:version[:scope]] [POM location] [extra XML]"""
    artifact = DefaultScopedArtifact.from_mvn_str(dep)
    pom.inject_artifact('pom:dependencyManagement/pom:dependencies',
                        'dependency', artifact, xml_string)

@macro(types=(Pom,))
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
