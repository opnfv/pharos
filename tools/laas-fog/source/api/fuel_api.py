import requests
import json
import time
import sys
import logging

class Fuel_api:

    def __init__(self,url,logger,user="admin",password="admin"):
        self.logger = logger
        self.base = url
        self.user = user
        self.password = password
        self.header = {"Content-Type": "application/json"}

    def getKey(self):
        url = self.base + 'keystone/v2.0/tokens/'
        reqData = {"auth": {"tenantName": self.user, "passwordCredentials": 
            {"username": self.user, "password": self.password}}}
        try:
            token = requests.post(url, headers=self.header,json=reqData).json()
            self.token = token['access']['token']['id']
            self.header['X-Auth-Token'] = self.token
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)

    def getNotifications(self):
        url = self.base+'/api/notifications'
        try:
            req = requests.get(url,headers=self.header)
            return req.json()

        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)
        
    
    def waitForBootstrap(self):
        while True:
            time.sleep(30)
            notes = self.getNotifications()
            for note in notes:
                if "bootstrap image building done" in note['message']:
                    return

    
    def getNodes(self):
        url = self.base+'api/nodes'
        try:
            req = requests.get(url,headers=self.header)
            return req.json()
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)
    
    def getID(self,mac):
        for node in self.getNodes():
            if node['mac'] == mac:
                return node['id']


    def getNetID(self,name,osid):
        url = self.base+'api/clusters/'+str(osid)+'/network_configuration/neutron'
        try:
            req = requests.get(url,headers=self.header)
            nets = req.json()['networks']
            for net in nets:
                if net['name'] == name:
                    return net['id']
            return -1
        
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)
     

    def createOpenstack(self):
        url = self.base+'api/clusters'
        data = {"nodes": [], "tasks": [], "name": "OpenStack", "release_id": 2, "net_segment_type": "vlan"}
        try:
            req = requests.post(url,json=data,headers=self.header)
            return req.json()['id']
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)

    
    def simpleNetDict(self,osID):
        nets = self.getNetworks(osID)
        netDict = {}
        targetNets = ['admin','public','storage','management']
        for net in nets['networks']:
            for tarNet in targetNets:
                if tarNet in net['name']:
                    netDict[tarNet] = net['id']
        return netDict
    
    def getNetworks(self,osID):
        url = self.base + 'api/clusters/'+str(osID)+'/network_configuration/neutron/'
        try:
            req = requests.get(url,headers=self.header)
            return req.json()
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)


    def uploadNetworks(self,netJson,osID):
        url = self.base+'api/clusters/'+str(osID)+'/network_configuration/neutron'
        try:
            req = requests.put(url,headers=self.header,json=netJson)
            return req.json()
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)
            

    def addNodes(self,clusterID,nodes):
        url = self.base + 'api/clusters/'+str(clusterID)+'/assignment'
        try:
            req = requests.post(url,headers=self.header,json=nodes)
            return req.json()
        
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)
    
    
    def getIfaces(self,nodeID):
        url = self.base + 'api/nodes/'+str(nodeID)+'/interfaces'
        try:
            req = requests.get(url,headers=self.header)
            return req.json()

        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)


    def setIfaces(self,nodeID,ifaceJson):
        url = self.base+'/api/nodes/'+str(nodeID)+'/interfaces'
        try:
            req = requests.put(url,headers=self.header,json=ifaceJson)
            return req.json()
        
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)
    

    def getTasks(self):
        url = self.base+"/api/tasks/"
        try:
            req = requests.get(url,headers=self.header)
            return req.json()
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)
    

    def waitForTask(self,uuid):
        progress = 0
        while progress < 100:
            for task in self.getTasks():
                if task['uuid'] == uuid:
                    progress = task['progress']
            line = "Task "+str(progress)+"% complete."
            time.sleep(20)
        #It is possible for the task to hang at 100% for a moment but not be done
        while True:
            for task in self.getTasks():
                if task['uuid'] == uuid and not task['status'] == "ready":
                    time.sleep(10)
                elif task['uuid'] == uuid and task['status'] == "ready":
                    return

    #horizon dashboard takes the first ip address after the router's
    def getHorizonIP(self,osid):
        url = self.base+'api/clusters/'+str(osid)+'/network_configuration/neutron/'
        try:
            req = requests.get(url,headers=self.header)
            routerIP = req.json()['vips']['vrouter_pub']['ipaddr'].split('.')
            routerIP[-1] = str(int(routerIP[-1])+1)
            return '.'.join(routerIP)
        except Exception:
            self.logger.exception('%s',"Failed to talk to the Fuel api!")
            sys.exit(1)
   

    def deployOpenstack(self,clusterID):
        #First, we need to provision the cluster
        url = self.base+'/api/clusters/'+str(clusterID)+'/provision'
        req = requests.put(url,headers=self.header)
        if req.status_code < 300:
            self.logger.info('%s',"Sent provisioning task")
        else:
            self.logger.error('%s',"failed to provision Openstack environment")
            sys.exit(1)
        
        taskUID = ''
        tasks = self.getTasks()
        for task in tasks:
            if task['name'] == "provision" and task['cluster'] == clusterID:
                taskUID = task['uuid']

        self.waitForTask(taskUID)

        #Then, we deploy cluster
        url = self.base + '/api/clusters/'+str(clusterID)+'/deploy'
        req = requests.put(url,headers=self.header)
        if req.status_code < 300:
            self.logger.info('%s',"Sent deployment task")
        taskUID=''
        tasks = self.getTasks()
        for task in tasks:
            if 'deploy' in task['name'] and task['cluster'] == clusterID:
                taskUID = task['uuid']
        if len(taskUID) > 0:
            self.waitForTask(taskUID)

