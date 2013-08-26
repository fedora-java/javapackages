#!/usr/bin/env python
"""
Setup script
"""
from setuptools import setup

setup(
    name = 'javapackages',
    description = 'Module for handling, querying and manipulating of various '
                  'files for Java packaging in Linux distributions',
    version = '1.0.0',
    license = 'BSD',
    download_url = 'https://fedorahosted.org/released/javapackages/',
    url = 'https://fedorahosted.org/javapackages/',
    packages = ['javapackages'],
    test_suite = "test",
    maintainer  = 'javapackages maintainers',
    maintainer_email = 'java-devel@lists.fedoraproject.org'
)
