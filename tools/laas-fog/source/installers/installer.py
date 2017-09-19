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


class Installer(object):
    """
    This is a simple base class to define a single constructor
    for all the different installer types.
    I may move more functionality to this class as we add support for more
    installers and there becomes common fucntions that would be nice to share
    between installers.
    """

    def __init__(self, domList, netList, libvirt_handler, util):
        self.doms = domList
        self.nets = netList
        self.libvirt = libvirt_handler
        self.osid = 0
        self.util = util
        self.log = util.createLogger(util.hostname)
