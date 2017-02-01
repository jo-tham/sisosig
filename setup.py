#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'requests>=2.13.0',
    'pymongo>=3.4.0',
    'request.futures>=0.9.7',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='sisosig',
    version='0.1.0',
    description="Decide on trips using weather forecasts",
    long_description=readme + '\n\n' + history,
    author="Jotham Apaloo",
    author_email='jothamapaloo@gmail.com',
    url='https://github.com/jo-tham/sisosig',
    packages=[
        'sisosig',
    ],
    package_dir={'sisosig':
                 'sisosig'},
    entry_points={
        'console_scripts': [
            'sisosig=sisosig.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='sisosig',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
