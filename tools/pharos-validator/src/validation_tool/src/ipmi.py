##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import subprocess
import logging

def power_nodes(nodes, action):
    """ Attempts to power on all nodes specified in a list, then returns a list
    of the names of all failures. The list will be empty if no failures."""
    failed_nodes = []
    logger = logging.getLogger(__name__)
    if not nodes:
        logger.info("No nodes, is empty list")
    for node in nodes:
        # -I flag must be 'lanplus', 'lan' by itself doesn't work with
        # the most recent idrac/ipmi version
        if action == "on":
            pass
        elif action == "off":
            pass
        else:
            logger.error("Invalid ipmi command")

        cmd = ["ipmitool", \
                  "-I", "lanplus", \
                  "-H ", "'"+node.ipmi_addr+"'", \
                  "-U ", "'"+node.ipmi_user+"'", \
                  "-P ", "'"+node.ipmi_pass+"'", \
                  "power", action]

        logger.debug("Running: \"{}\"".format(' '.join(cmd)))
        try:
            with open(os.devnull, 'w') as fn:
                status = subprocess.check_call(" ".join(cmd), \
                        stdout=fn, stderr=fn, shell=True)
        except subprocess.CalledProcessError as e:
            status = e.returncode
            logger.error("{} could not be accessed at {} (exit code {})".format(\
                    node.name, node.ipmi_addr, status))
            failed_nodes.append(node.name)
        if int(status) == 0:
            logger.info("{} successfully powered {}".format(node.name, action))

    return failed_nodes

def status(node, ipaddr, username, passwd):
    # -I flag must be 'lanplus', 'lan' by itself doesn't work with
    # the most recent idrac/ipmi version
    chkcmd = ["ipmitool", \
              "-I", "lanplus", \
              "-H", ipaddr, \
              "-U", username, \
              "-P", passwd, \
              "chassis", "status"]
    print(chkcmd)
    subprocess.Popen(chkcmd)
