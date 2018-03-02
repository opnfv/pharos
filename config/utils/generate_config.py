#!/usr/bin/python
##############################################################################
# Copyright (c) 2018 OPNFV and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
"""Generate configuration from PDF/IDF and jinja2 installer template"""

import argparse
import logging
from os.path import abspath, basename, dirname, exists, isfile, split
from subprocess import CalledProcessError, check_output
import gen_config_lib
import yaml
from jinja2 import Environment, FileSystemLoader


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--yaml", "-y", type=str, required=True)
PARSER.add_argument("--jinja2", "-j", type=str, required=True, action='append')
PARSER.add_argument("--includesdir", "-i", action='append', default=[])
PARSER.add_argument("--batch", "-b", action='store_true')
ARGS = PARSER.parse_args()

ARGS.jinja2 = [abspath(x) for x in ARGS.jinja2]
ARGS.includesdir.extend([dirname(x) for x in ARGS.jinja2])

LOADER = yaml.CSafeLoader if yaml.__with_libyaml__ else yaml.SafeLoader

ENV = Environment(
    loader=FileSystemLoader(ARGS.includesdir),
    extensions=['jinja2.ext.do']
)
gen_config_lib.load_custom_filters(ENV)

# Run `eyaml decrypt` on the whole file, but only if PDF data is encrypted
# Note: eyaml return code is 0 even if keys are not available
try:
    if isfile(ARGS.yaml) and 'ENC[PKCS7' in open(ARGS.yaml).read():
        DICT = yaml.load(check_output(['eyaml', 'decrypt',
                                       '-f', ARGS.yaml]), Loader=LOADER)
except CalledProcessError as ex:
    logging.error('eyaml decryption failed! Fallback to raw data.')
except OSError as ex:
    logging.warn('eyaml not found, skipping decryption. Fallback to raw data.')
try:
    DICT['details']
except (NameError, TypeError) as ex:
    with open(ARGS.yaml) as _:
        DICT = yaml.load(_, Loader=LOADER)

# If an installer descriptor file (IDF) exists, include it (temporary)
IDF_PATH = '/idf-'.join(split(ARGS.yaml))
if exists(IDF_PATH):
    with open(IDF_PATH) as _:
        IDF = yaml.load(_, Loader=LOADER)
        DICT['idf'] = IDF['idf']

# Print dictionary generated from yaml (uncomment for debug)
# print(DICT)

for _j2 in ARGS.jinja2:
    TEMPLATE = ENV.get_template(basename(_j2))
    OUTPUT = TEMPLATE.render(conf=DICT)
    # Render template and write generated conf to file or stdout
    if ARGS.batch:
        if _j2.endswith('.j2'):
            with open(_j2[:-3], 'w') as _:
                _.write(OUTPUT)
        else:
            logging.warn('Skipping {}, name does not end in ".j2"'.format(_j2))
    else:
        # pylint: disable=superfluous-parens
        print(OUTPUT)
