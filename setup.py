#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import cyrax

setup(name = 'cyrax',
      description = 'Static site generator',
      long_description = read('README.rst'),
      license = 'ISC',
      version = cyrax.__version__,
      author = 'Alexander Solovyov',
      author_email = 'alexander@solovyov.net',
      url = 'http://piranha.org.ua/cyrax/',
      install_requires = ['Jinja2', 'smartypants'],
      packages = ['cyrax', 'cyrax.template'],

      entry_points = {
          'console_scripts': ['cyrax = cyrax:main']
      },

      classifiers = [
          'Environment :: Console',
          'License :: OSI Approved :: ISC License (ISCL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Utilities',
      ],
      platforms='any',
)
