import os
import logging
import string
import sys
import time
import subprocess
import xml.dom
import xml.dom.minidom
import re
import random
import logging
from database import HostDataBase
"""
This class defines some useful functions that may be needed throughout the provisioning and deployment stage.
The utility object is carried through most of the deployment process.
"""
LOGGING_DIR = ""

class Utilities:
    def __init__(self,host_ip,hostname,conf):
        self.host = host_ip
        self.hostname = hostname
        self.scripts = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"hostScripts/")
        self.remoteDir = conf['remote_scripts']
        self.conf = conf
        self.logger = logging.getLogger(hostname)

    def execRemoteScript(self,script,args=[]):
        cmd = [self.remoteDir+script]
        for arg in args:
            cmd.append(arg)
        self.sshExec(cmd)

    def waitForBoot(self):
        i = 0
        while (not self.pingHost()) and i < 30:
            i += 1
        if i == 30:
            self.logger.error("Host %s has not booted",self.host)
            sys.exit(1)
    
    #returns true if the host responds to two pings
    def checkHost(self):
        if self.pingHost() and self.pingHost():
            return True
        return False

    #returns true if the host responds to pings
    def pingHost(self):
        i = 0
        response = 1
        while i < 10 and response != 0:
            response = subprocess.call("ping -c 1 "+self.host+" >/dev/null 2>&1",shell=True)
            i = i + 1
        if response == 0:
            return True
        return False
    
    def copyDir(self,localDir,remoteDir):
        cmd = "mkdir -p "+remoteDir
        self.sshExec(cmd.split(" "))
        cmd = "scp -o StrictHostKeyChecking=no -r "+localDir+"* root@"+self.host+":"+remoteDir
        subprocess.call(cmd,shell=True)
    
    def copyScripts(self):
        self.copyDir(self.scripts,self.remoteDir)
    
    def sshExec(self,args):
        cmd = ['ssh','root@'+self.host]
        for arg in args:
            cmd.append(arg)
        nul = open(os.devnull,'w')    
        return subprocess.call(cmd,stdout=nul,stderr=nul)
    

    def resetKnownHosts(self):
        lines = []
        sshFile = open('/root/.ssh/known_hosts','r')
        lines = sshFile.read()
        sshFile.close()
        lines = lines.split('\n')
        sshFile = open('/root/.ssh/known_hosts','w')
        for line in lines:
            if self.host not in line:
                sshFile.write(line+'\n')
        sshFile.close()

    def restartHost(self):
        cmd = ['shutdown','-r','now']
        self.sshExec(cmd)

    def changePassword(self):
    #Note: this is an adapted version of the code found here:
    #https://stackoverflow.com/questions/2257441/
    #random-string-generation-with-upper-case-letters-and-digits-in-python
        paswd = ''.join(random.SystemRandom().choice(string.ascii_uppercase+string.digits) for x in range(15))
        command = "printf "+paswd+" | passwd --stdin root"
        self.sshExec(command.split(' '))
        return paswd
    
    def markHostDeployed(self):
        db = HostDataBase(self.conf['database'])
        db.makeHostDeployed(self.hostname)
        db.close()

    def finishDeployment(self):
        self.markHostDeployed()
        passwd = self.changePassword()
        self.logger.info("host %s provisioning done",self.hostname)
        self.logger.info("You may access the host at %s",self.host)
        self.logger.info("The password is %s", passwd)
        self.logger.warning('%s', "You should change all passwords for security")
        #sys.exit(0)
    
    
    
    @staticmethod
    def restartHost(host_ip):
        #This method assumes that you already have ssh access to the target
        nul = open(os.devnull,'w')
        ret_code = subprocess.call(['ssh','-o','StrictHostKeyChecking=no','root@'+host_ip, 'shutdown','-r','now'],stdout=nul,stderr=nul)
        return ret_code
    
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


    @staticmethod
    def createLogger(name,log_dir=LOGGING_DIR):
        global LOGGING_DIR
        if log_dir != LOGGING_DIR:
            LOGGING_DIR = log_dir
        log = logging.getLogger(name)
        if len(log.handlers) > 0: #if this logger has already been initialized
            return log
        log.setLevel(10)
        han = logging.FileHandler(os.path.join(log_dir,name+".log"))
        han.setLevel(10)
        log_format = '[%(levelname)s] %(asctime)s [#] %(message)s'
        formatter = logging.Formatter(fmt=log_format)
        han.setFormatter(formatter)
        log.addHandler(han)
        return log



    @staticmethod
    def getIPfromMAC(macAddr,logFile,remote=None):
        if remote != None:
            logFile = Utilities.retrieveFile(remote,logFile)
        ip = Utilities.getIPfromLog(macAddr,logFile)
        if remote != None:
            os.remove(logFile)
        return ip

    @staticmethod
    def retrieveFile(host,remote_loc,local_loc=os.getcwd()):
        subprocess.call(['scp','root@'+host+':'+remote_loc,local_loc])
        return os.path.join(local_loc,os.path.basename(remote_loc))
    
    @staticmethod
    def getIPfromLog(macAddr,logFile):    
        try:
            messagesFile = open(logFile,"r")
            allLines = messagesFile.readlines()
        except Exception:
            #print "Failed to read log for dnsmasq. exiting"
            sys.exit(1)
        importantLines = []
        for line in allLines:
            if macAddr in line and "DHCPACK" in line:
                importantLines.append(line)
        ipRegex = r'(\d+\.\d+\.\d+\.\d+)'
        IPs = []
        for line in importantLines:
            IPs.append(re.findall(ipRegex,line))
        if len(IPs) > 0 and len(IPs[-1]) > 0:
            return IPs[-1][0]
        return None

