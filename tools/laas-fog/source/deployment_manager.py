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

import logging
from api.libvirt_api import Libvirt


class Deployment_Manager:
    """
    This class manages the deployment of OPNFV on a booked host
    if it was requested. If no OPNFV installer was requested, this class will
    create the virtual machines and networks in the config files and exit.
    """
    def __init__(self, installerType, scenario, utility):
        """
        init function
        """
        # installerType will either be the constructor for an installer or None
        self.installer = installerType
        self.virt = Libvirt(
                utility.host,
                net_conf=utility.conf['hypervisor_config']['networks'],
                dom_conf=utility.conf['hypervisor_config']['vms']
                )
        self.host = utility.host
        self.util = utility

    def getIso(self):
        """
        checks if any of the domains expect an ISO file to exist
        and retrieves it.
        """
        isoDom = None
        for dom in self.doms:
            if dom.iso['used']:
                isoDom = dom
                break
        if isoDom:
            path = isoDom.iso['location']
            url = isoDom.iso['URL']
            self.util.sshExec(['wget', '-q', '-O', path, url])

    def getDomMacs(self):
        """
        assigns the 'macs' instance variable to the domains
        so that they know the mac addresses of their interfaces.
        """
        for dom in self.doms:
            dom.macs = self.virt.getMacs(dom.name)

    def makeDisks(self):
        """
        Creates the qcow2 disk files the domains expect on the remote host.
        """
        disks = []
        for dom in self.doms:
            disks.append(dom.disk)
        self.util.execRemoteScript("mkDisks.sh", disks)

    def go(self):
        """
        'main' function.
        creates virtual machines/networks and either passes control to the
        OPNFV installer, or finishes up if an installer was not requested.
        """
        log = logging.getLogger(self.util.hostname)
        self.virt.setLogger(log)
        log.info("%s", "Connecting to the host hypervisor")
        self.virt.openConnection()
        domains, networks = self.virt.go()
        log.info("%s", "Created all networks and VM's on host")
        self.doms = domains
        self.nets = networks
        if self.installer is None:
            log.warning("%s", "No installer requested. Finishing deployment")
            self.util.finishDeployment()
            return
        log.info("%s", "retrieving ISO")
        self.getIso()
        self.getDomMacs()
        self.util.copyScripts()
        self.makeDisks()
        log.info("%s", "Beginning installation of OPNFV")
        try:
            installer = self.installer(
                    self.doms,
                    self.nets,
                    self.virt,
                    self.util
                    )
            installer.go()
        except Exception:
            log.exception('%s', "failed to install OPNFV")
