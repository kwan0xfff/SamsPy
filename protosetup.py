"""Samspy - Simple Aerospace Models in Python"

Source at:
    https://github.com/kwan0xfff/SamsPy.git

NOTE: This file contains the elements of a setup.py file, but isn't yet
ready for use with setuptools.
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='samspy',
    version='0.0.1',
    description='A sample Python project',
    long_description=long_description,
    url='https://github.com/kwan0xfff/SamsPy',
    author='Rick Kwan',
    author_email='kwan0xfff@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='aerospace propulsion rocket-engines',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['PyYAML'],

    #% From here, adding annotations with '#%' for things to be
    #% addressed in the near future.

    # additional groups of dependencies, e.g.,
    # $ pip install -e .[dev,test]
    #%extras_require={
    #%    'dev': ['check-manifest'],
    #%    'test': ['coverage'],
    #%},

    # Data files.
    #%package_data={
    #%    'sample': ['package_data.dat'],
    #%},

    # Alternative approach for data.  See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    #%data_files=[('my_data', ['data/data_file'])],

    # Executable scripts, entry points;
    #$entry_points={
    #$    'console_scripts': [
    #$        'sample=sample:main',
    #$    ],
    #$},
)
