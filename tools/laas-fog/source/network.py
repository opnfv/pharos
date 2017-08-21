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

import sys
import xml.dom
import xml.dom.minidom
import yaml


class Network:
    """
    This class has a similar role as the Domain class.
    This class will parse a config file and
    write the xml definitions of those networks for libvirt.
    """

    def __init__(self, propertiesDict):
        """
        init. propertiesDict should be
        one of the dictionaries returned by parseConfigFile
        """
        self.name = propertiesDict['name']
        self.brName = propertiesDict['brName']
        self.brAddr = propertiesDict['brAddr']
        self.netmask = propertiesDict['netmask']
        self.forward = propertiesDict['forward']
        self.dhcp = propertiesDict['dhcp']
        self.cidr = propertiesDict['cidr']

    def toXML(self):
        """
        Takes the config of this network and writes a valid xml definition
        for libvirt.
        returns a string
        """
        definition = xml.dom.minidom.parseString("<network>\n</network>")
        nameElem = definition.createElement('name')
        nameElem.appendChild(definition.createTextNode(self.name))
        definition.documentElement.appendChild(nameElem)

        if self.forward['used']:
            forwardElem = definition.createElement('forward')
            forwardElem.setAttribute('mode', self.forward['type'])
            definition.documentElement.appendChild(forwardElem)

        bridgeElem = definition.createElement('bridge')
        bridgeElem.setAttribute('name', self.brName)
        bridgeElem.setAttribute('stp', 'on')
        bridgeElem.setAttribute('delay', '5')
        definition.documentElement.appendChild(bridgeElem)

        ipElem = definition.createElement('ip')
        ipElem.setAttribute('address', self.brAddr)
        ipElem.setAttribute('netmask', self.netmask)
        if self.dhcp['used']:
            dhcpElem = definition.createElement('dhcp')
            rangeElem = definition.createElement('range')
            rangeElem.setAttribute('start', self.dhcp['rangeStart'])
            rangeElem.setAttribute('end', self.dhcp['rangeEnd'])
            dhcpElem.appendChild(rangeElem)
            ipElem.appendChild(dhcpElem)

        definition.documentElement.appendChild(ipElem)

        self.xml = definition.toprettyxml()
        return self.xml

    def writeXML(self, filePath):
        """
        writes xml definition to given file
        """
        f = open(filePath, 'w')
        f.write(self.toXML())
        f.close()

    @staticmethod
    def parseConfigFile(path):
        """
        parses given config file
        """
        configFile = open(path, 'r')
        try:
            config = yaml.safe_load(configFile)
        except Exception:
            print "Bad network configuration file. exiting"
            sys.exit(1)

        return config
