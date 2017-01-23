##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
import struct
import socket
import ipaddress
import os
import netifaces

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

def approxsize(x, y, deviation):
    """Approximately compares 'x' to 'y' within % of 'deviation'"""
    logger = logging.getLogger(__name__)

    dev = (y * .01 * deviation)

    if x >= round(y - dev, 0) and x <= round(y + dev, 0):
        logger.debug("{} is approximately {}".format(x, y))
        return True
    else:
        logger.debug("{} is not approximately {}".format(x, y))
        return False

def read_line(sock):
    """Reads from a socket until a \n character or 512 bytes have been read,
    whichever comes first"""
    c = ""
    recvline = ""
    reads = 0
    while (c != "\n" and reads < 512):
        # Decode bytes to str, sockets output bytes which aren't pretty
        c = sock.recv(1).decode("utf-8")
        #print("char: '" + c + "'") # Debugging code
        recvline += c
        reads += 1
    return recvline

def read_msg(sock):
    """Reads a message prefixed with a number and a newline char, eg. "20\n"
    then reads x lines, where x is equal to the number in the first line."""
    # Read the socket once initially for the line count
    buf = read_line(sock)
    buf = buf[:-1] # Cut off the '\n' character
    length = int(buf)

    lines = []
    for i in range(length):
        lines.append(read_line(sock))
    return "".join(lines)

def send_msg(sock, msg):
    """Sends a message to a socket"""
    # Encode python str to bytes beforehand, sockets only deal in bytes
    msg = bytes(msg, "utf-8")
    totalsent = 0
    while totalsent < len(msg):
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            return -1
        totalsent = totalsent + sent
    return totalsent

def get_addrs():
    """Get the addresses of the machine that this program is running on"""
    addrs = [];
    for iface in netifaces.interfaces():
        for info in netifaces.ifaddresses(iface)[netifaces.AF_INET]:
            addrs.append(info["addr"])

    return addrs

def gen_ip_range(addr_and_cidr, excluded, minimum, maximum):
    """Takes a network adress with cidr number eg. (10.10.10.0/24),
    and then a min max value. Then creates a list of ip addresses avalable on [a,b] without
    "excluded" addresses"""
    logger = logging.getLogger(__name__)

    # Generate a list of available ip addresses for the dhcp server
    ip_range = list(map(lambda x: x.exploded, ipaddress.ip_network(addr_and_cidr).hosts()))

    if (None != excluded):
        for addr in excluded:
            # Remove the value from the list, if it isn't in the list then whatever
            try:
                ip_range.remove(addr)
            except ValueError:
                logger.debug("{} not in ip_range, cannot remove".format(addr))

    # Remove all values before the minimum usable value
    for i in range(len(ip_range)):
        if ip_range[i] == minimum:
            ip_range = ip_range[i::]
            break
    # Remove all values after the maximum usable value
    for i in range(len(ip_range)):
        if ip_range[i] == maximum:
            ip_range = ip_range[0:i+1]
            break
    return ip_range

def split_cidr(net_and_cidr):
    """
    split_cidr: Split up cidr notation subnets into a subnet string and a
    netmask string

    input: cidr notation of a subnet

    output: (Subnet string, Netmask string)
    """
    split = net_and_cidr.split('/')
    netmask = cidr_to_netmask(int(split[1]))

    return split[0], netmask

def cidr_to_netmask(cidr):
    bits = 0xffffffff ^ (1 << 32 - cidr) - 1
    netmask = socket.inet_ntoa(struct.pack('>I', bits))
    return netmask
