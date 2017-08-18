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

"""
This class will install Joid onto the remote host.
Currently only supports joid's "default" configuration
"""


class Joid_Installer:

    def __init__(self, doms, nets, libvirt_handler, util):
        """
        init function calls the super constructor
        """
        super(Joid_Installer, self).__init__(doms, nets, libvirt_handler, util)

    def go(self):
        """
        does all the work of this class.
        Currently just runs the joidInstall script, which installs joid
        onto the remote host
        """
        self.logger.info("%s", "Executing joid virtual installation")
        self.util.execRemoteScript("joidInstall.sh")
