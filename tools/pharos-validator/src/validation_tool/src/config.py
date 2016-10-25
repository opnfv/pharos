##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
import sys
import os
import yaml
import struct
import socket

from pharosvalidator import util
from collections import namedtuple

class Topology():
    """
    Topology: Class to store any number of Network classes
    and metadata about them
    """
    def __init__(self, yaml_config):
        # Dictionary of available networks
        self.logger = logging.getLogger(__name__)
        self.networks = {}
        self.external_networks = []

        # Fill the above dictionaries
        self.parse_yaml(yaml_config)

    def parse_yaml(self, yaml_config):
        """
        parse_yaml: parses the yaml configuration file this program uses
        for all the network and node information
        """
        config = safe_yaml_read(yaml_config)
        for network in config["networks"]:
            self.logger.info("Reading network section {}".format(network))
            if network == "admin":
                self.networks[network] = Network(config["networks"][network])
            #TODO
            elif network == "external":
                for external_network in config["networks"][network]:
                    self.external_networks.append(Network(external_network))

class Network():
    """
    Network: Class to store all information on a given network
    """
    def __init__(self, network):
        try:
            self.logger = logging.getLogger(__name__)

            # Some generic settings
            self.enabled = network["enabled"]
            self.vlan = network["vlan"]

            # VM settings
            self.installer_nic_type = network["installer_vm"]["nic_type"]
            self.installer_members = network["installer_vm"]["members"]
            self.installer_ip = network["installer_vm"]["ip"]

            # Tuple containing the minimum and maximum
            self.usable_ip_range = self.parse_ip_range(network["usable_ip_range"])
            self.gateway = network["gateway"]
            self.cidr = network["cidr"]
            self.dhcp_range = network["dhcp_range"]
            self.dns_domain = network["dns-domain"]
            self.dns_search = network["dns-search"]

            subnet, netmask = self.split_cidr(network["cidr"])
            self.subnet = subnet
            self.netmask = netmask

            # List of all dns servers
            self.dns_upstream = network["dns-upstream"]

            self.nic_mapping = {}
        except KeyError as e:
            self.logger.error("Field {} not available in network configuration file".format(e))

    def split_cidr(self, cidr):
        """
        split_cidr: Split up cidr notation subnets into a subnet string and a
        netmask string

        input: cidr notation of a subnet

        output: Subnet string; Netmask string
        """
        split = cidr.split('/')
        host_bits = int(split[1])
        netmask = self.cidr_to_netmask(host_bits)
        subnet = split[0]

        return subnet, netmask

    def parse_ip_range(self, ip_range_string):
        """
        parse_ip_range: Create a named tuple object that contains the lowest
        ip address and the highest ip address from a configuration file

        input: String formatted like so "min, max" where min/max are ip addresses

        output: Named tuple object containing a minimum and maximum field
        """
        rp = ip_range_string.split(",")
        ip_range = namedtuple("ip_range", ['minimum', 'maximum'])(minimum=min(rp), maximum=max(rp))
        return ip_range

    def cidr_to_netmask(self, cidr):
        bits = 0xffffffff ^ (1 << 32 - cidr) - 1
        netmask = socket.inet_ntoa(struct.pack('>I', bits))
        self.logger.debug("Netmask generated from cidr '{}': '{}'".format(cidr, netmask))
        return netmask

class Inventory():
    """
    Inventory: Class to hold configuration file data
    """
    def __init__(self, yaml_config):
        # Create the class logger
        self.logger = logging.getLogger(__name__)

        self.nodes = []

        # Fill the above list
        self.parse_yaml(yaml_config)

    def parse_yaml(self, yaml_config):
        config = safe_yaml_read(yaml_config)
        nodes = []
        for node in config["nodes"]:
            self.nodes.append(Node(node))

    def nodecount(self):
        return len(self.nodes)

class Node():
    """
    Node: Class to hold
    """
    def __init__(self, node):
        self.logger = logging.getLogger(__name__)
        try:
            self.name = node["name"]
            self.tags = node["tags"]
            self.arch = node["arch"]
            self.mac_address = node["mac_address"] # ipmi mac address
            self.cpus = node["cpus"]
            self.memory = node["memory"]
            self.disk = node["disk"]
        except KeyError as e:
            self.logger.error("Field {} not available in inventory file".format(e))

        # Power sub section
        if node["power"]["type"] == "ipmi":
            try:
                self.ipmi_addr = node["power"]["address"]
                self.ipmi_user = node["power"]["user"]
                self.ipmi_pass = node["power"]["pass"]
            except KeyError as e:
                self.logger.error("Field {} not available in inventory file".format(e))
        else:
            pass

def safe_yaml_read(yamlfile):
    logger = logging.getLogger(__name__)
    if os.path.isfile(yamlfile) == False:
        logger.critical("Could not open find {}".format(yamlfile))
        quit(1)
    with open(yamlfile, 'r') as fd:
        return yaml.load(fd.read())
