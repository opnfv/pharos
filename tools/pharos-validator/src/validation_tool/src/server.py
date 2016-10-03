##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
import os
import subprocess
import time

# Constant definitions
from pharosvalidator.const import *

def ssh_thread(remoteaddr, returnaddr, port, passes):
    """
    ssh_thread: the main loop of a thread the server spawns to connect to a node
    over ssh.

    input: remoteaddr, returnaddr, and port to forward to run_remote_test;
    passes to specify how many attempts should be made
    """
    for i in range(passes):
        status = run_remote_test(remoteaddr, returnaddr, port)
        time.sleep(1)

def run_remote_test(remoteaddr, returnaddr, port):
    """
    run_remote_tests: ssh to a give remote address, and run a test program
    on the remote machine specifying the address and port of where the results
    should be sent (usually back to the machine this program was run on)

    input: ip address of the ssh target; Adress of the test results target;
    Port of the test results target

    output: 0 if the test ran over ssh perfectly, non-zero if the test faild
    """
    #TODO add way to keep attempting to ssh until service is up and running aka ping part 2
    logger = logging.getLogger(__name__)

    cmd = ["ssh", "root@"+remoteaddr, HARDWARE_TEST, \
            "-p", port, "-H", returnaddr, "hardware"]

    logger.debug("Running: {}".format(" ".join(cmd)))
    try:
        with open(os.devnull, 'w') as fn:
            status = subprocess.check_call(" ".join(cmd), stdout=fn, stderr=fn, shell=True)
    except subprocess.CalledProcessError as e:
        status = e.returncode
        logger.error("ssh attempt to '{}' failed".format(remoteaddr))

    return status

def ping_network(ip_range_list, ipcnt, passes):
    """
    ping_network: Ping a range of ips until the amount of successful pings
    reaches a number n

    input: List of ip addresses to be pinged; Counter for threshold
    of successful pings; Number of iterations to pass

    output: List of ip addresses that were found to be up
    """
    logger = logging.getLogger("pharosvalidator")
    assert isinstance(ip_range_list, list)
    ips_found = 0
    alive_ips = []
    for t in range(passes):
        for addr in list(ip_range_list):
            cmd = [ \
                    "ping", \
                    "-c", "1", \
                    "-w", "1", \
                    addr]
            logger.debug("Running: \"{}\"".format(' '.join(cmd)))
            try:
                with open(os.devnull, 'w') as fn:
                    status = subprocess.check_call(" ".join(cmd), \
                            stdout=fn, stderr=fn, shell=True)
            except subprocess.CalledProcessError as e:
                status = e.returncode
                logger.error("Ping at '{}' failed".format(addr))
            # If the ip address was pinged successfully, then remove it from future attempts
            if status == 0:
                ips_found += 1
                logger.info("{} is up, {} total nodes up".format(addr, ips_found))

                # Remove the ip that was successfully pinged from being tested again
                ip_range_list.remove(addr)

                # Add the successfully pinged node to a list of successful pings
                alive_ips.append(addr)

            if ips_found >= ipcnt:
                break

        if ips_found >= ipcnt:
            break

    return alive_ips

def bring_up_admin_ip(ipaddr):
    """
    Assign the machine this test is running on an address according to the
    configuration file
    """
    cmd = [""]
    subprocess.Popen(cmd)
