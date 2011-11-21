#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='chegg_api',
    version='dev',
    description="""Python bindings for Chegg APIs""",
    # long_description=open('README.rst').read(),
    author='Marc Abramowitz',
    author_email='mabramowitz@chegg.com',
    # url='https://github.com/kennethreitz/omnijson',
    packages=[
        'chegg_api',
    ],
    license='MIT',
)
