import logging
from installers.fuel import Fuel_Installer
from api.libvirt_api import Libvirt
from utilities import Utilities
#from installers.X import X

"""
This class is passed the message from the pharos api to know what kind of
deployment is wanted, creates needed vm's and networks based on the installer config,
and then passes control to the right installer to do everything else.
"""

class Deployment_Manager:
    def __init__(self,installerType,scenario,utility):
        self.installer = installerType #installerType will either be the constructor for an installer or None
        self.virt = Libvirt(utility.host,net_conf=utility.conf['network_config_file'],
                dom_conf=utility.conf['vm_config_file'])
        self.host = utility.host
        self.util = utility


    def getIso(self):
        isoDom = None
        for dom in self.doms:
            if dom.iso['used']:
                isoDom = dom
                break
        if isoDom:
            path = isoDom.iso['location']
            url = isoDom.iso['URL']
            self.util.sshExec(['wget','-q','-O',path,url])

    def getDomMacs(self):
        for dom in self.doms:
            dom.macs = self.virt.getMacs(dom.name)

    def makeDisks(self):
        disks = []
        for dom in self.doms:
            disks.append(dom.disk)
        self.util.execRemoteScript("mkDisks.sh",disks)
    
    def go(self):
        log = logging.getLogger(self.util.hostname)
        log.info("%s","Connecting to the host hypervisor")
        self.virt.openConnection()
        domains,networks = self.virt.go()
        log.info("%s","Created all networks and VM's on host")
        self.doms = domains
        self.nets = networks
        if self.installer == None:
            log.warning("%s","No installer requested. Finishing deployment")
            self.util.finishDeployment()
            return
        log.info("%s","retrieving ISO")
        self.getIso()
        self.getDomMacs()
        self.util.copyScripts()
        self.makeDisks()
        log.info("%s","Beginning installation of OPNFV")
        try:
            installer = self.installer(self.doms,self.nets,self.virt,self.util)
            installer.go()
        except Exception:
            log.exception('%s',"failed to install OPNFV")
