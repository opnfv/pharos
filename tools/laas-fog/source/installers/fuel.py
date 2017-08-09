"""
This class is the installer for any OPNFV scenarios which use Fuel as the 
installer. This class uses the libvirt api handler to create all the virtual hosts,
then installs fuel and uses the fuel api handler to create and deploy an openstack environment
"""

import sys
import time
import json
from network import Network
from domain import Domain
from utilities import Utilities
from installer import Installer
from api.fuel_api import Fuel_api

class Fuel_Installer(Installer): 
    
    def __init__(self,domList,netList,libvirt_handler,util):
        super(Fuel_Installer,self).__init__(domList,netList,libvirt_handler,util)
        self.handler = Fuel_api('http://'+self.libvirt.host+":8000/",self.log,'admin','admin')
        self.fuelNets = None
        #self.log = util.createLogger(util.hostname)

    def bootMaster(self):
        self.libvirt.bootMaster()
        time.sleep(100)

    def bootNodes(self):
        self.libvirt.bootSlaves()

    def waitForNodes(self,numNodes):
        done = False
        self.log.info("Waiting for %i nodes to boot into Fuel",numNodes)
        discoveredNodes = 0
        while not done:
            discoveredNodes = len(self.handler.getNodes())
            self.log.info("found %i/%i nodes",(discoveredNodes,numNodes))

            done = discoveredNodes == numNodes

    def installMaster(self):
        #copies the fuelInstall script to the master and runs it
        self.util.execRemoteScript("ipnat.sh",[self.libvirt.host])
        self.util.execRemoteScript("fuelInstall.sh",[self.util.remoteDir])

    def makeOpenstack(self):
        self.osid = self.handler.createOpenstack()

    def addNodesToOpenstack(self):
        nodesList = [
            {"id": 1, "roles": ["controller", "cinder"]}, 
            {"id": 2, "roles": ["controller", "cinder"]}, 
            {"id": 3, "roles": ["controller", "cinder"]}, 
            {"id": 4, "roles": ["compute"]}, 
            {"id": 5, "roles": ["compute"]}
        ]

        self.handler.addNodes(self.osid,nodesList)

    
    def configNetworks(self):
        self.configPublicNet()
        self.configStorageNet()
        self.configManagementNet()

    def configPublicNet(self):
        networks = self.handler.getNetworks(self.osid)
        for net in networks['networks']:
            if net['name'] == "public":
                net["ip_ranges"] = [["10.20.1.10","10.20.1.126"]]
                net['cidr'] = "10.20.1.0/24"
                net['gateway'] = "10.20.1.1"
        
        #updates the floating ranges
        networks['networking_parameters']['floating_ranges'] = [["10.20.1.130","10.20.1.254"]]
        self.handler.uploadNetworks(networks,self.osid)

    def configStorageNet(self):
        networks = self.handler.getNetworks(self.osid)
        for net in networks['networks']:
            if net['name'] == "storage":
                net["ip_ranges"] = [["10.20.3.5","10.20.3.254"]]
                net["cidr"] = "10.20.3.0/24"
                net["meta"]["notation"] = "ip_ranges"
                net["meta"]["use_gateway"] = True
                net["gateway"] = "10.20.3.1"
                net["vlan_start"] = None
        self.handler.uploadNetworks(networks,self.osid)

    def configManagementNet(self):
        networks = self.handler.getNetworks(self.osid)
        for net in networks['networks']:
            if net['name'] == "management":
                net["ip_ranges"] = [["10.20.2.5","10.20.2.254"]]
                net["cidr"] = "10.20.2.0/24"
                net["meta"]["notation"] = "ip_ranges"
                net["meta"]["use_gateway"] = True
                net["gateway"] = "10.20.2.1"
                net["vlan_start"] = None
        self.handler.uploadNetworks(networks,self.osid)

    
    #TODO: make this method smarter. I am making too many assumptions about 
    #the order of interfaces and networks
    def configIfaces(self):
        for x in range(1,6):
            idNum = x
            ifaceJson = self.handler.getIfaces(idNum)
        
            ifaceJson[0]['assigned_networks'] = [{"id":1,"name":"fuelweb_admin"},{"id":5,"name":"private"}]
            ifaceJson[2]['assigned_networks'] = [{"id":4,"name":"storage"}]
            ifaceJson[3]['assigned_networks'] = [{"id":3,"name":"management"}]
            if idNum < 4:
                ifaceJson[1]['assigned_networks'] = [{"id":2,"name":"pubic"}]
            
            self.handler.setIfaces(idNum,ifaceJson)
    
    def clearAdminIface(self,ifaceJson,node):
        for iface in ifaceJson:
            if iface['mac'] == node.macs['admin']:
                iface['assigned_networks'] = [{"id":1,"name":"fuelweb_admin"}]
    
    def configPublicIfaces(self,ifaceJson,node):
        for interface in ifaceJson:
            if interface['mac'] == node.macs['public']:
                netID = self.handler.getNetID('public',self.osid)
                if netID < 0:
                    self.log.warning('%s',"cannot find public network")
                interface['assigned_networks'] = [{"id": netID,"name": "public"}]
    
    def configStorageIfaces(self,ifaceJson,node):
        for interface in ifaceJson:
            if interface['mac'] == node.macs['storage']:
                netID = self.handler.getNetID('storage',self.osid)
                if netID < 0:
                    self.log.warning('%s',"cannot find storage network")
                interface['assigned_networks'] = [{"id": netID,"name": "storage"}]
    
    def configManagementIfaces(self,ifaceJson,node):
        for interface in ifaceJson:
            if interface['mac'] == node.macs['management']:
                netID = self.handler.getNetID('management',self.osid)
                if netID < 0:
                    self.log.warning('%s',"cannot find management network")
                interface['assigned_networks'] = [{"id": netID,"name": "management"}]


    def deployOpenstack(self):
        self.log.info("%s","Deploying Openstack environment. This may take a while")
        self.handler.deployOpenstack(self.osid)

    def go(self):
        self.libvirt.openConnection()
        self.log.info('%s','installing the Fuel master node. This will take some time.')
        self.installMaster()
        time.sleep(45)
        self.handler.getKey()
        self.log.info('%s','The master node is installed. Waiting for bootstrap image to build')
        self.handler.waitForBootstrap()
        self.bootNodes()
        self.waitForNodes(5)
        self.log.info('%s',"Defining an openstack environment")
        self.makeOpenstack()
        self.addNodesToOpenstack()
        self.log.info('%s',"configuring interfaces...")
        self.configIfaces()
        self.log.info('%s',"configuring networks...")
        self.configNetworks()
        self.deployOpenstack()
        
        horizon = self.handler.getHorizonIP(self.osid)
        self.util.execRemoteScript('/horizonNat.sh',[self.libvirt.host,horizon])
        self.log.info("You may access the Openstack Horizon dashboard at %s/horizon",self.libvirt.host)
        
        self.libvirt.close()
        self.util.finishDeployment()
