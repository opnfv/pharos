#!/usr/bin/python
import time
import sys
import os
import json
import re
import logging
from api.fog import FOG_Handler
from utilities import Utilities
from deployment_manager import Deployment_Manager
from database import HostDataBase
from api.libvirt_api import Libvirt
from installers import *
#form installers import all the installers

"""
This is the 'main' class that chooses a host and provisions + deploys it.
this class can be run directly from the command line, or it can be called from the 
pharos dashboard listener when a deployment is requested.
Either way, this file should be called with:
    ./pod_manager.py --config <CONFIG_FILE>
"""


class Pod_Manager:
    #Thi dictionary allows me to map the supported installers to the 
    #respective installer classes, foor easier parsing of the config file
    INSTALLERS = {"fuel": fuel.Fuel_Installer,"None":None} 
    
    def __init__(self,conf,requested_host=None,reset=False):
        self.conf = conf
        if self.conf['installer'] != None:
            self.conf['installer'] = Pod_Manager.INSTALLERS[self.conf['installer'].lower()]
        self.fog = FOG_Handler(self.conf['fog_server'])
        self.fog.setFogKey(self.conf['fog_api_key'])
        self.fog.setUserKey(self.conf['fog_user_key'])
        self.database = HostDataBase(self.conf['database'])
        self.request = requested_host
        if reset:
            ip = Utilities.getIPfromMAC(self.fog.getHostMac(self.request),
                    self.conf['dhcp_log'],remote=self.conf['dhcp_server'])
            self.flash_host(self.request,ip)


    def start_deploy(self):    
        host = self.database.getHost(self.request)
        hostMac = self.fog.getHostMac(host)
        dhcp_log = self.conf['dhcp_log']
        dhcp_server = self.conf['dhcp_server']
        host_ip = Utilities.getIPfromMAC(hostMac,dhcp_log,remote=dhcp_server)
        util = Utilities(host_ip,host,self.conf)
        util.resetKnownHosts()
        log = Utilities.createLogger(host,self.conf['logging_dir'])
        #log.info("Using host %s at %s",(host,host_ip))
        log.info("Starting booking on host %s",host)
        log.info("host is reachable at %s",host_ip)
        log.info('ghosting host %s with clean image',host)
        self.flash_host(host,host_ip,util)
        log.info('Host %s imaging complete',host)
        Deployment_Manager(self.conf['installer'],self.conf['scenario'],util).go()


    #We do this using a FOG server, but you can use whatever fits into your
    #lab infrastructure. This method should put the host into a state as if it 
    #centos was just freshly installed, updated, and needed virtualization software
    #installed. This is the 'clean' starting point we work from
    def flash_host(self,host,host_ip,util=None):
        self.fog.imageHost(host)
        Utilities.restartHost(host_ip)
        #self.restartHostFromNode(host)
        self.fog.waitForHost(host)
        #if util is not given, then we are just flashing to reset after a booking expires
        if util != None:
            time.sleep(30)
            util.waitForBoot()
            util.checkHost()
            time.sleep(15)
            util.checkHost()
            #util.copySSHKeys()
        
    
if __name__ == "__main__":
    configFile = ""
    host = ""
    for i in range(len(sys.argv) -1):
        if "--config" in sys.argv[i]:
            configFile = sys.argv[i+1]
        elif "--host" in sys.argv[i]:
            host = sys.argv[i+1]
    if len(configFile) < 1:
        print "No config file specified"
        sys.exit(1)
    configFile = json.loads(open(configFile).read())
    manager = Pod_Manager(configFile,requested_host=host)
    manager.start_deploy()
