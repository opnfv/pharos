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

import yaml
import jinja2


class Domain:
    """
    This class defines a libvirt vm abstraction that can parse our simple
    config file and add all necessary boiler plate and info to write a full xml
    definition of itself for libvirt.
    """
    JINJA_TEMPLATE = ""

    def __init__(self, propertiesDict):
        """
        init function.
        properiesDict should be one of the dictionaries returned by the static
        method parseConfigFile
        """
        self.name = propertiesDict['name']
        self.memory = propertiesDict['memory']
        self.vcpus = propertiesDict['vcpus']
        self.disk = propertiesDict['disk']
        self.iso = propertiesDict['iso']
        # the vm will either boot from an iso or pxe
        self.netBoot = not self.iso['used']
        self.interfaces = propertiesDict['interfaces']

    def toXML(self):
        """
        returns the xml definition of this domain
        """
        return self.jinja_toXML()

    def writeXML(self, filePath):
        """
        writes this domain's xml definition to the given file.
        """
        f = open(filePath, 'w')
        f.write(self.toXML())
        f.close()

    def jinja_toXML(self, template_path=None):
        """
        Uses a jinja template to simply create an xml
        definition of this domain
        returns a string
        """
        if template_path is None:
            template_path = self.JINJA_TEMPLATE
        template = jinja2.Template(open(template_path).read())
        xml_doc = template.render(
                name=self.name,
                memory=self.memory,
                cpu=self.vcpus,
                iso=self.iso,
                networks=self.interfaces,
                disk=self.disk
                )
        self.xml = xml_doc
        return self.xml

    @classmethod
    def parseConfigFile(cls, path):
        """
        parses the domains config file
        """
        configFile = open(path, 'r')
        try:
            config = yaml.safe_load(configFile)
        except Exception:
            print "Invalid domain configuration. exiting"
        cls.JINJA_TEMPLATE = config['jinja-template']
        return config['domains']
