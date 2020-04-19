#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import os
import re
import sys


VERSION_FILE = 'ajaxlte/__init__.py'
version_text = open(VERSION_FILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_text, re.M)
if mo:
    version = mo.group(1)
    print (version)
else:
    raise RuntimeError(
        "Unable to find version string in %s." % (VERSION_FILE,))

name = 'django-ajaxlte'
package = 'ajaxlte'
description = 'Genrerate adminlte cruds for models'
url = 'https://github.com/xangcastle/django_ajaxlte/'
author = 'Cesar Abel Ramirez'
author_email = 'xangcastle@gmail.com'
license = 'BSD'
install_requires = [
    'Django>=3.0.5',
    'django-crispy-forms>=1.9.0',
    'django-mathfilters>=1.0.0'
]

if sys.argv[-1] == 'publish':
    args = {'version': version}
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/django-ajaxlte-%(version)s*" % args)
    print("Creating git tag the version now:")
    os.system("git tag -a %(version)s -m 'version %(version)s'" % args)
    os.system("git push --tags")
    sys.exit()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), "r").read()


setup(
    name=name,
    version=version,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    packages=['ajaxlte'],
    include_package_data=True,
    description=description,
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
    install_requires=install_requires
)
