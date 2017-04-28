# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 10:58:11 2017

@author: justi
"""

#!/usr/bin/env python

from setuptools import setup, find_packages

import sys
PYTHON_3 = sys.version_info[0] == 3
if PYTHON_3:
    nlp-tools = 'nlp-tools'
else:
    None

with open('README') as f:
    long_description = f.read()

setup(name='nlp-tools',
      version='0.5.0',
      description='NLP Tools - NLTK, Spacy, and Gensim integration',
      author='Justin Smith',
      author_email='justingriffis@gmail.com',
      keywords=('natural language', 'data mining' 'text-extraction'),
      license = "MIT License",
      exclude_package_data={'': ['.gitignore']},
      packages=find_packages('src'),
      package_dir={'': 'src'},
      requires=[nlp-tools],
      install_requires=['distribute', nlp-tools],
      classifiers= [
        'Development Status :: 3 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Utilities'],
      long_description=long_description,
      url='http://github.com/timClicks/slate')