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
import os
from subprocess import CalledProcessError, check_output
import gen_config_lib
import yaml
from jinja2 import Environment, FileSystemLoader


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--yaml", "-y", type=str, required=True)
PARSER.add_argument("--jinja2", "-j", type=str, required=True)
ARGS = PARSER.parse_args()

ENV = Environment(loader=FileSystemLoader(os.path.dirname(ARGS.jinja2)))
gen_config_lib.load_custom_filters(ENV)

# Run `eyaml decrypt` on the whole file, but only if PDF data is encrypted
# Note: eyaml return code is 0 even if keys are not available
try:
    if os.path.isfile(ARGS.yaml) and 'ENC[PKCS7' in open(ARGS.yaml).read():
        DICT = yaml.safe_load(check_output(['eyaml', 'decrypt',
                                            '-f', ARGS.yaml]))
except CalledProcessError as ex:
    logging.error('eyaml decryption failed! Fallback to raw data.')
except OSError as ex:
    logging.warn('eyaml not found, skipping decryption. Fallback to raw data.')
try:
    DICT['details']
except (NameError, TypeError) as ex:
    with open(ARGS.yaml) as _:
        DICT = yaml.safe_load(_)

# If an installer descriptor file (IDF) exists, include it (temporary)
IDF_PATH = '/idf-'.join(os.path.split(ARGS.yaml))
if os.path.exists(IDF_PATH):
    with open(IDF_PATH) as _:
        IDF = yaml.safe_load(_)
        DICT['idf'] = IDF['idf']

# Print dictionary generated from yaml (uncomment for debug)
# print(DICT)

# Render template and print generated conf to console
TEMPLATE = ENV.get_template(os.path.basename(ARGS.jinja2))

# pylint: disable=superfluous-parens
print(TEMPLATE.render(conf=DICT))
