##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
import socket
import yaml
import os

import pharosvalidator.test as pharostest
from pharosvalidator.util import send_msg

# Main driver procedure
def run(args):
    logger = logging.getLogger(__name__)

    # Create a new logger strictly for logging test results to a file
    test_logger = logging.getLogger('test_logger')
    test_logger.setLevel(logging.INFO)
    tl_handler = logging.FileHandler(args.t)
    tl_handler.setFormatter(logging.Formatter("%(message)s"))
    test_logger.addHandler(tl_handler)

    #Run validation tests, then send results back to server on jump host
    if args.test == "hardware":
        result = hardware_test()
    elif args.test == "network":
        result = network_test()
    else:
        logger.error("Invalid test name chosen, please choose \"hardware\" or \"network\"")
        quit()

    logger.debug("TEST RESULTS\n" + "#"*50 + '\n' + result + "#"*50 + '\n')
    logger.info("Sending results to host...")
    send_test_result(args.host, args.port, result)

def hardware_test():
    """
    hardware_test: Run hardware probing/testing functions

    input: None

    output: String in YAML format of the tests that were run
    """
    logger = logging.getLogger(__name__)
    logger.info("Beginning hardware test")

    # Run test scripts
    results = []
    results.append(pharostest.testinterpreter("CPU test", pharostest.eval_cpu, \
                                               pharostest.probe_cpu()))
    results.append(pharostest.testinterpreter("Mem test", pharostest.eval_memory,
                                               pharostest.probe_memory()))
    results.append(pharostest.testinterpreter("Storage test", pharostest.eval_storage, \
                                                   pharostest.probe_storage()))
    # Start generating the yaml file
    yamltext = ""
    for result in results:
        yamltext += yaml.dump(result, default_flow_style=False)
    return yamltext

def network_test(networkfile):
    logger = logging.getLogger(__name__)
    logger.info("Beginning network test")
    logger.info("Ending network test")
    pass

def send_test_result(host, port, result):
    """
    send_result: Send the final test result to the central test server

    input: Host address of target; Port of target; String to send to server

    output: None
    """
    logger = logging.getLogger(__name__)
    logger.info("Sending test result")

    # Format the results properly
    linecount = 0
    for c in result:
        if c == "\n":
            linecount += 1

    result = str(linecount) + "\n" + result

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, int(port)))
    send_msg(sock, result)
