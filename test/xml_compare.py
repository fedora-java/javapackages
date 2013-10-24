from lxml import etree
import sys
import re

def compare_xml_files(file1, file2, unordered=None):
    """ Compares two XML files and returns empty string if they're identical
    and string with differences otherwise. Optional third argument specifies
    which elements should be compared without taking element order into
    account. It is represented by list of xpath-like epressions with * as a
    wildcard.
    Examples: ['*'] for unordered comparison of all elements.
              ['/html/head'] for unordered comparison of children of <head>
                    element under the root <html>
              ['p'] for unordered comparison of children of every <p> element
    """
    return compare_lxml_etree(etree.parse(file1).getroot(),
            etree.parse(file2).getroot(), unordered)

def compare_lxml_etree(doc1, doc2, unordered=None):
    """ Compares two XML documents (lxml.etree) and returns empty string if
    they're identical and string with differences otherwise. Optional third
    argument specifies which elements should be compared without taking element
    order into account. It is represented by list of xpath-like epressions with
    * as a wildcard.
    Examples: ['*'] for unordered comparison of all elements.
              ['/html/head'] for unordered comparison of children of <head>
                    element under the root <html>
              ['p'] for unordered comparison of children of every <p> element
    """

    paths = _create_paths(unordered)

    _strip_comments(doc1)
    _strip_comments(doc2)

    lines = []
    for sgn, line in _compare_element(doc1, doc2, unordered_paths = paths):
        lines.append('{sgn}{line}'.format(sgn=sgn, line=line))

    return '\n'.join(lines)

def _strip_comments(doc):
    for node in doc.iter():
        if node.tag == etree.Comment:
            parent = node.getparent()
            parent.remove(node)

def _localname(tag):
    return etree.QName(tag).localname

def _compare_element(exp, act, unordered_paths=None):
    if exp.tag != act.tag:
        return _print_element(exp, '-') + _print_element(act, '+')

    tag = _localname(exp.tag)
    new_unordered = _descend_paths(unordered_paths, tag)
    def callback(exp, act):
        return _compare_element(exp, act, unordered_paths=new_unordered)

    if _matches_paths(unordered_paths, tag):
        child_rep = _tab(_compare_children_unordered(exp, act, callback))
    else:
        child_rep = _tab(_compare_children_ordered(exp, act, callback))

    attr_rep = _tab(_compare_attrs(exp, act))
    text_rep = _tab(_compare_text(exp.text, act.text))
    tail_rep = _compare_text(exp.tail, act.tail)

    if attr_rep or child_rep or text_rep:
        rep = []
        end = ''
        if not attr_rep:
            end = '>' if child_rep or text_rep else '/>'

        rep.append((' ', '<{tag}{end}'.format(tag=tag, end=end)))

        if attr_rep:
            rep += attr_rep
            rep.append((' ', '>' if child_rep or text_rep else '/>'))

        if child_rep or text_rep:
            rep.extend(text_rep)
            rep.extend(child_rep)
            rep.append((' ', '</{tag}>'.format(tag=tag)))

        rep.extend(tail_rep)
        return rep
    else:
        if tail_rep:
            return [(' ', '<{tag} .../>'.format(tag=tag))] + tail_rep
        else: return []

class _Path(object):
    def __init__(self, parts, relative=False):
        self.parts = list(parts)
        self.relative = relative

    def matches_start(self, tagname):
        exp = re.escape(self.parts[0])
        exp = re.sub(r'\\\*', '.*', exp)
        return re.match(exp + '$', tagname)

    def matches(self, tagname):
        return len(self.parts) == 1 and self.matches_start(tagname)

    def descend(self):
        if len(self.parts) > 1:
            return _Path(self.parts[1:])

def _create_paths(paths):
    res = []
    for path in paths or []:
        if path.startswith('/'):
            parts = path.split('/')[1:]
            res.append(_Path(parts))
        else:
            parts = path.split('/')
            res.append(_Path(parts))
            res.append(_Path(parts, relative=True))
    return res

