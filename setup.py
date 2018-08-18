#!/usr/bin/env python
from setuptools import setup, find_packages
from glob import glob
setup(
    name='coffeemachine',
    version='1.0',
    scripts=glob('scripts/*') + [ 'manage.py' ],
    packages=find_packages(),
    setup_requires=['django', 'pyscard', 'pandas'],
    tests_require=['pytest', 'pytest-django'])
