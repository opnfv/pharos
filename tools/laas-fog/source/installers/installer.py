"""
This is a simple base class to define a single constructor
for all the different installer types.
I may move more functionality to this class as we add support for more 
installers and there becomes common fucntions that would be nice to share 
between installers.
"""
import logging
class Installer(object):
    def __init__(self,domList,netList,libvirt_handler,util):
        self.doms = domList
        self.nets = netList
        self.libvirt = libvirt_handler
        self.osid = 0
        self.util = util
        self.logger = util.createLogger(util.hostname)
