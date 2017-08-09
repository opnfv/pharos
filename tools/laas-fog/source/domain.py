import xml.dom
import xml.dom.minidom
import json

"""
This class defines a simple libvirt vm abstraction that can write its own xml from 
our simple xml file.
"""
class Domain:

    def __init__(self, propertiesDict):
        self.name = propertiesDict['name']
        self.memory = propertiesDict['memory']
        self.vcpus = propertiesDict['vcpus']
        self.disk = propertiesDict['disk']
        self.iso = propertiesDict['iso']
        if 'true' in self.iso['used'].lower():
            self.iso['used'] = True
            self.netBoot = False
        else:
            self.iso['used'] = False
            self.netBoot = True
        self.interfaces = propertiesDict['interfaces']


    def toXML(self):
        definition = xml.dom.minidom.parseString("<domain>\n</domain>")
        definition.documentElement.setAttribute('type','kvm')

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
        
        #add other boiler plate
        osElem = definition.createElement('os')
        
        typeElem = definition.createElement('type')
        typeElem.setAttribute('arch','x86_64')
        typeElem.appendChild(definition.createTextNode('hvm'))
        osElem.appendChild(typeElem)

        ###########Manage Boot options here######################## 
        if self.netBoot:
            bootElem = definition.createElement('boot')
            bootElem.setAttribute('dev','network')
            osElem.appendChild(bootElem)
        
        bootElem = definition.createElement('boot')
        bootElem.setAttribute('dev','hd')
        osElem.appendChild(bootElem)
        
        if self.iso['used']:
            bootElem = definition.createElement('boot')
            bootElem.setAttribute('dev','cdrom')
            osElem.appendChild(bootElem)

        definition.documentElement.appendChild(osElem)

        featureElem = definition.createElement('feature')
        featureElem.appendChild(definition.createElement('acpi'))
        featureElem.appendChild(definition.createElement('apic'))

        definition.documentElement.appendChild(featureElem)

        cpuElem = definition.createElement('cpu')
        cpuElem.setAttribute('mode','custom')
        cpuElem.setAttribute('match','exact')
        modelElem = definition.createElement('model')
        modelElem.appendChild(definition.createTextNode('Broadwell'))
        cpuElem.appendChild(modelElem)

        definition.documentElement.appendChild(cpuElem)

        clockElem = definition.createElement('clock')
        clockElem.setAttribute('offset','utc')
        
        timeElem = definition.createElement('timer')
        timeElem.setAttribute('name','rtc')
        timeElem.setAttribute('tickpolicy','catchup')
        clockElem.appendChild(timeElem)

        timeElem = definition.createElement('timer')
        timeElem.setAttribute('name','pit')
        timeElem.setAttribute('tickpolicy','delay')
        clockElem.appendChild(timeElem)

        timeElem = definition.createElement('timer')
        timeElem.setAttribute('name','hpet')
        timeElem.setAttribute('present','no')
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
        memElem.setAttribute('enabled','no')
        pmElem.appendChild(memElem)
        diskElem = definition.createElement('suspend-to-disk')
        diskElem.setAttribute('enabled','no')
        pmElem.appendChild(diskElem)

        definition.documentElement.appendChild(pmElem)


        deviceElem = definition.createElement('devices')

        #add disk and maybe iso
        emuElem = definition.createElement('emulator')
        emuElem.appendChild(definition.createTextNode('/usr/libexec/qemu-kvm'))
        deviceElem.appendChild(emuElem)

        diskElem = definition.createElement('disk')
        diskElem.setAttribute('type','file')
        diskElem.setAttribute('device','disk')
        
        driverElem = definition.createElement('driver')
        driverElem.setAttribute('name','qemu')
        driverElem.setAttribute('type','qcow2')
        diskElem.appendChild(driverElem)

        
        sourceElem = definition.createElement('source')
        sourceElem.setAttribute('file',self.disk)
        diskElem.appendChild(sourceElem)

        targetElem = definition.createElement('target')
        targetElem.setAttribute('dev','hda')
        targetElem.setAttribute('bus','ide')
        diskElem.appendChild(targetElem)

        deviceElem.appendChild(diskElem)

        if self.iso['used']:
            diskElem = definition.createElement('disk')
            diskElem.setAttribute('type','file')
            diskElem.setAttribute('device','cdrom')
            
            driverElem = definition.createElement('driver')
            driverElem.setAttribute('name','qemu')
            driverElem.setAttribute('type','raw')
            diskElem.appendChild(driverElem)

            sourceElem = definition.createElement('source')
            sourceElem.setAttribute('file',self.iso['location'])
            diskElem.appendChild(sourceElem)

            targetElem = definition.createElement('target')
            targetElem.setAttribute('dev','hdb')
            targetElem.setAttribute('bus','ide')
            diskElem.appendChild(targetElem)

            diskElem.appendChild(definition.createElement('readonly'))
            deviceElem.appendChild(diskElem)

            

        for iface in self.interfaces:
            ifaceElem = definition.createElement('interface')
            ifaceElem.setAttribute('type',iface['type'])
            sourceElem = definition.createElement('source')
            sourceElem.setAttribute(iface['type'],iface['name'])
            modelElem = definition.createElement('model')
            modelElem.setAttribute('type','e1000')
            ifaceElem.appendChild(sourceElem)
            ifaceElem.appendChild(modelElem)
            deviceElem.appendChild(ifaceElem)

        graphicElem = definition.createElement('graphics')
        graphicElem.setAttribute('type','vnc')
        graphicElem.setAttribute('port','-1')
        deviceElem.appendChild(graphicElem)

        consoleElem = definition.createElement('console')
        consoleElem.setAttribute('type','pty')
        deviceElem.appendChild(consoleElem)

        definition.documentElement.appendChild(deviceElem)
        return definition.toprettyxml()

    
    def writeXML(self, filePath):
        f = open(filePath, 'w')
        f.write(self.toXML())
        f.close()
    
    @staticmethod
    def parseConfigFile(path):
        configFile = open(path,'r')
        try:
            config = json.loads(configFile.read())
        except Exception:
            print "Invalid domain configuration. exiting"
            sys.exit(1)
        return config    

        

