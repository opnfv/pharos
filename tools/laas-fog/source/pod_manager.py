#!/usr/bin/python
"""
#############################################################################
#Copyright 2017 Parker Berberian and others                                 #
#                                                                           #
#Licensed under the Apache License, Version 2.0 (the "License");            #
#you may not use this file except in compliance with the License.           #
#You may obtain a copy of the License at                                    #
#                                                                           #
#    http://www.apache.org/licenses/LICENSE-2.0                             #
#                                                                           #
#Unless required by applicable law or agreed to in writing, software        #
#distributed under the License is distributed on an "AS IS" BASIS,          #
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
#See the License for the specific language governing permissions and        #
#limitations under the License.                                             #
#############################################################################
"""

import time
import sys
import yaml
import os
from api.fog import FOG_Handler
from utilities import Utilities
from deployment_manager import Deployment_Manager
from database import HostDataBase
from installers import fuel
from installers import joid


class Pod_Manager:
    """
    This is the 'main' class that chooses a host and provisions & deploys it.
    this class can be run directly from the command line,
    or it can be called from the pharos dashboard listener when
    a deployment is requested.
    Either way, this file should be called with:
        ./pod_manager.py --config <CONFIG_FILE>
    """
    # This dictionary allows me to map the supported installers to the
    # respective installer classes, for easier parsing of the config file
    INSTALLERS = {
            "fuel": fuel.Fuel_Installer,
            "joid": joid.Joid_Installer,
            "none": None
            }

    def __init__(self, conf, requested_host=None, reset=False):
        """
        init function.
        conf is the read and parsed config file for this deployment
        requested_host is the optional hostname of the host you request
        if reset, we just flash the host to a clean state and return.
        """
        self.conf = conf
        if self.conf['installer'] is not None:
            inst = Pod_Manager.INSTALLERS[self.conf['installer'].lower()]
            self.conf['installer'] = inst
        self.fog = FOG_Handler(self.conf['fog']['server'])
        # Sets the fog keys, either from the config file
        # or the secrets file the config points to
        if os.path.isfile(self.conf['fog']['api_key']):
            self.fog.getFogKeyFromFile(self.conf['fog']['api_key'])
        else:
            self.fog.setFogKey(self.conf['fog']['api_key'])

        if os.path.isfile(self.conf['fog']['user_key']):
            self.fog.getUserKeyFromFile(self.conf['fog']['user_key'])
        else:
            self.fog.setUserKey(self.conf['fog']['user_key'])
        self.database = HostDataBase(self.conf['database'])
        self.request = requested_host
        if reset:
            mac = self.fog.getHostMac(self.request)
            log = self.conf['dhcp_log']
            dhcp_serv = self.conf['dhcp_server']
            ip = Utilities.getIPfromMAC(mac, log, remote=dhcp_serv)
            self.flash_host(self.request, ip)

    def start_deploy(self):
        """
        Ghosts the machine with the proper disk image and hands off
        control to the deployment manager.
        """
        try:
            host = self.database.getHost(self.request)
            hostMac = self.fog.getHostMac(host)
            dhcp_log = self.conf['dhcp_log']
            dhcp_server = self.conf['dhcp_server']
            host_ip = Utilities.getIPfromMAC(
                    hostMac, dhcp_log, remote=dhcp_server
                    )
            util = Utilities(host_ip, host, self.conf)
            util.resetKnownHosts()
            log = Utilities.createLogger(host, self.conf['logging_dir'])
            self.fog.setLogger(log)
            log.info("Starting booking on host %s", host)
            log.info("host is reachable at %s", host_ip)
            log.info('ghosting host %s with clean image', host)
            self.flash_host(host, host_ip, util)
            log.info('Host %s imaging complete', host)
            inst = self.conf['installer']
            scenario = self.conf['scenario']
            Deployment_Manager(inst, scenario, util).go()
        except Exception:
            log.exception("Encountered an unexpected error")

    def flash_host(self, host, host_ip, util=None):
        """
        We do this using a FOG server, but you can use whatever fits into your
        lab infrastructure. This method should put the host into a state as if
        centos was just freshly installed, updated,
        and needed virtualization software installed.
        This is the 'clean' starting point we work from
        """
        self.fog.setImage(host, self.conf['fog']['image_id'])
        self.fog.imageHost(host)
        Utilities.restartRemoteHost(host_ip)
        self.fog.waitForHost(host)
        # if util is not given, then we are just
        # flashing to reset after a booking expires
        if util is not None:
            time.sleep(30)
            util.waitForBoot()
            util.checkHost()
            time.sleep(15)
            util.checkHost()


if __name__ == "__main__":
    configFile = ""
    host = ""
    for i in range(len(sys.argv) - 1):
        if "--config" in sys.argv[i]:
            configFile = sys.argv[i+1]
        elif "--host" in sys.argv[i]:
            host = sys.argv[i+1]
    if len(configFile) < 1:
        print "No config file specified"
        sys.exit(1)
    configFile = yaml.safe_load(open(configFile))
    manager = Pod_Manager(configFile, requested_host=host)
    manager.start_deploy()
