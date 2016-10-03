#!/usr/bin/env python3
# bin/setup_interface

# -----------------------------------------------------------------------

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ------------------------------------------------------------------------

# Author: Todd Gaunt, toddgaunt@iol.unh.edu or toddgaunt@gmail.com
# License: Apache v2.0
# Description: Script for setting up initial network interfaces
# it activates dhcp on all interfaces in order to at least get the admin
# network up

import os
import subprocess
import netifaces

def generate_interfaces_file(ifaces, os_network_file):
    """Takes a list of interfaces and a location to save a network
    interfaces file"""
    interfaces = ""
    for i in ifaces:
        n = "auto " + str(i) + "\n" \
            + "iface " + str(i) + " inet dhcp\n"
        interfaces += n
    return interfaces

def set_interfaces_up(ifaces):
    """Uses ifup command to put network devices up according to
    interfaces file"""
    for iface in ifaces:
        ifupcmd = [ \
                "ifup",
                iface]
        ifdowncmd = [ \
                "ifdown",
                iface]
        with open(os.devnull, 'w') as fn:
            status = subprocess.Popen(ifdowncmd, stdout=fn, stderr=fn).wait()
            status = subprocess.Popen(ifupcmd, stdout=fn, stderr=fn).wait()
        print(str(iface) + " " + str(status))

def main():
    os_network_file="/etc/network/interfaces"
    ifaces = netifaces.interfaces()
    interfaces = generate_interfaces_file(ifaces, os_network_file)
    with open(os_network_file, 'w') as fd:
        fd.write(interfaces)
    set_interfaces_up(ifaces)

if __name__ == "__main__":
    main()
