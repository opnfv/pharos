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

from pharosvalidator import util
from collections import namedtuple

class ServerConfig:
    def __init__(self, port, dhcp_init, invconf_path, netconf_path):
        self.logger = logging.getLogger(__name__)

        self.port = port
        self.init_cmd = dhcp_init.split(" ")
        self.inventory = {}
        self.networks = {}

        netyaml = self.safe_yaml_read(netconf_path)
        for network in netyaml["networks"]:
            # The only network we're interested in
            if network == "admin":
                self.networks[network] = Network(netyaml["networks"][network])

        self.inventory["nodes"] = []
        invyaml = self.safe_yaml_read(invconf_path)
        for node in invyaml["nodes"]:
            self.inventory["nodes"].append(Node(node))
        self.inventory["jumphost"] = invyaml["jumphost"]
        self.inventory["details"] = invyaml["details"]

    def safe_yaml_read(self, yamlfile):
        logger = logging.getLogger(__name__)
        if os.path.isfile(yamlfile) == False:
            logger.critical("Could not open find {}".format(yamlfile))
            quit(1)
        with open(yamlfile, 'r') as fd:
            return yaml.load(fd.read())

    def nodecount(self):
        return len(self.inventory["nodes"])

class Node:
    def __init__(self, node):
        self.logger = logging.getLogger(__name__)
        try:
            self.name = node["name"]
            self.remote_management = node["remote_management"]
            self.ipmi_addr = util.split_cidr(self.remote_management["address"])[0]
            self.ipmi_user = self.remote_management["user"]
            self.ipmi_pass = self.remote_management["pass"]

            # This is the interface that will be assigned an address by the dhcp server
            self.interfaces = []
            for iface in node["interfaces"]:
                self.interfaces.append(iface["mac_address"])
        except KeyError as e:
            self.logger.info("unable to add {}".format(e))
            pass

class Network:
    def __init__(self, network):
        self.logger = logging.getLogger(__name__)
        try:
            self.cidr = network["cidr"]
            self.ip_range = network["usable_ip_range"]
            netpair = util.split_cidr(self.cidr)
            self.subnet = netpair[0]
            self.netmask = netpair[1]
            self.installer_ip = network["installer_vm"]["ip"]
            self.vlan = network["installer_vm"]["vlan"]
        except KeyError as e:
            self.logger.info("unable to add {}".format(e))
            pass

    def ip_bounds(self):
        rp = self.ip_range.split(",")
        return namedtuple("ip_bounds", ['start', 'end'])(start=min(rp), end=max(rp))
