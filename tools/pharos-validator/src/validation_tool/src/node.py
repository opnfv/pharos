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

import pharosvalidator.test.probe as probe
import pharosvalidator.test.evaluate as evaluate
from pharosvalidator.util import send_msg

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
    results.append(testinterpreter("CPU test", evaluate.cpu, probe.cpu()))
    results.append(testinterpreter("Memory test", evaluate.memory, probe.memory()))
    results.append(testinterpreter("Storage test", evaluate.storage, probe.storage()))

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

def send_result(host, port, result):
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

def testinterpreter(name, test, dataset):
    """High level function for test functions within this module to print out
    their results in an ordered function while also writing out logs,
    expects a list of testresults objects"""

    # Start the yaml file contents
    data = {name:[]}

    # test the dataset
    results = test(dataset)

    for result in results:
        data[name].append(result)

    return data
