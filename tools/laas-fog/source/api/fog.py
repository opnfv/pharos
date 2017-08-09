import requests
import json
import sys
import time

from network import Network
from utilities import Utilities
"""
This class talks with the REST web api for the FOG server.

TODO: convert prints to logs and remove uneeded pass's
"""
class FOG_Handler:

    def __init__(self,baseURL,fogKey=None,userKey=None,interact=False):
        self.baseURL = baseURL
        self.fogKey = fogKey
        self.userKey = userKey
        self.header = {}
        self.updateHeader()
        self.interact = interact

    def getUserKeyFromFile(self,path):
        self.userKey = open(path).read()
        self.updateHeader()

    def getFogKeyFromFile(self,path):
        self.fogKey = open(path).read()
        self.updateHeader()
    
    def setUserKey(self,key):
        self.userKey = key
        self.updateHeader()

    def setFogKey(self,key):
        self.fogKey = key
        self.updateHeader()
    
    def updateHeader(self):
        self.header = {}
        self.header['fog-api-token'] = self.fogKey
        self.header['fog-user-token'] = self.userKey
    
    def delTask(self,hostNum):
        try:
            url = self.baseURL+'fog/host/'+str(hostNum)+'/cancel'
            req = requests.delete(url,headers=self.header)
            if req.status_code == 200:
                pass
                #print "successfully cancelled task"
        except Exception:
            pass
            #print "Failed to connect to the FOG server!"
            #print req.status_code
            #print req.url


    def getHostMac(self,hostname):
        try:
            hostNum = int(self.getHostNumber(hostname))
            url = self.baseURL + "host/"+str(hostNum)
            req = requests.get(url,headers = self.header)
            macAddr = req.json()['primac']
            return macAddr
        except Exception:
            pass
            #print "Failed to connect to the FOG server!"
            #print req.status_code
            #print req.url
    
    def getHostNumber(self,hostname):
        try:
            req = requests.get(self.baseURL+"host",headers=self.header)
            hostData = req.json()
            if hostData is not None:
                for hostDict in hostData['hosts']:
                    if hostname == hostDict['name']:
                        return hostDict['id']
            return -1
        except Exception:
            pass
            #print "Failed to connect to the FOG server!"
            #print req.status_code
            #print req.url
    
    def imageHost(self,hostName):
        num = str(self.getHostNumber(hostName))
        url = self.baseURL+'host/'+num+'/task'

        try:
            req = requests.post(url,headers=self.header,json={"taskTypeID":1})
            if req.status_code == 200:
                pass
                #print "Successfully scheduled imaging for host"

        except Exception:
            #print "Failed to send image task to FOG server."
            if self.interact:
                #print "There may already be an existing task for the host. Attempt to delete it?"
                ans = raw_input("(y/n)  ")
                if 'y' in ans:
                    self.delTask(num)
                    self.imageHost(num)
                else:
                    #print "Cannot continue. exiting"
                    sys.exit(1)

            else:
                #print "Trying to delete task"
                self.deTask(num)
                self.imageHost(num)

    def waitForHost(self,host):
        while True:
            imageTask = self.getImagingTask(host)
            if imageTask is None:
                #print "\nNo more imaging tasks found for host. Assumed imaging complete."
                return
            state = int(imageTask['stateID'])
            if state == 1:
                #print "Image task is waiting to start. Host has not checked in yet"
                self.waitForTaskToActive(host)
                continue
            if state == 3:
                self.waitForTaskToStart(host)
                #print "\n"
                self.waitForImaging(host)
                continue
                #per = str(imageTask['percent'])
                #timeR = str(imageTask['timeRemaining'])
                #if per.trim() == '':
                #    #print "Task is starting"
                #else:
                #    #print per+"% done. Aproximately "+timeR+" remaining"
            time.sleep(5)


    
    def waitForImaging(self,host):
        #print "Host has begun the imaging process\n"
        while True:
            task = self.getImagingTask(host)
            if task is None:
                return
            per = str(task['percent'])
            timeR = str(task['timeRemaining'])
            written = str(task['dataCopied'])
            total = str(task['dataTotal'])
            line = per+"% done. Aproximately "+timeR+" remaining. Written "+written+" out of "+total
            #print line
            #This overwrites the current line, so that we don't flood stdout
            #sys.stdout.write("\r")
            #sys.stdout.flush()
            #sys.stdout.write(line)
            #sys.stdout.flush()
            time.sleep(3)

    
    def waitForTaskToActive(self,host):
        while True:
            try:
                task = self.getImagingTask(host)
            except:
                pass
            state = int(task['stateID'])
            if state == 1:
                #print "..."
                time.sleep(4)
            else:
                return


    def waitForTaskToStart(self,host):
        while True:
            try:
                per = str(self.getImagingTask(host)['percent'])
            except:
                pass
            if per.strip() == '':
                #print "..."
                time.sleep(1)
            else:
                return


    def getImagingTask(self,host):                                                                     
        try:
            taskList = requests.get(self.baseURL+'task/current',headers=self.header).json()['tasks']
            imageTask = None                                                  
            for task in taskList:
                if str(task['host']['name']) == host and int(task['typeID']) == 1:
                    imageTask = task
            return imageTask
        except Exception:
            #print "Failed to connect to the Fog Server!"
            sys.exit(1)


    def getHosts(self):
        req = requests.get(self.baseURL+"host",headers=self.header) 
        return req.json()['hosts']

    def getHostsinGroup(self,groupName):
        groupID = None
        for group in requests.get(self.baseURL+"group",headers=self.header).json()['groups']:
            if groupName.lower() in group['name'].lower():
                groupID = group['id']
        if groupID == None:
            return
        hostIDs = []
        for association in requests.get(self.baseURL+"groupassociation",headers=self.header).json()['groupassociations']:
            if association['groupID'] == groupID:
                hostIDs.append(association['hostID'])

        hosts = []
        for hostID in hostIDs:
            hosts.append(requests.get(self.baseURL+"host/"+str(hostID),headers=self.header).json())
        return hosts
