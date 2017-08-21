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
import yaml
import jinja2


class Network:
    """
    This class has a similar role as the Domain class.
    This class will parse a config file and
    write the xml definitions of those networks for libvirt.
    """
    JINJA_TEMPLATE = ""

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
        Returns a string representation of the
        xml definition of this network
        """
        return self.jinja_toXML()

    def writeXML(self, filePath):
        """
        writes xml definition to given file
        """
        f = open(filePath, 'w')
        f.write(self.toXML())
        f.close()

    def jinja_toXML(self, template_path=None):
        """
        Uses a jinja template to create an xml
        definition for this network.
        returns a string
        """
        if template_path is None:
            template_path = self.JINJA_TEMPLATE
        template = jinja2.Template(open(template_path).read())
        xml_doc = template.render(
                net_name=self.name,
                br_name=self.brName,
                netmask=self.netmask,
                ip_addr=self.brAddr
                )
        self.xml = xml_doc
        return self.xml

    @classmethod
    def parseConfigFile(cls, path):
        """
        parses given config file
        """
        configFile = open(path, 'r')
        try:
            config = yaml.safe_load(configFile)
        except Exception:
            print "Bad network configuration file. exiting"
            sys.exit(1)
        cls.JINJA_TEMPLATE = config['jinja-template']
        return config['networks']
