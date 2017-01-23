##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import re
import sys
import platform
import subprocess
import netifaces
import logging
from pharosvalidator.util import approxsize, cd
from pharosvalidator.pharos import *

# Static vars
MEMPATH="/proc/meminfo"
CPUINFOPATH="/proc/cpuinfo"
CPUPATH="/sys/devices/system/cpu/"
DISKPATH="/sys/block/"

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

def readproc(path):
    """Reads and parses /proc from [path] argument files
    and returns a hashmap of values"""
    logger = logging.getLogger(__name__)
    # Fail if path does not exist
    try:
        hashmap = {}
        with open(path) as fd:
            logger.debug("Reading {}".format(path))
            for line in fd:
                data = line.split(":")
                if len(data) == 2:
                    # Strip trailing characters from hashmap names and entries
                    # for less junk
                    hashmap[data[0].strip()] = data[1].strip()
        return hashmap
    except IOError:
        logger.error("Path to file does not exist: {}".format(path))
        quit(1)

def probe_cpu():
    logger = logging.getLogger(__name__)
    cpudata = {}
    cpuinfo = readproc(CPUINFOPATH)
    cpudata["bitsize"] = sys.maxsize.bit_length()
    cpudata["architecture"] = platform.architecture()[0]
    cpudata["cores"] = int(cpuinfo["cpu cores"])
    cpudata["frequency"] = []
    for i in range(cpudata["cores"]):
        freqpath = "{0}/cpu{1}/cpufreq/cpuinfo_max_freq".format(CPUPATH, \
                                                                str(i))
        try:
            with open(freqpath) as fd:
                logger.debug("Opening {}".format(freqpath))
                cpufreq = (float(fd.read(-1)))/1000
        except IOError:
            # Less accurate way of getting cpu information as
            # this frequency may change during operation,
            # if dynamic frequency scaling is enabled,
            # however it is better than nothing.
            logger.error("Path to file does not exist: {}".format(freqpath))
            logger.error("Reading cpu frequency from {} instead".format(freqpath))
            cpufreq = float(cpuinfo["cpu MHz"])

        if cpufreq < 0:
            cpudata["frequency"].append(0)
        else:
            cpudata["frequency"].append(cpufreq)

    return cpudata

def probe_memory():
    logger = logging.getLogger(__name__)
    meminfo=readproc(MEMPATH)
    # Create the memory object to store memory information
    memdata = {}
    memdata["size"] = (int(meminfo["MemTotal"].split(' ')[0]))/1000000
    return memdata

def probe_storage():
    """Gather's disk information"""
    logger = logging.getLogger(__name__)
    diskdata = {"names":[],"rotational":{},"sizes":{}}
    for disk in os.listdir(DISKPATH):
        #sdX is the naming schema for IDE/SATA interfaces in Linux
        if re.match(r"sd\w",disk):
            logger.debug("Found disk {}".format(disk))
            diskdata["names"].append(disk)
            sizepath = "{0}/{1}/size".format(DISKPATH, disk)
            try:
                with open(sizepath) as fd:
                    size = int(fd.read(-1))
            except IOError:
                size = -1
            # If the read was successful
            if size != -1:
                # Converts the value to Gb
                diskdata["sizes"][disk] = (size * 512)/1000000000

            rotationalpath = "{0}/{1}/queue/rotational".format(DISKPATH, disk)
            try:
                with open(rotationalpath) as fd:
                    rotational = int(fd.read(-1))
            except IOError:
                rotational = -1
            if rotational == 0:
                diskdata["rotational"][disk] = False
            else:
                diskdata["rotational"][disk] = True

    return diskdata

def probe_netinterfaces(nodeinfo):
    """Uses netifaces to probe the system for network interface information"""
    netfaces = []
    for interface in netifaces.interfaces():
        netface = netdata()
        netface.name = interface
        tmp = netifaces.ifaddresses(interface)
        # If the interface is up and has at least one ip address
        if netifaces.AF_INET in tmp:
            netface.status = 1 # 1 stands for "up"
            netface.addrs = tmp[netifaces.AF_INET]
        # If the interface is down
        else:
            netface.status = 0 # 0 stands for "down"
        # The file /proc/net/arp may also be used to read MAC addresses
        if netifaces.AF_LINK in tmp:
            netface.MAC = tmp[netifaces.AF_LINK]
        netfaces.append(netface)

    return netfaces

def eval_cpu(cpudata):
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

def eval_memory(memdata):
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

def eval_storage(diskdata):
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
