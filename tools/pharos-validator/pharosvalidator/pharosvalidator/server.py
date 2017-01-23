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
import socket
import yaml
import threading
import queue
import argparse
import sys

from pharosvalidator import config
from pharosvalidator import pharos
from pharosvalidator import util
from pharosvalidator import dhcp
from pharosvalidator import ipmi

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
    run_remote_tests: ssh to a given remote address, and run a test program
    on the remote machine specifying the address and port of where the results
    should be sent (usually back to the machine this program was run on)

    input: ip address of the ssh target; Adress of the test results target;
    Port of the test results target

    output: 0 if the test ran over ssh perfectly, non-zero if the test faild
    """
    #TODO add way to keep attempting to ssh until service is up and running aka ping part 2
    logger = logging.getLogger(__name__)

    cmd = ["ssh", "-o", "UserKnownHostsFile=/dev/null", \
           "-o", "StrictHostKeyChecking=no", \
           "-i", "/etc/pharosvalidator/ssh/id_rsa", \
           "root@"+remoteaddr, "python3", "/usr/bin/pharosvalidator", "-p", port, \
           "node", "-H", returnaddr, "hardware"]

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
                logger.debug("Ping to '{}' failed, {} more tries".format(addr, passes - t))
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

# Below code is for receiving test results
def receiver_start(nodecount, port, q):
    """Start a server to retrieve the files from the nodes. Server will run
    indefinetely until the parent process ends"""
    logging.basicConfig(level=0)
    logger = logging.getLogger(__name__)

    address = "" # Empty means act as a server on all available interfaces

    logger.info("Bringing up receiver server...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((address, port))
    sock.listen(nodecount) # Max connections is the amount of nodes

    while True:
        # Receive a descriptor for the client socket, cl stands for client
        (clsock, claddress) = sock.accept()
        logger.info("Received client connection...")
        client_thread = threading.Thread(target=receiver_accept_thread, \
                args=(clsock, claddress, q), daemon=True)
        # Start a new thread to read the new client socket connection
        client_thread.start()

    socket.close()
    logger.info("Bringing down receiver server...")

def receiver_accept_thread(clsock, claddress, q):
    """Read from the socket into the queue, then close the connection"""
    logger = logging.getLogger(__name__)
    q.put(util.read_msg(clsock))
    logger.info("Retreived message from socket")
    clsock.close()

# Main driver procedure
def run(args):
    """PXE boot each nodes, then start up server to receive results"""
    logger = logging.getLogger(__name__)

    conf = config.ServerConfig(args.port, args.dhcp_init, \
                                         args.inventory_config, \
                                         args.network_config)

    # Create a new logger strictly for logging test results to a file
    test_logger = logging.getLogger('test_logger')
    test_logger.setLevel(logging.INFO)
    tl_handler = logging.FileHandler(args.t)
    tl_handler.setFormatter(logging.Formatter("%(message)s"))
    test_logger.addHandler(tl_handler)

    # Start dhcp server
    node_addrs = dhcp.gen_dhcpd_file(args.dhcpfile, conf.inventory["nodes"], conf.networks["admin"])
    logger.info(node_addrs)
    if dhcp.start_dhcp_service(conf.init_cmd) != 0:
        logger.error("Halting, cannot bring up dhcp server")
        quit()

    # Queue for holding test logs, makes program thread safe
    logs_q = queue.Queue()
    # Start a new thread for the server that receives results
    threading.Thread(target=receiver_start, \
            args=(conf.nodecount(), conf.port, logs_q), \
            daemon=True).start()
    # First power off all nodes
    # ipmi.power_nodes(conf.inventory["nodes"], "off")
    failed_nodes = ipmi.power_nodes(conf.inventory["nodes"], "on")

    # If the failed nodes list is not empty, then fail
    if failed_nodes != []:
        logger.error("Halting, {} were unable to be powered on".format(", ".join(failed_nodes)))
        quit()

    admin_network = conf.networks["admin"]

    available_ips = ping_network(ip_range_list=node_addrs, ipcnt=conf.nodecount(), passes=1000)
    logger.info(available_ips)

    # Start a thread to run tests on each different node, and setup
    # their NICs
    for ip in available_ips:
        threading.Thread( \
                target=ssh_thread, \
                args=(str(ip), str(admin_network.installer_ip), str(conf.port), 200), \
                daemon=True).start()
    for node in conf.inventory["nodes"]:
        logger.info("Awaiting test result...")
        test_logger.info(logs_q.get())
        logger.info("Logging test result...")
    logger.info("Finished test, powering off nodes")
    ipmi.power_nodes(conf.inventory["nodes"], "off")
