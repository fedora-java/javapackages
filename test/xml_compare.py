from lxml import etree
import sys
from collections import defaultdict
import re

def compare_xml_files(file1, file2, unordered=[]):
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
    return compare_xml(etree.parse(file1).getroot(), etree.parse(file2).getroot(), unordered)

def compare_xml(doc1, doc2, unordered=[]):
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
    unord_abs = [path[1:] for path in unordered if path.startswith('/')]
    unord_rel = [path for path in unordered if not path.startswith('/')]

    strip_xml(doc1)
    strip_xml(doc2)

    return '\n'.join(['{sgn}{line}'.format(sgn=sgn, line=line) for sgn, line
            in compare_element(doc1, doc2, unordered_abs=unord_abs + unord_rel, unordered_rel=unord_rel)])

def strip_xml(doc):
    unwanted = [node for node in doc.iter() if node.tag == etree.Comment]

    for c in unwanted:
        p = c.getparent()
        p.remove(c)

def localname(tag):
    return etree.QName(tag).localname

def compare_element(e1, e2, unordered_abs=[], unordered_rel=[]):
    if e1.tag != e2.tag:
        return print_element(e1, '-') + print_element(e2, '+')
    new_abs, unordered = process_paths(unordered_abs, unordered_rel, e1.tag)
    if unordered:
        child_rep = tab(compare_children_unordered(e1, e2,
            lambda a, b: compare_element(a, b, new_abs, unordered_rel)))
    else:
        child_rep = tab(compare_children_ordered(e1, e2,
            lambda a, b: compare_element(a, b, new_abs, unordered_rel)))

    attr_rep = tab(compare_attrs(e1, e2))
    text_rep = tab(compare_text(e1.text, e2.text))
    tail_rep = compare_text(e1.tail, e2.tail)
    tag = localname(e1.tag)

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

def tab(lst):
    return [(sgn, '    ' + line) for sgn, line in lst]

def process_paths(unordered_abs, unordered_rel, tagname):
    tagname = localname(tagname)
    current_paths = [path for path in unordered_abs if path.find('/') == -1]
    new_abs = [path[path.index('/') + 1:] for path in unordered_abs if path.find('/') >= 0]
    new_abs += [path[path.index('/') + 1:] for path in unordered_rel
            if path.find('/') >= 0 and path_matches(tagname, path[:path.index('/')])]
    new_abs += unordered_rel
    unordered = any([path_matches(tagname, path) for path in current_paths])
    return (new_abs, unordered)

def path_matches(path, exp):
    exp = re.escape(exp)
    exp = re.sub(r'\\\*', '.*', exp)
    return re.match(exp + '$', path)

def print_element(e, prefix):
    if e is None:
        return
    rep = []
    attrs = ['{k}="{v}"'.format(k=k, v=v) for k,v in e.attrib.iteritems()]
    t = localname(e.tag)
    if len(e) or e.text:
        rep.append('<{e}{attrs}>'.format(e=t, attrs=(' ' + ' '.join(attrs)) if attrs else ''))
        if e.text and e.text.strip():
            rep.append('    ' + e.text.strip())
        rep += ['    ' + line for child in e for child_rep, line in print_element(child, prefix)]
        rep.append('</{e}>'.format(e=t))
    else:
        rep.append('<{e}{attrs}/>'.format(e=t, attrs=(' ' + ' '.join(attrs)) if attrs else ''))
    return [(prefix, line) for line in rep]

def compare_children_unordered(e1, e2, cmp_f):
    r_matched = set()
    index = []
    for i, v in enumerate(e1):
        first = None
        for j, w in enumerate(e2):
            if j not in r_matched:
                if v.tag == w.tag:
                    subrep = cmp_f(v, w)
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
                index.append((i, print_element(v, '-')))

    for j, w in enumerate(e2):
        if j not in r_matched:
            index.append((j, print_element(w, '+')))
    return [inner for idx, item in sorted(index, key=lambda tup: tup[0]) for inner in item]

def compare_children_ordered(e1, e2, cmp_f):
    rep = []
    for i, v in enumerate(e1):
        if i < len(e2):
            rep += cmp_f(v, e2[i])
        else:
            rep += print_element(v, '-')
    for i in range(len(e1), len(e2)):
        rep += print_element(e2[i], '+')
    return rep

def dictdiff(d1, d2, f_left, f_right, f_both):
    """ Calls f_left on items present in d1 but not in d2, f_right on items
    present in d2 but not in d1 and f_both on items that are present in both
    """
    ret = []
    for k in d1.keys():
        if k in d2:
            ret += f_both(k, d1[k], d2[k])
        else:
            ret += f_left(k, d2[k])
    for k in d2.keys():
        if k not in d1:
            ret += f_right(k, d2[k])
    return ret

def compare_text(t1, t2):
    t1 = t1.strip() if t1 else None
    t2 = t2.strip() if t2 else None
    rep = []
    if t1 != t2:
        if t1:
            rep.append(('-', t1))
        if t2:
            rep.append(('+', t2))
    return rep;

def compare_attrs(e1, e2):
    rep = []
    a1, a2 = e1.attrib, e2.attrib

    def fmt(sign, k, v):
        return (sign, '{k}="{v}"'.format(k=k, v=v))

    rep += dictdiff(a1, a2, lambda k, v: [fmt('-', k, v)],
        lambda k, v: [fmt('+', k ,v)],
        lambda k, v1, v2: [fmt('-', k, v1), fmt('+', k ,v)] if v1 != v2 else [])

    return rep

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage {name} file1 file2 [unordered_elements_path_specifiaction]'.format(name=sys.argv[0])
        sys.exit(1)
    print compare_xml_files(sys.argv[1], sys.argv[2], sys.argv[3:])

