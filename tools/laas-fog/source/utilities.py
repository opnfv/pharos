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

import os
import logging
import string
import sys
import subprocess
import xml.dom
import xml.dom.minidom
import re
import random
import yaml
from database import HostDataBase, BookingDataBase
from api.vpn import VPN
LOGGING_DIR = ""


class Utilities:
    """
    This class defines some useful functions that may be needed
    throughout the provisioning and deployment stage.
    The utility object is carried through most of the deployment process.
    """
    def __init__(self, host_ip, hostname, conf):
        """
        init function
        host_ip is the ip of the target host
        hostname is the FOG hostname of the host
        conf is the parsed config file
        """
        self.host = host_ip
        self.hostname = hostname
        root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.scripts = os.path.join(root_dir, "hostScripts/")
        self.remoteDir = "/root/hostScripts/"
        self.conf = conf
        self.logger = logging.getLogger(hostname)

    def execRemoteScript(self, script, args=[]):
        """
        executes the given script on the
        remote host with the given args.
        script must be found in laas/hostScripts
        """
        cmd = [self.remoteDir+script]
        for arg in args:
            cmd.append(arg)
        self.sshExec(cmd)

    def waitForBoot(self):
        """
        Continually pings the host, waiting for it to boot
        """
        i = 0
        while (not self.pingHost()) and i < 30:
            i += 1
        if i == 30:
            self.logger.error("Host %s has not booted", self.host)
            sys.exit(1)

    def checkHost(self):
        """
        returns true if the host responds to two pings.
        Sometimes, while a host is pxe booting, a host will
        respond to one ping but quickly go back offline.
        """
        if self.pingHost() and self.pingHost():
            return True
        return False

    def pingHost(self):
        """
        returns true if the host responds to a ping
        """
        i = 0
        response = 1
        cmd = "ping -c 1 "+self.host
        cmd = cmd.split(' ')
        nul = open(os.devnull, 'w')
        while i < 10 and response != 0:
            response = subprocess.call(cmd, stdout=nul, stderr=nul)
            i = i + 1
        if response == 0:
            return True
        return False

    def copyDir(self, localDir, remoteDir):
        """
        uses scp to copy localDir to remoteDir on the
        remote host
        """
        cmd = "mkdir -p "+remoteDir
        self.sshExec(cmd.split(" "))
        cmd = "scp -o StrictHostKeyChecking=no -r "
        cmd += localDir+" root@"+self.host+":/root"
        cmd = cmd.split()
        nul = open(os.devnull, 'w')
        subprocess.call(cmd, stdout=nul, stderr=nul)

    def copyScripts(self):
        """
        Copies the hostScrpts dir to the remote host.
        """
        self.copyDir(self.scripts, self.remoteDir)

    def sshExec(self, args):
        """
        executes args as an ssh
        command on the remote host.
        """
        cmd = ['ssh', 'root@'+self.host]
        for arg in args:
            cmd.append(arg)
        nul = open(os.devnull, 'w')
        return subprocess.call(cmd, stdout=nul, stderr=nul)

    def resetKnownHosts(self):
        """
        edits your known hosts file to remove the previous entry of host
        Sometimes, the flashing process gives the remote host a new
        signature, and ssh complains about it.
        """
        lines = []
        sshFile = open('/root/.ssh/known_hosts', 'r')
        lines = sshFile.read()
        sshFile.close()
        lines = lines.split('\n')
        sshFile = open('/root/.ssh/known_hosts', 'w')
        for line in lines:
            if self.host not in line:
                sshFile.write(line+'\n')
        sshFile.close()

    def restartHost(self):
        """
        restarts the remote host
        """
        cmd = ['shutdown', '-r', 'now']
        self.sshExec(cmd)

    @staticmethod
    def randoString(length):
        """
        this is an adapted version of the code found here:
        https://stackoverflow.com/questions/2257441/
        random-string-generation-with-upper-case-letters-and-digits-in-python
        generates a random alphanumeric string of length length.
        """
        randStr = ''
        chars = string.ascii_uppercase + string.digits
        for x in range(length):
            randStr += random.SystemRandom().choice(chars)
        return randStr

    def changePassword(self):
        """
        Sets the root password to a random string and returns it
        """
        paswd = self.randoString(15)
        command = "printf "+paswd+" | passwd --stdin root"
        self.sshExec(command.split(' '))
        return paswd

    def markHostDeployed(self):
        """
        Tells the database that this host has finished its deployment
        """
        db = HostDataBase(self.conf['database'])
        db.makeHostDeployed(self.hostname)
        db.close()

    def make_vpn_user(self):
        """
        Creates a vpn user and associates it with this booking
        """
        config = yaml.safe_load(open(self.conf['vpn_config']))
        myVpn = VPN(config)
        # name = dashboard.getUserName()
        u, p, uid = myVpn.makeNewUser()  # may pass name arg if wanted
        self.logger.info("%s", "created new vpn user")
        self.logger.info("username: %s", u)
        self.logger.info("password: %s", p)
        self.logger.info("vpn user uid: %s", uid)
        self.add_vpn_user(uid)

    def add_vpn_user(self, uid):
        """
        Adds the dn of the vpn user to the database
        so that we can clean it once the booking ends
        """
        db = BookingDataBase(self.conf['database'])
        # converts from hostname to pharos resource id
        inventory = yaml.safe_load(open(self.conf['inventory']))
        host_id = -1
        for resource_id in inventory.keys():
            if inventory[resource_id] == self.hostname:
                host_id = resource_id
                break
        db.setVPN(host_id, uid)

    def finishDeployment(self):
        """
        Last method call once a host is finished being deployed.
        It notifies the database and changes the password to
        a random string
        """
        self.markHostDeployed()
        self.make_vpn_user()
        passwd = self.changePassword()
        self.logger.info("host %s provisioning done", self.hostname)
        self.logger.info("You may access the host at %s", self.host)
        self.logger.info("The password is %s", passwd)
        notice = "You should change all passwords for security"
        self.logger.warning('%s', notice)

    @staticmethod
    def restartRemoteHost(host_ip):
        """
        This method assumes that you already have ssh access to the target
        """
        nul = open(os.devnull, 'w')
        ret_code = subprocess.call([
            'ssh', '-o', 'StrictHostKeyChecking=no',
            'root@'+host_ip,
            'shutdown', '-r', 'now'],
            stdout=nul, stderr=nul)

        return ret_code

    @staticmethod
    def getName(xmlString):
        """
        Gets the name value from xml. for example:
        <name>Parker</name> returns Parker
        """
        xmlDoc = xml.dom.minidom.parseString(xmlString)
        nameNode = xmlDoc.documentElement.getElementsByTagName('name')
        name = str(nameNode[0].firstChild.nodeValue)
        return name

    @staticmethod
    def getXMLFiles(directory):
        """
        searches directory non-recursively and
        returns a list of all xml files
        """
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
    def createLogger(name, log_dir=LOGGING_DIR):
        """
        Initializes the logger if it does not yet exist, and returns it.
        Because of how python logging works, calling logging.getLogger()
        with the same name always returns a reference to the same log file.
        So we can call this method from anywhere with the hostname as
        the name arguement and it will return the log file for that host.
        The formatting includes the level of importance and the time stamp
        """
        global LOGGING_DIR
        if log_dir != LOGGING_DIR:
            LOGGING_DIR = log_dir
        log = logging.getLogger(name)
        if len(log.handlers) > 0:  # if this logger is already initialized
            return log
        log.setLevel(10)
        han = logging.FileHandler(os.path.join(log_dir, name+".log"))
        han.setLevel(10)
        log_format = '[%(levelname)s] %(asctime)s [#] %(message)s'
        formatter = logging.Formatter(fmt=log_format)
        han.setFormatter(formatter)
        log.addHandler(han)
        return log

    @staticmethod
    def getIPfromMAC(macAddr, logFile, remote=None):
        """
        searches through the dhcp logs for the given mac
        and returns the associated ip. Will retrieve the
        logFile from a remote host if remote is given.
        if given, remote should be an ip address or hostname that
        we can ssh to.
        """
        if remote is not None:
            logFile = Utilities.retrieveFile(remote, logFile)
        ip = Utilities.getIPfromLog(macAddr, logFile)
        if remote is not None:
            os.remove(logFile)
        return ip

    @staticmethod
    def retrieveFile(host, remote_loc, local_loc=os.getcwd()):
        """
        Retrieves file from host and puts it in the current directory
        unless local_loc is given.
        """
        subprocess.call(['scp', 'root@'+host+':'+remote_loc, local_loc])
        return os.path.join(local_loc, os.path.basename(remote_loc))

    @staticmethod
    def getIPfromLog(macAddr, logFile):
        """
        Helper method for getIPfromMAC.
        uses regex to find the ip address in the
        log
        """
        try:
            messagesFile = open(logFile, "r")
            allLines = messagesFile.readlines()
        except Exception:
            sys.exit(1)
        importantLines = []
        for line in allLines:
            if macAddr in line and "DHCPACK" in line:
                importantLines.append(line)
        ipRegex = r'(\d+\.\d+\.\d+\.\d+)'
        IPs = []
        for line in importantLines:
            IPs.append(re.findall(ipRegex, line))
        if len(IPs) > 0 and len(IPs[-1]) > 0:
            return IPs[-1][0]
        return None