def _matches_paths(paths, tagname):
    for path in paths or []:
        if path.matches(tagname):
            return True
    return False

def _descend_paths(paths, tagname):
    res = []
    for path in paths or []:
        if path.relative:
            res.append(path)
            if path.matches_start(tagname):
                descendant = path.descend()
                if descendant:
                    res.append(descendant)
        else:
            descendant = path.descend()
            if descendant:
                res.append(descendant)
    return res

def _tab(lst):
    return [(sgn, '    ' + line) for sgn, line in lst]

def _print_element(elem, prefix):
    if elem is None:
        return
    rep = []
    attrs = ['{k}="{v}"'.format(k=k, v=v) for k, v in elem.attrib.iteritems()]
    tag = _localname(elem.tag)
    if len(elem) or elem.text:
        rep.append('<{elem}{attrs}>'.format(elem=tag,
            attrs=(' ' + ' '.join(attrs)) if attrs else ''))
        if elem.text and elem.text.strip():
            rep.append('    ' + elem.text.strip())
        rep += ['    ' + line for child in elem for
                _, line in _print_element(child, prefix)]
        rep.append('</{elem}>'.format(elem=tag))
    else:
        rep.append('<{elem}{attrs}/>'.format(elem=tag,
            attrs=(' ' + ' '.join(attrs)) if attrs else ''))
    return [(prefix, line) for line in rep]

def _compare_children_unordered(exp, act, cmp_f):
    r_matched = set()
    index = []

    for i, lchild in enumerate(exp):
        first = None
        for j, rchild in enumerate(act):
            if j not in r_matched:
                if lchild.tag == rchild.tag:
                    subrep = cmp_f(lchild, rchild)
                    if not subrep:
                        r_matched.add(j)
                        break
                    elif not first:
                        first = (j, subrep)
        else:
            if first:
                j, subrep = first
                r_matched.add(j)
                index.append((i, subrep))
            else:
                index.append((i, _print_element(lchild, '-')))

    for j, rchild in enumerate(act):
        if j not in r_matched:
            index.append((j, _print_element(rchild, '+')))

    return _get_items_from_index(index)

def _get_items_from_index(index):
    items = []
    for _, item in sorted(index, key=lambda tup: tup[0]):
        items += item
    return items

def _compare_children_ordered(exp, act, cmp_f):
    rep = []
    for i, lchild in enumerate(exp):
        if i < len(act):
            rep += cmp_f(lchild, act[i])
        else:
            rep += _print_element(lchild, '-')
    for i in range(len(exp), len(act)):
        rep += _print_element(act[i], '+')
    return rep

def _compare_text(text1, text2):
    text1 = text1.strip() if text1 else None
    text2 = text2.strip() if text2 else None
    rep = []
    if text1 != text2:
        if text1:
            rep.append(('-', text1))
        if text2:
            rep.append(('+', text2))
    return rep

def _compare_attrs(exp, act):
    rep = []
    attrib1, attrib2 = exp.attrib, act.attrib

    for k, lchild in attrib1.iteritems():
        if k in attrib2:
            if attrib2[k] != lchild:
                rep.append(('-', '{name} = "{value}"'\
                        .format(name=k, value=lchild)))
                rep.append(('+', '{name} = "{value}"'\
                        .format(name=k, value=attrib2[k])))
        else:
            rep.append(('-', '{name} = "{value}"'.format(name=k, value=lchild)))

    for k, lchild in attrib2.iteritems():
        if k not in attrib1:
            rep.append(('+', '{name} = "{value}"'.format(name=k, value=lchild)))

    return rep

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ('Usage {name} filexp filact ' +
            '[unordered_elements path specification]').format(name=sys.argv[0])
        sys.exit(1)
    print compare_xml_files(sys.argv[1], sys.argv[2], sys.argv[3:])

