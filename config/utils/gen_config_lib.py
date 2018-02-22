##############################################################################
# Copyright (c) 2018 OPNFV and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
"""Library for generate_config functions and custom jinja2 filters"""

import logging
from ipaddress import IPv4Network, IPv4Address


def load_custom_filters(environment):
    """Load all defined filters into the jinja2 enviroment"""

    # TODO deprecate ipaddr_index and netmask for the better ipnet ones
    filter_list = {
        'dpkg_arch': filter_dpkg_arch,
        'storage_size_num': filter_storage_size_num,
        'ipnet_hostaddr': filter_ipnet_hostaddr,
        'ipnet_hostmin': filter_ipnet_hostmin,
        'ipnet_hostmax': filter_ipnet_hostmax,
        'ipnet_broadcast': filter_ipnet_broadcast,
        'ipnet_netmask': filter_ipnet_netmask,
        'ipnet_contains_ip': filter_ipnet_contains_ip,
        'ipnet_contains_iprange': filter_ipnet_contains_iprange,
        'ipnet_range_size': filter_ipnet_range_size,
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
    arch_dpkg_table = dict(
        zip(dpkg_arch_table.values(), dpkg_arch_table.keys()))

    if to_dpkg:
        return dpkg_arch_table[arch]
    else:
        return arch_dpkg_table[arch]


def filter_storage_size_num(size_str):
    """Convert human-readable size string to a string convertible to float"""

    # pattern: '^[1-9][\d\.]*[MGT]B?$', multiplier=1000 (not KiB)
    if size_str.endswith('B'):
        size_str = size_str[:-1]
    try:
        size_num = 1000000
        for multiplier in ['M', 'G', 'T']:
            if size_str.endswith(multiplier):
                return '{:.2f}'.format(size_num * float(size_str[:-1]))
            size_num = size_num * 1000
        return '{:.2f}'.format(float(size_str))
    except ValueError as ex:
        logging.error(size_str + " is not a valid size string")
        raise


def filter_ipnet_hostaddr(network_cidr, index):
    """Return the host IP address on given index from an IP network"""
    try:
        network_cidr_str = unicode(network_cidr)
    except NameError as ex:
        network_cidr_str = str(network_cidr)
    try:
        return IPv4Network(network_cidr_str)[index]
    except ValueError as ex:
        logging.error(network_cidr_str + " is not a valid network address")
        raise
    except IndexError as ex:
        logging.error(network_cidr_str + " has not enough range for "
                      + str(index) + " host IPs.")
        raise


def filter_ipnet_broadcast(network_cidr):
    """Return broadcast IP address from given IP network"""
    try:
        network_cidr_str = unicode(network_cidr)
    except NameError as ex:
        network_cidr_str = str(network_cidr)
    try:
        return IPv4Network(network_cidr_str).broadcast_address
    except ValueError as ex:
        logging.error(network_cidr_str + " is not a valid network address")
        raise


def filter_ipnet_hostmin(network_cidr):
    """Return the first host IP address from given IP network"""
    try:
        network_cidr_str = unicode(network_cidr)
    except NameError as ex:
        network_cidr_str = str(network_cidr)
    try:
        return IPv4Network(network_cidr_str)[1]
    except ValueError as ex:
        logging.error(network_cidr_str + " is not a valid network address")
        raise


def filter_ipnet_hostmax(network_cidr):
    """Return the last host IP address from given IP network"""
    try:
        network_cidr_str = unicode(network_cidr)
    except NameError as ex:
        network_cidr_str = str(network_cidr)
    try:
        return IPv4Network(network_cidr_str)[-2]
    except ValueError as ex:
        logging.error(network_cidr_str + " is not a valid network address")
        raise


def filter_ipnet_netmask(network_cidr):
    """Return the IP netmask from given IP network"""
    try:
        network_cidr_str = unicode(network_cidr)
    except NameError as ex:
        network_cidr_str = str(network_cidr)
    try:
        return IPv4Network(network_cidr_str).netmask
    except ValueError as ex:
        logging.error(network_cidr_str + " is not a valid network address")
        raise


def filter_ipnet_contains_ip(network_cidr, ip_address):
    """Check if an IP network cointains a given range"""
    try:
        network_cidr_str = unicode(network_cidr)
        ip_address_str = unicode(ip_address)
    except NameError as ex:
        network_cidr_str = str(network_cidr)
        ip_address_str = str(ip_address)
    try:
        return IPv4Address(ip_address_str) in IPv4Network(network_cidr_str)
    except ValueError as ex:
        logging.error(network_cidr_str + " is not a valid network address")
        raise


def filter_ipnet_contains_iprange(network_cidr, range_start, range_end):
    """Check if an IP network cointains a given range"""
    try:
        network_cidr_str = unicode(network_cidr)
        range_start_str = unicode(range_start)
        range_end_str = unicode(range_end)
    except NameError as ex:
        network_cidr_str = str(network_cidr)
        range_start_str = str(range_start)
        range_end_str = str(range_end)
    try:
        ipnet = IPv4Network(network_cidr_str)
        return (IPv4Address(range_start_str) in ipnet
                and IPv4Address(range_end_str) in ipnet)
    except ValueError as ex:
        logging.error(network_cidr_str + " is not a valid network address")
        raise


def filter_ipnet_range_size(network_cidr, range_start, range_end):
    """Get the size of an IP range between two IP addresses"""
    try:
        network_cidr_str = unicode(network_cidr)
        range_start_str = unicode(range_start)
        range_end_str = unicode(range_end)
    except NameError as ex:
        network_cidr_str = str(network_cidr)
        range_start_str = str(range_start)
        range_end_str = str(range_end)
    try:
        ipnet = IPv4Network(network_cidr_str)
        ip1 = IPv4Address(range_start_str)
        ip2 = IPv4Address(range_end_str)

        if ip1 in ipnet and ip2 in ipnet:
            index1 = list(ipnet.hosts()).index(ip1)
            index2 = list(ipnet.hosts()).index(ip2)
            ip_range_size = index2 - index1 + 1
            return ip_range_size
        else:
            raise ValueError
    except ValueError as ex:
        logging.error(range_start_str + " and " + range_end_str +
                      " are not valid IP addresses for range inside " +
                      network_cidr_str)
        raise


# This filter is too simple and does not take network mask into account.
# TODO Deprecate for filter_ipnet_hostaddr
def filter_ipaddr_index(base_address, index):
    """Return IP address in given network at given index"""
    try:
        base_address_str = unicode(base_address)
    except NameError as ex:
        base_address_str = str(base_address)
    return IPv4Address(base_address_str) + int(index)


# TODO deprecate for filter_ipnet_netmask
def filter_netmask(prefix):
    """Get netmask from prefix length integer"""
    try:
        prefix_str = unicode(prefix)
    except NameError as ex:
        prefix_str = str(prefix)
    return IPv4Network("1.0.0.0/"+prefix_str).netmask
