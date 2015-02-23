#-
# Copyright (c) 2015, Red Hat, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of Red Hat nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:  Michael Simacek <msimacek@redhat.com>

import six

from lxml import etree
from copy import deepcopy

from javapackages.common.exception import JavaPackagesToolsException

class XMLBindingException(JavaPackagesToolsException):
    pass


def _get_item_type(spec):
    assert 0 < len(spec) <= 2, spec
    spec = tuple(spec)
    ret = spec[0]
    if len(spec) == 1:
        if isinstance(spec[0], six.string_types):
            ret = str
    elif isinstance(spec[0], six.string_types):
        ret = spec[1]
    assert isinstance(ret, type), ret
    return ret


def _get_item_name(spec):
    assert 0 < len(spec) <= 2, spec
    spec = tuple(spec)
    ret = spec[0]
    if isinstance(spec[0], type) and issubclass(spec[0], ObjectBinding):
        ret = spec[0].element_name
    elif len(spec) == 2 and isinstance(spec[0], type):
        ret = spec[1]
    assert isinstance(ret, six.string_types), ret
    return ret


def _is_element(node):
    return isinstance(node.tag, six.string_types)

def _localname(element):
    return etree.QName(element.tag).localname

def from_element(for_type, element):
    if for_type is str:
        return element.text.strip() if element.text is not None else None
    if isinstance(for_type, list):
        item_type = _get_item_type(for_type)
        return [from_element(item_type, child) for child in element
                if _is_element(child)]
    if isinstance(for_type, set):
        item_type = _get_item_type(for_type)
        return set([from_element(item_type, child) for child in element
                    if _is_element(child)])
    if for_type is dict:
        new = {}
        for child in element:
            if isinstance(child.tag, six.string_types):
                name = _localname(child)
                value = from_element(str, child)
                new[name] = value
        return new
    if isinstance(for_type, type) and issubclass(for_type, ObjectBinding):
        name = _localname(element)
        if name != for_type.element_name:
            raise XMLBindingException("Unexpected element " + name)
        new = {}
        for child in element:
            if _is_element(child):
                name = _localname(child)
                if name in for_type.fields:
                    value = from_element(for_type.types.get(name, str), child)
                    if name in new:
                        raise XMLBindingException("More values for element " + name)
                    new[name] = value
        return for_type(**new)
    raise XMLBindingException("Unrecognized binding type: {0}".format(for_type))


def _make_element(name, ns=None):
    if ns:
        name = '{' + ns + '}' + name
    return etree.Element(name)

def to_element(obj, name=None, type_spec=None, ns=None):
    if isinstance(obj, six.string_types):
        element = _make_element(name, ns=ns)
        element.text = obj
        return element
    if isinstance(obj, list) or isinstance(obj, set):
        element = _make_element(name, ns=ns)
        for item in obj:
            element.append(to_element(item, name=_get_item_name(type_spec),
                                      ns=ns))
        return element
    if isinstance(obj, dict):
        element = _make_element(name, ns=ns)
        for key, value in obj.items():
            # TODO rly?
            # entry = _make_element(key, ns=ns)
            entry = _make_element(key)
            entry.text = value
            element.append(entry)
        return element
    if isinstance(obj, ObjectBinding):
        name = obj.element_name
        ns = obj.xmlns or ns
        element = _make_element(name, ns=ns)
        for item_name in obj.fields:
            value = obj.values.get(item_name)
            if value:
                child = to_element(value, item_name,
                                   obj.types.get(item_name, str), ns=ns)
                element.append(child)
        return element

class ObjectBinding(object):
    element_name = None
    fields = []
    types = {}
    equality = None
    defaults = {}
    xmlns = None

    def __init__(self, *args, **kwargs):
        assert self.element_name
        assert self.fields
        self.values = self.defaults.copy()
        self._touched = set()
        for name in self.fields:
            item_type = self.types.get(name, str)
            if name not in self.values:
                if type(item_type) in (list, set):
                    self.values[name] = type(item_type)()
                elif item_type == dict:
                    self.values[name] = {}
                elif item_type == str:
                    self.values[name] = ''
        values = zip(self.fields, args) + kwargs.items()
        for name, value in values:
            setattr(self, name, value)

    def __getattr__(self, name):
        if name in self.fields:
            return self.values.get(name)
        return getattr(super(ObjectBinding, self), name)

    def __setattr__(self, name, value):
        if name in self.fields:
            self.values[name] = value
            self._touched.add(name)
        else:
            super(ObjectBinding, self).__setattr__(name, value)

    def __contains__(self, name):
        return name in self._touched

    def __repr__(self):
        return repr(self.values)

    def _get_values_for_equality(self):
        if self.equality is not None:
            return [v for k, v in self.values.items() if k in self.equality]
        return [v for k, v in self.values.items()]

    def __eq__(self, that):
        return self is that or (type(self) is type(that) and
                                self._get_values_for_equality()
                                == that._get_values_for_equality())

    def __ne__(self, that):
        return not self.__eq__(that)

    def __hash__(self):
        if self.equality:
            return hash(self._get_values_for_equality)
        return id(self)

    def copy(self):
        return deepcopy(self)
