#!/usr/bin/env python

from distutils.core import setup

setup(name='Wobsiter',
      version='0.0.1',
      description='Creates complete wobsites from ReST sources.',
      author='Benedikt Sauer',
      author_email='bcsauer@uni-bonn.de',
      url='http://www.uni-bonn.de/~bcsauer',
      packages=['wobsiter', 'wobsiter.source', 'wobsiter.output'],
      scripts=['wobsiter.py'],
      license='GPL-3',
      long_description='',
      )

