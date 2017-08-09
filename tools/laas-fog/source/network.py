import sys
import xml.dom
import xml.dom.minidom
import json

"""
This class defines a simple libvirt network abstraction that can write its own xml
from our simple config file
"""
class Network: 
    
    def __init__(self, propertiesDict):
        self.name = propertiesDict['name']
        self.brName = propertiesDict['brName']
        self.brAddr = propertiesDict['brAddr']
        self.netmask = propertiesDict['netmask']
        self.forward = propertiesDict['forward']
        if 'true' in self.forward['used'].lower():
            self.forward['used'] = True
        else:
            self.forward['used'] = False
        self.dhcp = propertiesDict['dhcp']
        if 'true' in self.dhcp['used'].lower():
            self.dhcp['used'] = True
        else:
            self.dhcp['used'] = False

        self.cidr = propertiesDict['cidr']

    

    def toXML(self):
        definition = xml.dom.minidom.parseString("<network>\n</network>")
        nameElem = definition.createElement('name')
        #assign name value
        nameElem.appendChild(definition.createTextNode(self.name))
        definition.documentElement.appendChild(nameElem)

        if self.forward['used']:
            forwardElem = definition.createElement('forward')
            forwardElem.setAttribute('mode',self.forward['type'])
            definition.documentElement.appendChild(forwardElem)

        bridgeElem = definition.createElement('bridge')
        bridgeElem.setAttribute('name',self.brName)
        bridgeElem.setAttribute('stp','on')
        bridgeElem.setAttribute('delay','5')
        definition.documentElement.appendChild(bridgeElem)

        ipElem = definition.createElement('ip')
        ipElem.setAttribute('address',self.brAddr)
        ipElem.setAttribute('netmask',self.netmask)
        if self.dhcp['used']:
            dhcpElem = definition.createElement('dhcp')
            rangeElem = definition.createElement('range')
            rangeElem.setAttribute('start',self.dhcp['rangeStart'])
            rangeElem.setAttribute('end',self.dhcp['rangeEnd'])
            dhcpElem.appendChild(rangeElem)
            ipElem.appendChild(dhcpElem)

        definition.documentElement.appendChild(ipElem)

        self.xml = definition.toprettyxml()
        
        return self.xml
    
    
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
            print "Bad network configuration file. exiting"
            sys.exit(1)

        return config
        

def main():
    networkDefs = Network.parseConfigFile('/root/Fuel/python/network.cfg')
    for net in networkDefs:
        if len(net) > 0:
            network = Network(net)
            print network.toXML()
            filename = '/root/Fuel/networks/'+network.name+'.xml'
            open(filename,'w').write(network.toXML())



#main()


