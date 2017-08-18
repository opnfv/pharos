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

import xml.dom
import xml.dom.minidom
import yaml


class Domain:
    """
    This class defines a libvirt vm abstraction that can parse our simple
    config file and add all necessary boiler plate and info to write a full xml
    definition of itself for libvirt.
    """

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
        combines the given configuration with a lot of
        boiler plate to create a valid libvirt xml
        definition of a domain.
        returns a string
        """
        definition = xml.dom.minidom.parseString("<domain>\n</domain>")
        definition.documentElement.setAttribute('type', 'kvm')

        nameElem = definition.createElement('name')
        nameElem.appendChild(definition.createTextNode(self.name))
        definition.documentElement.appendChild(nameElem)

        memElem = definition.createElement('memory')
        memElem.appendChild(definition.createTextNode(str(self.memory)))
        definition.documentElement.appendChild(memElem)

        curMemElem = definition.createElement('currentMemory')
        curMemElem.appendChild(definition.createTextNode(str(self.memory)))
        definition.documentElement.appendChild(curMemElem)

        vcpuElem = definition.createElement('vcpu')
        vcpuElem.appendChild(definition.createTextNode(str(self.vcpus)))
        definition.documentElement.appendChild(vcpuElem)

        osElem = definition.createElement('os')

        typeElem = definition.createElement('type')
        typeElem.setAttribute('arch', 'x86_64')
        typeElem.appendChild(definition.createTextNode('hvm'))
        osElem.appendChild(typeElem)

        if self.netBoot:
            bootElem = definition.createElement('boot')
            bootElem.setAttribute('dev', 'network')
            osElem.appendChild(bootElem)

        bootElem = definition.createElement('boot')
        bootElem.setAttribute('dev', 'hd')
        osElem.appendChild(bootElem)

        if self.iso['used']:
            bootElem = definition.createElement('boot')
            bootElem.setAttribute('dev', 'cdrom')
            osElem.appendChild(bootElem)

        definition.documentElement.appendChild(osElem)

        featureElem = definition.createElement('feature')
        featureElem.appendChild(definition.createElement('acpi'))
        featureElem.appendChild(definition.createElement('apic'))

        definition.documentElement.appendChild(featureElem)

        cpuElem = definition.createElement('cpu')
        cpuElem.setAttribute('mode', 'custom')
        cpuElem.setAttribute('match', 'exact')
        modelElem = definition.createElement('model')
        modelElem.appendChild(definition.createTextNode('Broadwell'))
        cpuElem.appendChild(modelElem)

        definition.documentElement.appendChild(cpuElem)

        clockElem = definition.createElement('clock')
        clockElem.setAttribute('offset', 'utc')

        timeElem = definition.createElement('timer')
        timeElem.setAttribute('name', 'rtc')
        timeElem.setAttribute('tickpolicy', 'catchup')
        clockElem.appendChild(timeElem)

        timeElem = definition.createElement('timer')
        timeElem.setAttribute('name', 'pit')
        timeElem.setAttribute('tickpolicy', 'delay')
        clockElem.appendChild(timeElem)

        timeElem = definition.createElement('timer')
        timeElem.setAttribute('name', 'hpet')
        timeElem.setAttribute('present', 'no')
        clockElem.appendChild(timeElem)

        definition.documentElement.appendChild(clockElem)

        poweroffElem = definition.createElement('on_poweroff')
        poweroffElem.appendChild(definition.createTextNode('destroy'))

        definition.documentElement.appendChild(poweroffElem)

        rebootElem = definition.createElement('on_reboot')
        rebootElem.appendChild(definition.createTextNode('restart'))

        definition.documentElement.appendChild(rebootElem)

        crashElem = definition.createElement('on_reboot')
        crashElem.appendChild(definition.createTextNode('restart'))

        definition.documentElement.appendChild(crashElem)

        pmElem = definition.createElement('pm')
        memElem = definition.createElement('suspend-to-mem')
        memElem.setAttribute('enabled', 'no')
        pmElem.appendChild(memElem)
        diskElem = definition.createElement('suspend-to-disk')
        diskElem.setAttribute('enabled', 'no')
        pmElem.appendChild(diskElem)

        definition.documentElement.appendChild(pmElem)

        deviceElem = definition.createElement('devices')

        emuElem = definition.createElement('emulator')
        emuElem.appendChild(definition.createTextNode('/usr/libexec/qemu-kvm'))
        deviceElem.appendChild(emuElem)

        diskElem = definition.createElement('disk')
        diskElem.setAttribute('type', 'file')
        diskElem.setAttribute('device', 'disk')

        driverElem = definition.createElement('driver')
        driverElem.setAttribute('name', 'qemu')
        driverElem.setAttribute('type', 'qcow2')
        diskElem.appendChild(driverElem)

        sourceElem = definition.createElement('source')
        sourceElem.setAttribute('file', self.disk)
        diskElem.appendChild(sourceElem)

        targetElem = definition.createElement('target')
        targetElem.setAttribute('dev', 'hda')
        targetElem.setAttribute('bus', 'ide')
        diskElem.appendChild(targetElem)

        deviceElem.appendChild(diskElem)

        if self.iso['used']:
            diskElem = definition.createElement('disk')
            diskElem.setAttribute('type', 'file')
            diskElem.setAttribute('device', 'cdrom')

            driverElem = definition.createElement('driver')
            driverElem.setAttribute('name', 'qemu')
            driverElem.setAttribute('type', 'raw')
            diskElem.appendChild(driverElem)

            sourceElem = definition.createElement('source')
            sourceElem.setAttribute('file', self.iso['location'])
            diskElem.appendChild(sourceElem)

            targetElem = definition.createElement('target')
            targetElem.setAttribute('dev', 'hdb')
            targetElem.setAttribute('bus', 'ide')
            diskElem.appendChild(targetElem)

            diskElem.appendChild(definition.createElement('readonly'))
            deviceElem.appendChild(diskElem)

        for iface in self.interfaces:
            ifaceElem = definition.createElement('interface')
            ifaceElem.setAttribute('type', iface['type'])
            sourceElem = definition.createElement('source')
            sourceElem.setAttribute(iface['type'], iface['name'])
            modelElem = definition.createElement('model')
            modelElem.setAttribute('type', 'e1000')
            ifaceElem.appendChild(sourceElem)
            ifaceElem.appendChild(modelElem)
            deviceElem.appendChild(ifaceElem)

        graphicElem = definition.createElement('graphics')
        graphicElem.setAttribute('type', 'vnc')
        graphicElem.setAttribute('port', '-1')
        deviceElem.appendChild(graphicElem)

        consoleElem = definition.createElement('console')
        consoleElem.setAttribute('type', 'pty')
        deviceElem.appendChild(consoleElem)

        definition.documentElement.appendChild(deviceElem)
        return definition.toprettyxml()

    def writeXML(self, filePath):
        """
        writes this domain's xml definition to the given file.
        """
        f = open(filePath, 'w')
        f.write(self.toXML())
        f.close()

    @staticmethod
    def parseConfigFile(path):
        """
        parses the domains config file
        """
        configFile = open(path, 'r')
        try:
            config = yaml.safe_load(configFile)
        except Exception:
            print "Invalid domain configuration. exiting"
        return config
