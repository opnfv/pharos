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

import libvirt
import time
import xml.dom
import xml.dom.minidom
from domain import Domain
from network import Network
from utilities import Utilities


class Libvirt:
    """
    This class talks to the Libvirt api.
    Given a config file, this class should create all networks and
    domains.

    TODO: convert prints to logging and remove uneeded pass statements
    """

    def __init__(self, hostAddr, net_conf=None, dom_conf=None):
        """
        init function
        hostAddr is the ip address of the host
        net_conf and dom_conf are the paths
        to the config files
        """
        self.host = hostAddr
        self.URI = "qemu+ssh://root@"+str(hostAddr)+"/system"
        self.hypervisor = None
        self.domains = []
        self.networks = []
        self.net_conf = net_conf
        self.dom_conf = dom_conf

    def setLogger(self, log):
        """
        Saves the logger in self.log
        """
        self.log = log

    def bootMaster(self):
        """
        starts the previously defined master node
        """
        for dom in self.domains:
            if 'master' in dom.name():
                try:
                    dom.create()
                except Exception:
                    pass

    def bootSlaves(self):
        """
        boots every defined vm with 'slave' in its name
        """
        for dom in self.domains:
            if 'slave' in dom.name():
                try:
                    dom.create()
                    self.log.info("Booting %s", dom.name())
                except Exception:
                    self.log.exception("%s", "failed to boot domain")
                time.sleep(5)

    def getMacs(self, domName):
        """
        returns a dictionary with a network name
        mapped to the mac address of the domain on that net
        """
        try:
            dom = self.hypervisor.lookupByName(domName)
            xmlDesc = dom.XMLDesc(0)
            parsedXML = xml.dom.minidom.parseString(xmlDesc)
            interfacesXML = parsedXML.getElementsByTagName('interface')
            netDict = {}
            for iface in interfacesXML:
                src = iface.getElementsByTagName('source')[0]
                mac = iface.getElementsByTagName('mac')[0]
                netDict[src] = mac
            return netDict
        except Exception:
            self.log.exception("%s", "Domain not found")

    def defineVM(self, xmlConfig):
        """
        Generic method to define a persistent vm with the
        given config.
        Assumes that self.hypervisor is already connected.
        """
        if self.checkForVM(xmlConfig):
            vm = self.hypervisor.defineXML(xmlConfig)
            if vm is None:
                name = self.getName(xmlConfig)
                self.log.error("Failed to define vm %s. exiting", name)
                exit(1)
            else:
                self.log.info("Successfully created vm %s", vm.name())
                pass
            self.domains.append(vm)

    def checkForVM(self, xmlConfig):
        """
        Checks if another vm with the same name exists
        on the remote host already. If it does, it will
        delete that vm
        """
        allGood = False
        vms = self.hypervisor.listAllDomains(0)
        names = []
        for dom in vms:
            names.append(dom.name())
        vmName = Utilities.getName(xmlConfig)
        if vmName in names:
            self.log.warning("domain %s already exists", vmName)
            self.log.warning("%s", "Atempting to delete it")
            self.deleteVM(vmName)
            allGood = True
        else:
            allGood = True
        return allGood

    def deleteVM(self, name):
        """
        removes the given vm from the remote host
        """
        try:
            vm = self.hypervisor.lookupByName(name)
        except:
            return
        active = vm.isActive()
        persistent = vm.isPersistent()
        if active:
            try:
                vm.destroy()
            except:
                self.log.exception("%s", "Failed to destroy vm")

        if persistent:
            try:
                vm.undefine()
            except:
                self.log.exception("%s", "Failed to undefine domain")
                pass

    def openConnection(self):
        """
        opens a connection to the remote host
        and stores it in self.hypervisor
        """
        self.log.info("Attempting to connect to libvirt at %s", self.host)
        try:
            hostHypervisor = libvirt.open(self.URI)
        except:
            self.log.warning(
                    "Failed to connect to %s. Trying again", self.host
                    )
            time.sleep(5)
            try:
                hostHypervisor = libvirt.open(self.URI)
            except:
                self.log.exception("Cannot connect to %s. Exiting", self.host)
                exit(1)

        if hostHypervisor is None:
            self.log.error("Failed to connect to %s. Exiting", self.host)
            exit(1)
        self.hypervisor = hostHypervisor

    def restartVM(self, vm):
        """
        causes the given vm to reboot
        """
        dom = self.hypervisor.lookupByName(vm)
        dom.destroy()
        time.sleep(15)
        dom.create()

    def close(self):
        """
        Closes connection to remote hypervisor
        """
        self.log.info("Closing connection to the hypervisor %s", self.host)
        self.hypervisor.close()

    def defineAllDomains(self, path):
        """
        Defines a domain from all the xml files in a directory
        """
        files = Utilities.getXMLFiles(path)
        definitions = []
        for xml_desc in files:
            definitions.append(xml_desc.read())

        for definition in definitions:
            self.defineVM(definition)

    def createAllNetworks(self, path):
        """
        Creates a network from all xml files in a directory
        """
        files = Utilities.getXMLFiles(path)
        definitions = []
        for xml_desc in files:
            definitions.append(Utilities.fileToString(xml_desc))

        for definition in definitions:
            self.createNet(definition)

    def createNet(self, config):
        """
        creates the network on the remote host
        config is the xml in string representation
        that defines the network
        """
        if self.checkNet(config):
            network = self.hypervisor.networkDefineXML(config)

            if network is None:
                name = self.getName(config)
                self.log.warning("Failed to define network %s", name)
            network.create()
            if network.isActive() == 1:
                net = network.name()
                self.log.info("Successfully defined network %s", net)
            self.networks.append(network)

    def checkNet(self, config):
        """
        Checks if another net with the same name exists, and
        deletes that network if one is found
        """
        allGood = False
        netName = Utilities.getName(config)
        if netName not in self.hypervisor.listNetworks():
            return True
        else:  # net name is already used
            self.log.warning(
                    "Network %s already exists. Trying to delete it", netName
                    )
            network = self.hypervisor.networkLookupByName(netName)
            self.deleteNet(network)
            allGood = True
        return allGood

    def deleteNet(self, net):
        """
        removes the given network from the host
        """
        active = net.isActive()
        persistent = net.isPersistent()
        if active:
            try:
                net.destroy()
            except:
                self.log.warning("%s", "Failed to destroy network")

        if persistent:
            try:
                net.undefine()
            except:
                self.log.warning("%s", "Failed to undefine network")

    def go(self):
        """
        This method does all the work of this class,
        Parsing the net and vm config files and creating
        all the requested nets/domains
        returns a list of all networks and a list of all domains
        as Network and Domain objects
        """
        nets = self.makeNetworks(self.net_conf)
        doms = self.makeDomains(self.dom_conf)
        return doms, nets

    def makeNetworks(self, conf):
        """
        Given a path to a  config file, this method
        parses the config and creates all requested networks,
        and returns them in a list of Network objects
        """
        networks = []
        definitions = Network.parseConfigFile(conf)
        for definition in definitions:
            network = Network(definition)
            networks.append(network)
            self.createNet(network.toXML())
        return networks

    def makeDomains(self, conf):
        """
        Given a path to a config file, this method
        parses the config and creates all requested vm's,
        and returns them in a list of Domain objects
        """
        domains = []
        definitions = Domain.parseConfigFile(conf)
        for definition in definitions:
            domain = Domain(definition)
            domains.append(domain)
            self.defineVM(domain.toXML())
        return domains

    @staticmethod
    def getName(xmlString):
        """
        given xml with a name tag, this returns the value of name
        eg:
            <name>Parker</name>
        returns 'Parker'
        """
        xmlDoc = xml.dom.minidom.parseString(xmlString)
        nameNode = xmlDoc.documentElement.getElementsByTagName('name')
        name = str(nameNode[0].firstChild.nodeValue)
        return name
