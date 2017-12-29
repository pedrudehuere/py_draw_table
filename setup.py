# -*- coding: utf8 -*-

import os.path
from setuptools import setup


# getting version
version = {}
here = os.path.dirname(__file__)
with open(os.path.join(here, 'draw_table', '__version__.py')) as f:
    exec(f.read(), version)
version = version['version']


setup(
    name='draw_table',
    version=version,
    packages=['draw_table'],
    url='https://github.com/pedrudehuere/py_draw_table',
    license='MIT',
    author='Andrea Peter',
    author_email='pedrudehuere@hotmail.com',
    description='Simple string based table for Python 3',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ),
)
