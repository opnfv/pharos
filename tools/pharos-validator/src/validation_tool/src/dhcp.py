##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import yaml
import netifaces
import subprocess
import copy
import re
import os
import logging

from pharosvalidator.specification import *
from pharosvalidator import util

init_cmd = ["systemctl", "start", "dhcpd.service"]

def gen_dhcpd_file(dhcpdfile, nodes, network):
    """Generates and associates incremental ip addresses to
    MAC addresses according to restrictions placed by network
    configuration file. Writes all of this out in dhcpd.conf format"""
    logger = logging.getLogger(__name__)
    logger.info("Generating dhcpfile...")

    header = "default-lease-time 86400;\n\
            max-lease-time 604800;\n\
            max-lease-time 604800;\n\
            \n\
            allow booting;\n\
            authoritative;\n\
            \n"

    # Skip this network if it is disabled
    if network.enabled == False:
        logger.info("Admin network is disabled, please change the configuration to \"enabled\" if you would like this test to run")
        quit()

    # Not explicitly in the cofiguration file
    broadcastaddr = "0.0.0.0"
    next_server = "0.0.0.0"

    ip_range = util.gen_ip_range(network.cidr, [network.installer_ip], network.usable_ip_range.minimum, \
            network.usable_ip_range.maximum)

    tab = '    '
    subnetconf = "subnet {} netmask {} {{\n".format(network.subnet, network.netmask)\
            + tab+"range {} {};\n".format(network.usable_ip_range.minimum, network.usable_ip_range.maximum)\
            + tab+"option broadcast-address {};\n".format(broadcastaddr)\
            + tab+'filename "pxelinux.0";\n'\
            + tab+"next-server {};\n".format(next_server)

    # For now no static addresses are assigned
    """
    static_addrs = []
    for node in nodes:
        # Skip the node if it doesn't have a name or mac address specified
        if not node.name or not node.mac_address:
            continue

        if node.ipmi_addr in ip_range:
            ip_range.remove(node.ipmi_addr)

        static_line = "host {node}  {{ hardware ethernet {ipmi_mac}; fixed-address {ip_addr}; }}\n".format\
                (node=node.name, ipmi_mac=node.mac_address, ip_addr=ip_range[0])
        ip_range = ip_range[1::] # Remove the assigned ip address
        static_addrs.append(static_line)

    # Now add all statically assigned ip addresses
    for addr in static_addrs:
        subnetconf += tab+addr
    """

    subnetconf += "}\n" # Just the closing bracket

    # The final text to be written out to a file
    dhcpdtext = header + subnetconf

    with open(dhcpdfile, "w+") as fd:
        logger.info("Writing out dhcpd file to {}".format(dhcpdfile))
        fd.write(dhcpdtext)

    return dhcpdtext

def start_server():
    logger = logging.getLogger(__name__)
    global init_cmd
    cmd = init_cmd
    with open(os.devnull, 'w') as fn:
        status = subprocess.Popen(cmd, stdout=fn, stderr=fn).wait()
    if int(status) != 0:
        logger.error("Could not bring up dhcpd server")
    else:
        logger.info("Dhcp server brought up")
    return status

if __name__ == "__main__":
    split("inventory.yaml", "eth0")
