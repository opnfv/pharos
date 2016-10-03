##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging

from pharosvalidator.util import approxsize

# Constant macros
from pharosvalidator.const import *

def cpu(cpudata):
    """Compares system cpu against the pharos specification"""
    results = []

    # Architecture evaluation, a value of 63 or greater indicates at least a 64-bit OS
    if cpudata["bitsize"] >= 63:
        val = True
    else:
        val = False
    result = {"architecture": {
                "pass": val,
                "description": str(cpudata["architecture"])}}
    results.append(result)

    # Core evaluation
    if cpudata["cores"] < MIN_CORECOUNT:
        val = False
    else:
        val = True
    desc = "Have {0}, Need at least {1}".format(cpudata["cores"], MIN_CORECOUNT)
    result = {"corecount": {
                "pass": val,
                "description": desc}}
    results.append(result)

    # Speed evaluation
    i = 0
    for cpufreq in cpudata["frequency"]:
        # Cpufrequency was not read if this is the result
        if cpufreq == -1:
            desc = "(Cpu freuency could not be read)"
        else:
            if approxsize(cpufreq, MIN_CPUFREQ, 5) or cpufreq > MIN_CPUFREQ:
                val = True
            else:
                val = False
            desc = "Have {:.2f}Mhz, Need at least ~= {:.2f}Mhz".format( \
                        cpufreq, MIN_CPUFREQ)
        result = {"cpu"+str(i): {
                    "pass": val,
                    "description": desc}}
        results.append(result)
        i += 1

    return results

def memory(memdata):
    """Compares system meminfo object against the pharos specification"""
    logger = logging.getLogger(__name__)

    results = []

    logger.debug("required memory: {}, detected memory: {}".format(\
            MIN_MEMSIZE, memdata["size"]))
    # Capacity evaluation
    if approxsize(memdata["size"], MIN_MEMSIZE, 5) or memdata["size"] > MIN_MEMSIZE:
        val = True
    else:
        val = False

    desc = "Have {:.2f}G, Need at least ~= {:.2f}G".format( \
            memdata["size"], MIN_MEMSIZE/1000000)

    result = {"memory capacity": {
                "pass": val,
                "description": desc}}
    results.append(result)

    return results

def storage(diskdata):
    """Compares system storage against the Pharos specification"""
    def sizecmp(a, b, unit):
        if approxsize(a, b, 10) or a > b:
            val = True
        else:
            val = False
        desc = "capacity is {:.2f}{}, Need at least ~= {:.2f}{}".format(a, \
                                                            unit,  b, unit)
        return (val,desc)

    results = []
    # Disk size evaluation (also counts the disks)
    diskcount = {"ssd":0, "non-ssd":0}
    for disk in diskdata["names"]:
        if diskdata["rotational"][disk]:
            disktype = "non-ssd"
            diskcount["non-ssd"] += 1
        else:
            disktype = "ssd"
            diskcount["ssd"] += 1
        val, desc = sizecmp(diskdata["sizes"][disk], MIN_SSDSIZE, 'G')
        data = diskdata["sizes"][disk]
        result = {disk: {
                    "pass": val,
                    "description": "Disk type: disktype; " + desc}}
        results.append(result)

    # Disk number evaluation
    if sum(diskcount.values()) >= 3 and diskcount["ssd"] >= 1:
        val = True
    else:
        val = False
    desc = "Have {0} drives, Need at least {1} drives and {3} ssds".format( \
            sum(diskcount.values()), MIN_DISKCOUNT, \
            diskcount["ssd"], MIN_SSDCOUNT)

    data = diskcount
    result = {"diskcount": {
                "pass": val,
                "description": desc}}
    results.append(result)
    return results

"""
def netinterfaces(netfaces):
    results = []
    for netface in netfaces:
        if netface.status <= 0:
            val = False
            state = "down"
        else:
            val = True
            state = "up"
        try:
            MACaddr = netface.MAC[0]["addr"]
        except IndexError:
            MACaddr = "no MAC"
        if len(netface.addrs) > 0:
            addrs = ""
            for addr in netface.addrs:
                if len(addrs) > 0:
                    addrs += ", "
                addrs += addr['addr']
            addrs = "addresses: " + addrs
        else:
            addrs = "no address"
        desc = "({0} is {1} with {2})".format(netface.name, state, addrs)
        data = MACaddr
        results.append(gen_yamltext(netface.name, val, desc, data))
    return results
    """

