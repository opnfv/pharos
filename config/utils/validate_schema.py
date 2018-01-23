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

# Draft 4 (latest supported by py-jsonschema) does not support value-based
# decisions properly, see related github issue:
# https://github.com/json-schema-org/json-schema-spec/issues/64
# Workaround: build 'version_x.y: true' on the fly based on 'version: x.y'
def schema_version_workaround(node):
    """Traverse nested dictionaries and handle 'version' key where found."""
    if 'version' in node:
        node['version_{0}'.format(node['version'])] = True
    for item in node.items():
        if type(item) is dict:
            schema_version_workaround(item)
schema_version_workaround(_DICT)

_VALIDATOR = jsonschema.Draft4Validator(_SCHEMA)
for error in _VALIDATOR.iter_errors(_DICT):
    raise RuntimeError(str(error))
