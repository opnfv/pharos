#! /usr/bin/env python3

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
    license = 'TBD',

    packages = ['pharosvalidator',
                'pharosvalidator.test'],

    package_dir =  {'pharosvalidator':'src',
                    'pharosvalidator.test':'src/test'},

    # Change these per distribution
    data_files = [('share/man/man1/', ['doc/pharos-validator.1']),
                  ('share/licenses/pharos-validator/LICENSE', ['LICENSE']),
                  ('share/pharos-validator/', ['doc/config.yaml', 'doc/inventory.yaml', 'doc/network.yaml']),
                 ],

    scripts = ['bin/pharos-validator-node',
               'bin/pharos-validator-server']
    )
