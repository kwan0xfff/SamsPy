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
    version='0.0.2.dev',
    description='Simple Aerospace ModelS in Python',
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

    # Example data files
    package_data={
        '': ['share/*.yaml'],
    },

    # Executable scripts, entry points
    entry_points={
        'console_scripts': [
            'lvbasic=samspy.cmds.lvbasic:main',
        ],
    },
)
