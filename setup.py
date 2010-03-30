#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='cyrax',
      description='Static site generator',
      long_description = read('README'),
      license = 'BSD',
      version = '0.1.9',
      author = 'Alexander Solovyov',
      author_email = 'piranha@piranha.org.ua',
      url = 'http://hg.piranha.org.ua/cyrax/',
      packages = ['cyraxlib'],
      scripts = ['cyrax'],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Editors :: Documentation',
        'Topic :: Utilities',
        ],
      platforms='any',
      )
