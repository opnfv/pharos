import os
import libvirt
import time
import subprocess
import xml.dom
import xml.dom.minidom

from domain import Domain
from network import Network
from utilities import Utilities
"""
This class talks to the Libvirt api. Given a config file, this class should create all networks and 
domains.



TODO: convert prints to logging and remove uneeded pass statements
"""

class Libvirt:


    def __init__(self, hostAddr,net_conf=None,dom_conf=None,interact=False):
        self.host = hostAddr
        self.URI = "qemu+ssh://root@"+str(hostAddr)+"/system"
        #self.checkHost()
        self.hypervisor = None
        self.domains = []
        self.networks = []
        self.net_conf = net_conf
        self.dom_conf = dom_conf
        #If program is run in foreground interactively, it will ask for
        #permission before deleting existing networks
        self.delAllNets = not interact
        self.delAllDoms = not interact

    
    def bootMaster(self):
        for dom in self.domains:
            if 'master' in dom.name():
                try:
                    dom.create()
                except Exception:
                    pass

    def bootSlaves(self):
        for dom in self.domains:
            if 'slave' in dom.name():
                try:
                    dom.create()
                    #print "booting "+dom.name()
                except Exception:
                    pass
                    #print "failed to boot domain"
                time.sleep(5)
    
    
    def getAdminMac(self,dom):
        xmlDesc = dom.XMLDesc(0)
        parsedXml = xml.dom.minidom.parseSrtring(xmlDesc)
        interfacesXML = parsedXML.getElementsByTagName('interface')
        for iface in interfacesXML:
            if 'admin' in iface.getElementsByTagName('source')[0].getAttribute('network'):
                return interface.getElementsByTagName('mac')[0].getAttribute('address')
               

    def getMacs(self,domName):
        try:
            dom = self.hypervisor.lookupByName(domName)
            xmlDesc = dom.XMLDesc(0)
            parsedXML = xml.dom.minidom.parseString(xmlDesc)
            interfacesXML = parsedXML.getElementsByTagName('interface')
            ##print interfacesXML
            netDict = {}
            targetNets = ['admin','public','private','storage','management']
            for iface in interfacesXML:
                for targetNet in targetNets:
                    if targetNet in iface.getElementsByTagName('source')[0].getAttribute('network'):
                        netDict[targetNet] = iface.getElementsByTagName('mac')[0].getAttribute('address')
            return netDict
        except Exception:
            pass
            #print "Domain not found"

    
    #############CreateVM(xmlString, address)###################
    #Generic method to create a vm with given parameters
    def createVM(xmlConfig, host):
        vm, hypervisor = defineVM(xmlConfig, host)
        if vm.create() < 0:
            #print "Failed to instantiate vm. exiting"
            exit(1)
        #print "Successfully created VM. Closing connection and sleeping 15 seconds."
        hypervisor.close()
        time.sleep(15)

    ############DefineVM(xmlString, address)###################
    #Generic method to define a vm, and return it
    #also opens a new connection to the host hypervisor and returns it

    def defineVM(self,xmlConfig):
        #check that disk image exists and create/copy it
        #check that there are ssh keys and handle that
        #give/check VM IP and return it
        if self.checkForVM(xmlConfig):
            vm = self.hypervisor.defineXML(xmlConfig)
            if vm == None:
                #print "Failed to define vm. exiting\n"
                exit(1)
            else:
                #print "Successfully created vm "+vm.name()
                pass
            self.domains.append(vm)

    
    def checkForVM(self,xmlConfig):
        allGood = False
        vms = self.hypervisor.listAllDomains(0)
        names = []
        for dom in vms:
            names.append(dom.name())
        vmName = Utilities.getName(xmlConfig)
        if vmName in names:
            #print vmName + " domain already exists!"
            if self.delAllDoms:
                #print "Deleting domain"
                self.deleteVM(vmName)
                allGood = True
            else:
                ans = str(raw_input("Delete it? [y/n/a]\n"))
                if 'a' in ans.lower():
                    self.delAllDoms = True
                    self.deleteVM(vmName)
                    allGood = True
                elif 'y' in ans.lower() or self.delAllDoms:
                    self.deleteVM(vmName)
                    allGood = True
                else:
                    allGood = False
        else:
            allGood = True
        return allGood


    def deleteVM(self,name):
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
                #print "Failed to destroy domain"
                pass
        
        if persistent:
            try:
                vm.undefine()
            except:
                #print "Failed to undefine domain"
                pass

        #Check to make sure that the vm is gone
        """ 
        vm = None
        try:
            vm = self.hypervisor.lookupByName(name)
        except Exception as inst:
            #print "Successfully deleted vm" """
    ##################OpenConnection(address)####################
    #opens a connection to the hypervisor on the given
    #host and returns it
    def openConnection(self):
        #print "connecting to "+str(self.host)
        try:
            hostHypervisor = libvirt.open(self.URI)
        except:
            #print "Failed to connect to "+str(self.host)+". Trying again"
            time.sleep(5)
            try:
                hostHypervisor = libvirt.open(self.URI)
            except:
                #print "Cannot connect to host. exiting"
                libvirt.open(self.URI)
                exit(1)
                
        if hostHypervisor == None:
            #print "Failed to connect to host: "+str(self.host)
            #print "Is libvirt installed?"
            exit(1)
        self.hypervisor = hostHypervisor

    
    def restartVM(self,vm):
        dom = self.hypervisor.lookupByName(vm)
        dom.destroy()
        time.sleep(15)
        dom.create()
    
    def close(self):
        #print 'Closing connection to remote host'
        self.hypervisor.close()


    def getAllDisks(self,path):
        files = Utilities.getXMLFiles(path)
        definitions = []
        disks = []
        for xml in files:
            definitions.append(Utilities.fileToString(xml))

        for definition in definitions:
            disks.append(defDict['disk'])
        return disks

    
    def defineAllDomains(self, path):
        files = Utilities.getXMLFiles(path)
        definitions = []
        for xml in files:
            definitions.append(xml.read())

        for definition in definitions:
            self.defineVM(definition)
       

    def createAllNetworks(self,path):
        files = Utilities.getXMLFiles(path)
        definitions = []
        for xml in files:
            definitions.append(Utilities.fileToString(xml))

        for definition in definitions:
            self.createNet(definition)

    
    def createNet(self,config):
        if self.checkNet(config):
            network = self.hypervisor.networkDefineXML(config)

            if network == None:
                #print "error defining network\n"
                pass
            network.create()
            if network.isActive() == 1:
                pass
                #print "Successfully defined network " + network.name() + '\n'
            self.networks.append(network)  
   
    def checkNet(self,config):
        allGood = False
        netName = Utilities.getName(config)
        if netName not in self.hypervisor.listNetworks():
            return True
        else: #net name is already used, but it must be unique
            #print netName + " network already exists!"
            if self.delAllNets:
                #print "Deleting network"
                self.deleteNet(network)
                allGood = True
            else:
                ans = str(raw_input("Delete it? [y/n/a]\n"))
                if 'a' in ans.lower():
                    self.delAllNets = True
                    self.deleteNet(network)
                    allGood = True
                elif 'y' in ans.lower():
                    self.deleteNet(network)
                    allGood = True
                else:
                    allGood = False
        return allGood

    
    def deleteNet(self,net):
        active = net.isActive()
        persistent = net.isPersistent()
        name = net.name()
        if active:
            try:
                net.destroy()
            except:
                #print "Failed to destroy network"
                pass

        if persistent:
            try:
                net.undefine()
            except:
                #print "Failed to undefine network"
                pass
        
    def deployFuel(self,path):
        #makes sure there isnt an old entry in known_hosts
        #cmd = "ssh root@"+self.host+""" 'sed -i -E "s/^.*10.20.0.2.*$//" /root/.ssh/known_hosts'"""
        #subprocess.call(cmd,shell=True)
        
        self.sshExec(["/bin/bash",self.remoteScripts+"/fuelInstall.sh",self.remoteScripts])

    #Running this method should do all of the work of this class
    #parsing the config file and defining all the networks and domains
    def go(self):
        nets = self.makeNetworks(self.net_conf)
        doms = self.makeDomains(self.dom_conf)
        return doms,nets

    def makeNetworks(self,conf):
        networks = []
        definitions = Network.parseConfigFile(conf)
        for definition in definitions:
            network = Network(definition)
            networks.append(network)
            self.createNet(network.toXML())
        return networks

    def makeDomains(self,conf):
        domains = []
        definitions = Domain.parseConfigFile(conf)
        for definition in definitions:
            domain = Domain(definition)
            domains.append(domain)
            self.defineVM(domain.toXML())
        return domains

    @staticmethod
    def getName(xmlString):
        xmlDoc = xml.dom.minidom.parseString(xmlString)
        nameNode = xmlDoc.documentElement.getElementsByTagName('name')
        name = str(nameNode[0].firstChild.nodeValue)
        return name
        
    #####################FileToString(file)####################
    #reads a file line by line and returns its string representation
    @staticmethod
    def fileToString(filePath):
        string = ''
        openFile = open( filePath, 'r')
        for line in openFile:
            string = string + line
        openFile.close()
        return string

    ####################getXMLFiles############################
    #searches the given directory non-recursively and 
    #returns a list of all xml files
    @staticmethod
    def getXMLFiles(directory):
        contents = os.listdir(directory)
        fileContents = []
        for item in contents:
            if os.path.isfile(os.path.join(directory, item)):
                fileContents.append(os.path.join(directory, item))
        xmlFiles = []
        for item in fileContents:
            if 'xml' in os.path.basename(item):
                xmlFiles.append(item)
        return xmlFiles

