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

import requests
import time
import sys


class Fuel_api:

    def __init__(self, url, logger, user="admin", password="admin"):
        """
        url is the url of the fog api in the form
        http://ip.or.host.name:8000/
        logger is a reference to the logger
        the default creds for fuel is admin/admin
        """
        self.logger = logger
        self.base = url
        self.user = user
        self.password = password
        self.header = {"Content-Type": "application/json"}

    def getKey(self):
        """
        authenticates with the user and password
        to get a keystone key, used in the headers
        from here on to talk to fuel.
        """
        url = self.base + 'keystone/v2.0/tokens/'
        reqData = {"auth": {
            "tenantName": self.user,
            "passwordCredentials": {
                "username": self.user,
                "password": self.password
                }
            }}
        self.logger.info("Retreiving keystone token from %s", url)
        token = requests.post(url, headers=self.header, json=reqData)
        self.logger.info("Received response code %d", token.status_code)
        self.token = token.json()['access']['token']['id']
        self.header['X-Auth-Token'] = self.token

    def getNotifications(self):
        """
        returns the fuel notifications
        """
        url = self.base+'/api/notifications'
        try:
            req = requests.get(url, headers=self.header)
            return req.json()

        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def waitForBootstrap(self):
        """
        Waits for the bootstrap image to build.
        """
        while True:
            time.sleep(30)
            notes = self.getNotifications()
            for note in notes:
                if "bootstrap image building done" in note['message']:
                    return

    def getNodes(self):
        """
        returns a list of all nodes booted into fuel
        """
        url = self.base+'api/nodes'
        try:
            req = requests.get(url, headers=self.header)
            return req.json()
        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def getID(self, mac):
        """
        gets the fuel id of node with given mac
        """
        for node in self.getNodes():
            if node['mac'] == mac:
                return node['id']

    def getNetID(self, name, osid):
        """
        gets the id of the network with name
        """
        url = self.base+'api/clusters/'
        url += str(osid)+'/network_configuration/neutron'
        try:
            req = requests.get(url, headers=self.header)
            nets = req.json()['networks']
            for net in nets:
                if net['name'] == name:
                    return net['id']
            return -1

        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def createOpenstack(self):
        """
        defines a new openstack environment in fuel.
        """
        url = self.base+'api/clusters'
        data = {
                "nodes": [],
                "tasks": [],
                "name": "OpenStack",
                "release_id": 2,
                "net_segment_type": "vlan"
                }
        try:
            req = requests.post(url, json=data, headers=self.header)
            return req.json()['id']
        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def simpleNetDict(self, osID):
        """
        returns a simple dict of network names and id numbers
        """
        nets = self.getNetworks(osID)
        netDict = {}
        targetNets = ['admin', 'public', 'storage', 'management']
        for net in nets['networks']:
            for tarNet in targetNets:
                if tarNet in net['name']:
                    netDict[tarNet] = net['id']
        return netDict

    def getNetworks(self, osID):
        """
        Returns the pythonizezd json of the openstack networks
        """
        url = self.base + 'api/clusters/'
        url += str(osID)+'/network_configuration/neutron/'
        try:
            req = requests.get(url, headers=self.header)
            return req.json()
        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def uploadNetworks(self, netJson, osID):
        """
        configures the networks of the openstack
        environment with id osID based on netJson
        """
        url = self.base+'api/clusters/'
        url += str(osID)+'/network_configuration/neutron'
        try:
            req = requests.put(url, headers=self.header, json=netJson)
            return req.json()
        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def addNodes(self, clusterID, nodes):
        """
        Adds the nodes into this openstack environment.
        nodes is valid  json
        """
        url = self.base + 'api/clusters/'+str(clusterID)+'/assignment'
        try:
            req = requests.post(url, headers=self.header, json=nodes)
            return req.json()

        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def getIfaces(self, nodeID):
        """
        returns the pythonized json describing the
        interfaces of given node
        """
        url = self.base + 'api/nodes/'+str(nodeID)+'/interfaces'
        try:
            req = requests.get(url, headers=self.header)
            return req.json()

        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def setIfaces(self, nodeID, ifaceJson):
        """
        configures the interfaces of node with id nodeID
        with ifaceJson
        ifaceJson is valid json that fits fuel's schema for ifaces
        """
        url = self.base+'/api/nodes/'+str(nodeID)+'/interfaces'
        try:
            req = requests.put(url, headers=self.header, json=ifaceJson)
            return req.json()

        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def getTasks(self):
        """
        returns a list of all tasks
        """
        url = self.base+"/api/tasks/"
        try:
            req = requests.get(url, headers=self.header)
            return req.json()
        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def waitForTask(self, uuid):
        """
        Tracks the progress of task with uuid and
        returns once the task finishes
        """
        progress = 0
        while progress < 100:
            for task in self.getTasks():
                if task['uuid'] == uuid:
                    progress = task['progress']
            self.logger.info("Task is %s percent done", str(progress))
            time.sleep(20)
        # Task may hang a minute at 100% without finishing
        while True:
            for task in self.getTasks():
                if task['uuid'] == uuid and not task['status'] == "ready":
                    time.sleep(10)
                elif task['uuid'] == uuid and task['status'] == "ready":
                    return

    def getHorizonIP(self, osid):
        """
        returns the ip address of the horizon dashboard.
        Horizon always takes the first ip after the public router's
        """
        url = self.base+'api/clusters/'
        url += str(osid)+'/network_configuration/neutron/'
        try:
            req = requests.get(url, headers=self.header)
            routerIP = req.json()['vips']['vrouter_pub']['ipaddr'].split('.')
            routerIP[-1] = str(int(routerIP[-1])+1)
            return '.'.join(routerIP)
        except Exception:
            self.logger.exception('%s', "Failed to talk to the Fuel api!")
            sys.exit(1)

    def deployOpenstack(self, clusterID):
        """
        Once openstack and the nodes are configured,
        this method actually deploys openstack.
        It takes a while.
        """
        # First, we need to provision the cluster
        url = self.base+'/api/clusters/'+str(clusterID)+'/provision'
        req = requests.put(url, headers=self.header)
        if req.status_code < 300:
            self.logger.info('%s', "Sent provisioning task")
        else:
            err = "failed to provision Openstack Environment"
            self.logger.error('%s', err)
            sys.exit(1)

        taskUID = ''
        tasks = self.getTasks()
        for task in tasks:
            if task['name'] == "provision" and task['cluster'] == clusterID:
                taskUID = task['uuid']

        self.waitForTask(taskUID)

        # Then, we deploy cluster
        url = self.base + '/api/clusters/'+str(clusterID)+'/deploy'
        req = requests.put(url, headers=self.header)
        if req.status_code < 300:
            self.logger.info('%s', "Sent deployment task")
        taskUID = ''
        tasks = self.getTasks()
        for task in tasks:
            if 'deploy' in task['name'] and task['cluster'] == clusterID:
                taskUID = task['uuid']
        if len(taskUID) > 0:
            self.waitForTask(taskUID)
