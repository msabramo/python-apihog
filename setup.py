#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='apihog',
    version='dev',
    description="""Consumes APIs like a pig""",
    # long_description=open('README.rst').read(),
    author='Marc Abramowitz',
    author_email='marc@marc-abramowitz.com',
    # url='https://github.com/kennethreitz/omnijson',
    packages=[
        'apihog',
    ],
    license='MIT',
)
