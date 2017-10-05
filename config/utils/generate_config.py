#!/usr/bin/python
##############################################################################
# Copyright (c) 2017 OPNFV and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
"""This module does blah blah."""
import os
import re
import argparse
from pathlib import Path
import ipaddress
import yaml
from jinja2 import Environment, FileSystemLoader

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--yaml", "-y", type=str, required=True)
PARSER.add_argument("--jinja2", "-j", type=str, required=True)
ARGS = PARSER.parse_args()

# Processor architecture vs DPKG architecture mapping
DPKG_ARCH_TABLE = {
    'aarch64': 'arm64',
    'x86_64': 'amd64',
}
ARCH_DPKG_TABLE = dict(zip(DPKG_ARCH_TABLE.values(), DPKG_ARCH_TABLE.keys()))

# Custom filter to allow simple IP address operations returning
# a new address from an upper or lower (negative) index
def ipaddr_index(base_address, index):
    """Return IP address in given network at given index"""
    try:
        base_address_str = unicode(base_address)
    #pylint: disable=unused-variable
    except NameError as ex:
        base_address_str = str(base_address)
    return ipaddress.ip_address(base_address_str) + int(index)

# Custom filter to convert between processor architecture
# (as reported by $(uname -m)) and DPKG-style architecture
def dpkg_arch(arch, to_dpkg=True):
    """Return DPKG-compatible from processor arch and vice-versa"""
    if to_dpkg:
        return DPKG_ARCH_TABLE[arch]
    else:
        return ARCH_DPKG_TABLE[arch]

ENV = Environment(loader=FileSystemLoader('./'))
ENV.filters['ipaddr_index'] = ipaddr_index
ENV.filters['dpkg_arch'] = dpkg_arch

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


#If key exists, look for encrypted values and swap them out
my_file = Path("/etc/eyaml_keys/private_key.pkcs7.pem")
if my_file.is_file():
    regex_txt = r"ENC*"
    User = DICT["jumphost"]["remote_params"]["user"]
    Password = DICT["jumphost"]["remote_params"]["pass"]
    if re.match(regex_txt, User) is not None:
        User = os.popen('eyaml decrypt -s %s' % User).read()
        DICT["jumphost"]["remote_params"]["user"] = User.rstrip()
    if re.match(regex_txt, Password) is not None:
        Password = os.popen('eyaml decrypt -s %s' % Password).read()
        DICT["jumphost"]["remote_params"]["pass"] = Password.rstrip()
# Render template and print generated conf to console
TEMPLATE = ENV.get_template(ARGS.jinja2)
#pylint: disable=superfluous-parens
print(TEMPLATE.render(conf=DICT))
