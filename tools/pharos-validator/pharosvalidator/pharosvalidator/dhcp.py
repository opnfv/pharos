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

from pharosvalidator import pharos
from pharosvalidator import util

def gen_dhcpd_file(dhcpdfile, nodes, network):
    """Generates and associates incremental ip addresses to
    MAC addresses according to restrictions placed by network
    configuration file. Writes all of this out in dhcpd.conf format"""
    logger = logging.getLogger(__name__)
    logger.info("Generating dhcpfile...")
    dhcpdtxt = """default-lease-time 86400;
max-lease-time 604800;
max-lease-time 604800;

allow booting;
allow bootp;
authoritative;

subnet {subnet} netmask {netmask} {{
    range {ip_start} {ip_end};
    option broadcast-address {broadcastaddr};
    filename "pxelinux.0";
    next-server {next_server};
{static_ips}
}}
"""

    # Not explicitly in the cofiguration file
    broadcastaddr = "0.0.0.0"
    next_server = "0.0.0.0"

    ip_bounds = network.ip_bounds()
    ip_range = util.gen_ip_range(addr_and_cidr = network.cidr, \
                                 excluded = util.get_addrs(), \
                                 minimum = ip_bounds.start, \
                                 maximum = ip_bounds.end)

    # For now no static addresses are assigned
    static_addrtxt = ""
    static_addrs = []
    for node in nodes:
        if node.ipmi_addr in ip_range:
            ip_range.remove(node.ipmi_addr)

        i = 0;
        # Since all the interfaces are on the same hardware, its safe to assign them all the same ip
        for iface in node.interfaces:
            static_ip_line = "host {node}  {{ hardware ethernet {iface}; fixed-address {ip_addr}; }}\n".format( \
                node = node.name.replace(' ', '_') + str(i), \
                iface = iface, \
                ip_addr=ip_range[0])
            logger.info(static_ip_line)
            static_addrtxt += "    " + static_ip_line
            i += 1;
        static_addrs.append(ip_range[0])
        ip_range = ip_range[1::] # Remove the just assigned ip address from the range

    # Now format it all
    dhcpdtxt = dhcpdtxt.format(subnet=network.subnet, \
                    netmask=network.netmask, \
                    ip_start=ip_bounds.start, \
                    ip_end=ip_bounds.end, \
                    broadcastaddr=broadcastaddr, \
                    next_server=next_server, \
                    static_ips=static_addrtxt)

    with open(dhcpdfile, "w+") as fd:
        logger.info("Writing out dhcpd file to {}".format(dhcpdfile))
        fd.write(dhcpdtxt)

    return static_addrs

def start_dhcp_service(init_cmd):
    logger = logging.getLogger(__name__)
    with open(os.devnull, 'w') as fn:
        status = subprocess.Popen(init_cmd, stdout=fn, stderr=fn).wait()
    if int(status) != 0:
        logger.error("Could not bring up dhcpd server")
    else:
        logger.info("dhcpd server brought up")
    return status

if __name__ == "__main__":
    split("inventory.yaml", "eth0")
