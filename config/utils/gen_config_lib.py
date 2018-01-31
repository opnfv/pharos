#!/usr/bin/python
##############################################################################
# Copyright (c) 2018 OPNFV and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
"""Library for generate_config functions, including all custom jinja2 filters"""

import logging
import ipaddress

def load_custom_filters(environment):
    """Load all defined filters into the jinja2 enviroment"""

    #TODO deprecate ipaddr_index and netmask for the better ipnet ones
    filter_list = {
        'dpkg_arch': filter_dpkg_arch,
        'ipnet_hostaddr': filter_ipnet_hostaddr,
        'ipnet_hostmin': filter_ipnet_hostmin,
        'ipnet_hostmax': filter_ipnet_hostmax,
        'ipnet_broadcast': filter_ipnet_broadcast,
        'ipnet_netmask': filter_ipnet_netmask,
        'ipaddr_index': filter_ipaddr_index,
        'netmask': filter_netmask
    }

    for name, function in filter_list.items():
        environment.filters[name] = function

def filter_dpkg_arch(arch, to_dpkg=True):
    """Convert DPKG-compatible from processor arch and vice-versa"""

    # Processor architecture (as reported by $(uname -m))
    # vs DPKG architecture mapping
    dpkg_arch_table = {
        'aarch64': 'arm64',
        'x86_64': 'amd64',
    }
    arch_dpkg_table = dict(zip(dpkg_arch_table.values(), dpkg_arch_table.keys()))

    if to_dpkg:
        return dpkg_arch_table[arch]
    else:
        return arch_dpkg_table[arch]

def filter_ipnet_hostaddr(network_address, prefixlen, index):
    """Return the host IP address on given index from an IP network"""
    try:
        network_address_str = unicode(network_address)
        prefixlen_str = unicode(prefixlen)
    except NameError as ex:
        network_address_str = str(network_address)
        prefixlen_str = str(prefixlen)

    try:
        ipnet = ipaddress.IPv4Network(network_address_str + "/" + prefixlen_str)
        return list(ipnet.hosts())[index -1]
    except ValueError as ex:
        logging.error(network_address_str + "/" + prefixlen_str +
                      " is not a valid network address")
        raise
    except IndexError as ex:
        logging.error(ipnet.with_prefixlen + " has not enough range for "
                      + str(index) + " host IPs. Out of range after "
                      + str(ipnet.num_addresses))
        raise

def filter_ipnet_broadcast(network_address, prefixlen):
    """Return broadcast IP address from given IP network"""
    try:
        network_address_str = unicode(network_address)
        prefixlen_str = unicode(prefixlen)
    except NameError as ex:
        network_address_str = str(network_address)
        prefixlen_str = str(prefixlen)
    try:
        ipnet = ipaddress.IPv4Network(network_address_str + "/" + prefixlen_str)
        return ipnet.broadcast_address
    except ValueError as ex:
        logging.error(network_address_str + "/" + prefixlen_str +
                      " is not a valid network address")
        raise

def filter_ipnet_hostmin(network_address, prefixlen):
    """Return the first host IP address from given IP network"""
    try:
        network_address_str = unicode(network_address)
        prefixlen_str = unicode(prefixlen)
    except NameError as ex:
        network_address_str = str(network_address)
        prefixlen_str = str(prefixlen)
    try:
        ipnet = ipaddress.IPv4Network(network_address_str + "/" + prefixlen_str)
        return list(ipnet.hosts())[0]
    except ValueError as ex:
        logging.error(network_address_str + "/" + prefixlen_str +
                      " is not a valid network address")
        raise

def filter_ipnet_hostmax(network_address, prefixlen):
    """Return the last host IP address from given IP network"""
    try:
        network_address_str = unicode(network_address)
        prefixlen_str = unicode(prefixlen)
    except NameError as ex:
        network_address_str = str(network_address)
        prefixlen_str = str(prefixlen)
    try:
        ipnet = ipaddress.IPv4Network(network_address_str + "/" + prefixlen_str)
        return list(ipnet.hosts())[-1]
    except ValueError as ex:
        logging.error(network_address_str + "/" + prefixlen_str +
                      " is not a valid network address")
        raise

def filter_ipnet_netmask(network_address, prefixlen):
    """Return the IP netmask from given IP network"""
    try:
        network_address_str = unicode(network_address)
        prefixlen_str = unicode(prefixlen)
    except NameError as ex:
        network_address_str = str(network_address)
        prefixlen_str = str(prefixlen)
    try:
        ipnet = ipaddress.IPv4Network(network_address_str + "/" + prefixlen_str)
        return ipnet.netmask
    except ValueError as ex:
        logging.error(network_address_str + "/" + prefixlen_str +
                      " is not a valid network address")
        raise

# This filter is too simple and does not take network mask into account.
# TODO Deprecate for filter_ipnet_hostaddr
def filter_ipaddr_index(base_address, index):
    """Return IP address in given network at given index"""
    try:
        base_address_str = unicode(base_address)
    #pylint: disable=unused-variable
    except NameError as ex:
        base_address_str = str(base_address)
    return ipaddress.ip_address(base_address_str) + int(index)

#TODO deprecate for filter_ipnet_netmask
def filter_netmask(prefix):
    """Get netmask from prefix length integer"""
    try:
        prefix_str = unicode(prefix)
    except NameError as ex:
        prefix_str = str(prefix)
    return ipaddress.IPv4Network("1.0.0.0/"+prefix_str).netmask
