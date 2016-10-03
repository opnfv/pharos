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

from pharosvalidator.util import cd # Contains the pharos specification values

# Static vars
mempath="/proc/meminfo"
cpuinfopath="/proc/cpuinfo"
cpupath="/sys/devices/system/cpu/"
diskpath="/sys/block/"

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

def cpu():
    logger = logging.getLogger(__name__)
    cpudata = {}
    cpuinfo = readproc(cpuinfopath)
    cpudata["bitsize"] = sys.maxsize.bit_length()
    cpudata["architecture"] = platform.architecture()[0]
    cpudata["cores"] = int(cpuinfo["cpu cores"])
    cpudata["frequency"] = []
    for i in range(cpudata["cores"]):
        freqpath = "{0}/cpu{1}/cpufreq/cpuinfo_max_freq".format(cpupath, \
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

def memory():
    logger = logging.getLogger(__name__)
    meminfo=readproc(mempath)
    # Create the memory object to store memory information
    memdata = {}
    memdata["size"] = (int(meminfo["MemTotal"].split(' ')[0]))/1000000
    return memdata

def storage():
    """Gather's disk information"""
    logger = logging.getLogger(__name__)
    diskdata = {"names":[],"rotational":{},"sizes":{}}
    for disk in os.listdir(diskpath):
        #sdX is the naming schema for IDE/SATA interfaces in Linux
        if re.match(r"sd\w",disk):
            logger.debug("Found disk {}".format(disk))
            diskdata["names"].append(disk)
            sizepath = "{0}/{1}/size".format(diskpath, disk)
            try:
                with open(sizepath) as fd:
                    size = int(fd.read(-1))
            except IOError:
                size = -1
            # If the read was successful
            if size != -1:
                # Converts the value to Gb
                diskdata["sizes"][disk] = (size * 512)/1000000000

            rotationalpath = "{0}/{1}/queue/rotational".format(diskpath, disk)
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

def netinterfaces(nodeinfo):
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
