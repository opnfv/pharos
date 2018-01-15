#!/usr/bin/python
##############################################################################
# Copyright (c) 2018 Enea AB and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
"""This module validates a PDF file against the schema."""
import argparse
import jsonschema
import yaml

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--yaml", "-y", type=str, required=True)
PARSER.add_argument("--schema", "-s", type=str, required=True)
ARGS = PARSER.parse_args()

with open(ARGS.yaml) as _:
    _DICT = yaml.safe_load(_)

with open(ARGS.schema) as _:
    _SCHEMA = yaml.safe_load(_)

_VALIDATOR = jsonschema.Draft4Validator(_SCHEMA)
for error in _VALIDATOR.iter_errors(_DICT):
    raise RuntimeError(str(error))
