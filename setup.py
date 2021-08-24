#!/usr/bin/env python3

import setuptools

from algovanity import __metadata__


setuptools.setup(
    name = __metadata__.__pkgname__,
    description = __metadata__.__description__,
    version = __metadata__.__version__,
    author = __metadata__.__author__,
    author_email = __metadata__.__author_email__,
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: Linux',
    ],
    packages = setuptools.find_namespace_packages(include=[__metadata__.__pkgname__, f'{__metadata__.__pkgname__}.*']),
    entry_points = {
        'console_scripts': [
            'algovanity = algovanity.cli:main',
        ]
    },
    install_requires = [
        'py-algorand-sdk>=1.7.0',
    ],
)
