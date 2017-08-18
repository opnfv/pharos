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
from installer import Installer
from api.fuel_api import Fuel_api


class Fuel_Installer(Installer):
    """
    This class is the installer for any OPNFV scenarios which use Fuel as the
    installer. This class uses the libvirt api handler
    to create all the virtual hosts,
    then installs fuel and uses the fuel api handler
    to create and deploy an openstack environment

    This class will get much smarter and have less configuration hardcoded
    as we grow support for more OPNFV scenarios
    """

    def __init__(self, doms, nets, libvirt_handler, util):
        """
        init function
        Calls the super constructor
        """
        super(Fuel_Installer, self).__init__(doms, nets, libvirt_handler, util)
        url = 'http://'+self.libvirt.host+':8000/'
        self.handler = Fuel_api(url, self.log, 'admin', 'admin')
        self.fuelNets = None

    def bootMaster(self):
        """
        Boots the fuel master node and waits
        for it to come up
        """
        self.libvirt.bootMaster()
        time.sleep(100)

    def bootNodes(self):
        """
        Boots all the slave nodes
        """
        self.libvirt.bootSlaves()

    def waitForNodes(self, numNodes):
        """
        Waits for the nodes to pxe boot and be recognized by Fuel
        """
        done = False
        self.log.info("Waiting for %i nodes to boot into Fuel", numNodes)
        discoveredNodes = 0
        while not done:
            discoveredNodes = len(self.handler.getNodes())
            nodes = int(discoveredNodes)
            self.log.info("found %d nodes", nodes)

            done = discoveredNodes == numNodes

    def installMaster(self):
        """
        runs the fuelInstall script, which uses the fuel iso to
        install fuel onto the master node
        """
        self.util.execRemoteScript("ipnat.sh", [self.libvirt.host])
        self.util.execRemoteScript("fuelInstall.sh", [self.util.remoteDir])

    def makeOpenstack(self):
        """
        creates an openstack environment and saves
        the openstack id
        """
        self.osid = self.handler.createOpenstack()

    def addNodesToOpenstack(self):
        """
        Adds the nodes to the openstack environment with
        compute / controller + cinder roles
        """
        nodesList = [
            {"id": 1, "roles": ["controller", "cinder"]},
            {"id": 2, "roles": ["controller", "cinder"]},
            {"id": 3, "roles": ["controller", "cinder"]},
            {"id": 4, "roles": ["compute"]},
            {"id": 5, "roles": ["compute"]}
        ]

        self.handler.addNodes(self.osid, nodesList)

    def configNetworks(self):
        """
        configures the openstack networks by calling the 3 helper
        methods
        """
        self.configPublicNet()
        self.configStorageNet()
        self.configManagementNet()

    def configPublicNet(self):
        """
        sets the default public network
        changes the cidr, gateway, and floating ranges
        """
        networks = self.handler.getNetworks(self.osid)
        for net in networks['networks']:
            if net['name'] == "public":
                net["ip_ranges"] = [["10.20.1.10", "10.20.1.126"]]
                net['cidr'] = "10.20.1.0/24"
                net['gateway'] = "10.20.1.1"

        # updates the floating ranges
        rng = [["10.20.1.130", "10.20.1.254"]]
        networks['networking_parameters']['floating_ranges'] = rng
        self.handler.uploadNetworks(networks, self.osid)

    def configStorageNet(self):
        """
        sets the default storage network to have the right
        cidr and gateway, and no vlan
        """
        networks = self.handler.getNetworks(self.osid)
        for net in networks['networks']:
            if net['name'] == "storage":
                net["ip_ranges"] = [["10.20.3.5", "10.20.3.254"]]
                net["cidr"] = "10.20.3.0/24"
                net["meta"]["notation"] = "ip_ranges"
                net["meta"]["use_gateway"] = True
                net["gateway"] = "10.20.3.1"
                net["vlan_start"] = None
        self.handler.uploadNetworks(networks, self.osid)

    def configManagementNet(self):
        """
        sets the default management net to have the right
        cidr and gatewar and no vlan
        """
        networks = self.handler.getNetworks(self.osid)
        for net in networks['networks']:
            if net['name'] == "management":
                net["ip_ranges"] = [["10.20.2.5", "10.20.2.254"]]
                net["cidr"] = "10.20.2.0/24"
                net["meta"]["notation"] = "ip_ranges"
                net["meta"]["use_gateway"] = True
                net["gateway"] = "10.20.2.1"
                net["vlan_start"] = None
        self.handler.uploadNetworks(networks, self.osid)

    # TODO: make this method smarter. I am making too many assumptions about
    # the order of interfaces and networks
    def configIfaces(self):
        """
        assigns the proper networks to each interface of the nodes
        """
        for x in range(1, 6):
            idNum = x
            ifaceJson = self.handler.getIfaces(idNum)

            ifaceJson[0]['assigned_networks'] = [
                    {"id": 1, "name": "fuelweb_admin"},
                    {"id": 5, "name": "private"}
                    ]
            ifaceJson[2]['assigned_networks'] = [
                    {"id": 4, "name": "storage"}
                    ]
            ifaceJson[3]['assigned_networks'] = [
                    {"id": 3, "name": "management"}
                    ]
            if idNum < 4:
                ifaceJson[1]['assigned_networks'] = [{
                    "id": 2,
                    "name": "pubic"
                    }]

            self.handler.setIfaces(idNum, ifaceJson)

    def clearAdminIface(self, ifaceJson, node):
        """
        makes the admin interface have *only* the admin network
        assigned to it
        """
        for iface in ifaceJson:
            if iface['mac'] == node.macs['admin']:
                iface['assigned_networks'] = [{
                    "id": 1,
                    "name": "fuelweb_admin"
                    }]

    def deployOpenstack(self):
        """
        Once openstack is properly configured, this method
        deploy OS and returns when OS is running
        """
        self.log.info("%s", "Deploying Openstack environment.")
        self.log.info("%s", "This may take a while")
        self.handler.deployOpenstack(self.osid)

    def getKey(self):
        """
        Retrieves authentication tokens for the api handler,
        while allowing the first few attempts to fail to
        allow Fuel time to "wake up"
        """
        i = 0
        while i < 20:
            i += 1
            try:
                self.handler.getKey()
                return
            except Exception:
                self.log.warning("%s", "Failed to talk to Fuel api")
                self.log.warning("Exec try %d/20", i)
        try:
            self.handler.getKey()
        except Exception:
            self.logger.exception("%s", "Fuel api is unavailable")
            sys.exit(1)

    def go(self):
        """
        This method does all the work of this class.
        It installs the master node, boots the slaves
        into Fuel, creates and configures OS, and then
        deploys it and uses NAT to make the horizon dashboard
        reachable
        """
        self.libvirt.openConnection()
        self.log.info('%s', 'installing the Fuel master node.')
        self.log.info('%s', 'This will take some time.')
        self.installMaster()
        time.sleep(60)
        self.getKey()
        self.log.info('%s', 'The master node is installed.')
        self.log.info('%s', 'Waiting for bootstrap image to build')
        self.handler.waitForBootstrap()
        self.bootNodes()
        self.waitForNodes(5)
        self.log.info('%s', "Defining an openstack environment")
        self.makeOpenstack()
        self.addNodesToOpenstack()
        self.log.info('%s', "configuring interfaces...")
        self.configIfaces()
        self.log.info('%s', "configuring networks...")
        self.configNetworks()
        self.deployOpenstack()

        horizon = self.handler.getHorizonIP(self.osid)
        self.util.execRemoteScript(
                '/horizonNat.sh', [self.libvirt.host, horizon])
        notice = "You may access the Openstack dashboard at %s/horizon"
        self.log.info(notice, self.libvirt.host)

        self.libvirt.close()
        self.util.finishDeployment()
