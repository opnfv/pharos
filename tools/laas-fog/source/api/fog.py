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
import sys
import time


class FOG_Handler:
    """
    This class talks with the REST web api for the FOG server.

    TODO: convert prints to logs and remove uneeded pass's
    """

    def __init__(self, baseURL, fogKey=None, userKey=None):
        """
        init function
        baseURL should be http://fog.ip.or.hostname/fog/
        fogKey and userKey can optionally be supplied here or later
        They can be found in fog and provide authentication.
        """
        self.baseURL = baseURL
        self.fogKey = fogKey
        self.userKey = userKey
        self.header = {}
        self.updateHeader()

    def setLogger(self, logger):
        """
        saves the refference to the log object as
        self.log
        """
        self.log = logger

    def getUserKeyFromFile(self, path):
        """
        reads the user api key from a file
        """
        self.userKey = open(path).read()
        self.updateHeader()

    def getFogKeyFromFile(self, path):
        """
        reads the api key from a file
        """
        self.fogKey = open(path).read()
        self.updateHeader()

    def setUserKey(self, key):
        """
        sets the user key
        """
        self.userKey = key
        self.updateHeader()

    def setFogKey(self, key):
        """
        sets the fog key
        """
        self.fogKey = key
        self.updateHeader()

    def updateHeader(self):
        """
        recreates the http header used to talk to the fog api
        """
        self.header = {}
        self.header['fog-api-token'] = self.fogKey
        self.header['fog-user-token'] = self.userKey

    def setImage(self, host, imgNum):
        """
        Sets the image to be used during ghosting to the image
        with id imgNum. host can either be a hostname or number.
        """
        try:
            host = int(host)
        except:
            host = self.getHostNumber(host)
        url = self.baseURL+"host/"+str(host)
        host_conf = requests.get(url, headers=self.header).json()
        host_conf['imageID'] = str(imgNum)
        requests.put(url+"/edit", headers=self.header, json=host_conf)

    def delTask(self, hostNum):
        """
        Tries to delete an existing task for the host
        with hostNum as a host number
        """
        try:
            url = self.baseURL+'fog/host/'+str(hostNum)+'/cancel'
            req = requests.delete(url, headers=self.header)
            if req.status_code == 200:
                self.log.info("%s", "successfully deleted image task")
        except Exception:
            self.log.exception("Failed to delete the imaging task!")

    def getHostMac(self, hostname):
        """
        returns the primary mac address if the given host.
        """
        try:
            hostNum = int(self.getHostNumber(hostname))
            url = self.baseURL + "host/"+str(hostNum)
            req = requests.get(url, headers=self.header)
            macAddr = req.json()['primac']
            return macAddr
        except Exception:
            self.log.exception('%s', "Failed to connect to the FOG server")

    def getHostNumber(self, hostname):
        """
        returns the host number of given host
        """
        try:
            req = requests.get(self.baseURL+"host", headers=self.header)
            hostData = req.json()
            if hostData is not None:
                for hostDict in hostData['hosts']:
                    if hostname == hostDict['name']:
                        return hostDict['id']
            return -1
        except Exception:
            self.log.exception('%s', "Failed to connect to the FOG server")

    def imageHost(self, hostName, recurse=False):
        """
        Schedules an imaging task for the given host.
        This automatically uses the "associated" disk image.
        To support extra installers, I will need to create
        a way to change what that image is before calling
        this method.
        """
        num = str(self.getHostNumber(hostName))
        url = self.baseURL+'host/'+num+'/task'

        try:
            req = requests.post(
                    url,
                    headers=self.header,
                    json={"taskTypeID": 1}
                    )
            if req.status_code == 200:
                self.log.info("%s", "Scheduled image task for host")
        except Exception:
            if recurse:  # prevents infinite loop
                self.log.exception("%s", "Failed to schedule task. Exiting")
                sys.exit(1)
            self.log.warning("%s", "Failed to schedule host imaging")
            self.log.warning("%s", "Trying to delete existing image task")
            self.delTask(num)
            self.imageHost(num, recurse=True)

    def waitForHost(self, host):
        """
        tracks the imaging task to completion.
        """
        while True:
            imageTask = self.getImagingTask(host)
            if imageTask is None:
                self.log.info("%s", "Imaging complete")
                return
            state = int(imageTask['stateID'])
            if state == 1:
                self.log.info("%s", "Waiting for host to check in")
                self.waitForTaskToActive(host)
                continue
            if state == 3:
                self.waitForTaskToStart(host)
                self.waitForImaging(host)
                continue
            time.sleep(8)

    def waitForImaging(self, host):
        """
        Once the host begins being imaged, this tracks progress.
        """
        # print "Host has begun the imaging process\n"
        while True:
            task = self.getImagingTask(host)
            if task is None:
                return
            per = str(task['percent'])
            self.log.info("%s percent done imaging", per)
            time.sleep(15)

    def waitForTaskToActive(self, host):
        """
        Waits for the host to reboot and pxe boot
        into FOG
        """
        while True:
            try:
                task = self.getImagingTask(host)
            except:
                pass
            state = int(task['stateID'])
            if state == 1:
                time.sleep(4)
            else:
                return

    def waitForTaskToStart(self, host):
        """
        waits for the task to start and imaging to begin.
        """
        while True:
            try:
                per = str(self.getImagingTask(host)['percent'])
            except:
                pass
            if per.strip() == '':
                time.sleep(1)
            else:
                return

    def getImagingTask(self, host):
        """
        Sorts through all current tasks to find the image task
        associated with the  given host.
        """
        try:
            taskList = requests.get(
                    self.baseURL+'task/current',
                    headers=self.header)
            taskList = taskList.json()['tasks']
            imageTask = None
            for task in taskList:
                hostname = str(task['host']['name'])
                if hostname == host and int(task['typeID']) == 1:
                    imageTask = task
            return imageTask
        except Exception:
            self.log.exception("%s", "Failed to talk to FOG server")
            sys.exit(1)

    def getHosts(self):
        """
        returns a list of all hosts
        """
        req = requests.get(self.baseURL+"host", headers=self.header)
        return req.json()['hosts']

    def getHostsinGroup(self, groupName):
        """
        returns a list of all hosts in groupName
        """
        groupID = None
        groups = requests.get(self.baseURL+"group", headers=self.header)
        groups = groups.json()['groups']
        for group in groups:
            if groupName.lower() in group['name'].lower():
                groupID = group['id']
        if groupID is None:
            return
        hostIDs = []
        associations = requests.get(
                self.baseURL+"groupassociation",
                headers=self.header
                )
        associations = associations.json()['groupassociations']
        for association in associations:
            if association['groupID'] == groupID:
                hostIDs.append(association['hostID'])

        hosts = []
        for hostID in hostIDs:
            hosts.append(requests.get(
                self.baseURL+"host/"+str(hostID),
                headers=self.header
                ).json())
        return hosts
