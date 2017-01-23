#!/usr/bin/env python3

from distutils.core import setup

import subprocess

setup(
    name = 'pharos-validator',
    description = 'Testing tool for Pharos spec compliance',
    author = 'Todd Gaunt',
    url = '',
    download_url = '',
    author_email = 'singularik@iol.unh.edu',
    version = '0.1',
    license = 'Apache 2.0',

    packages = ['pharosvalidator'],

    package_dir =  {'pharosvalidator':'pharosvalidator'},

    # Change these per distribution
    data_files = [('share/man/man1/', ['doc/pharosvalidator.1']),
                  ('share/licenses/pharosvalidator/LICENSE', ['LICENSE']),
                  ('share/pharosvalidator/', ['doc/config.yaml', 'doc/inventory.yaml', 'doc/network.yaml']),
                 ],

    scripts = ['bin/pharosvalidator']
    )
