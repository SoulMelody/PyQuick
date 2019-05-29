#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    'cffi',
    'wrapt',
    'six',
    "enum34 ; python_version < '3.4'"
]

setup_requirements = []

test_requirements = ['pytest', 'tox', 'virtualenv']

setup(
    author="Soul Melody",
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Python :: Implementation :: PyPy',
    ],
    description="Cffi wrapper of DOtherSide for pypy",
    install_requires=requirements,
    license="GNU General Public License v3",
    include_package_data=True,
    keywords='PyQuick',
    name='PyQuick',
    packages=find_packages(include=['PyQuick']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SoulMelody/PyQuick',
    version='0.0.1',
    zip_safe=False,
)
