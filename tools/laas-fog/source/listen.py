#!/usr/bin/python
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
import subprocess
import sys
import os
import yaml

"""
This is the file that the user will execute to start the whole process.
This file will start the pharos api listener in a new process and then exit.
"""


def checkArgs():
    """
    error checks the cmd line args and gets the path
    of the config file
    """
    usage = "./listen.py --config <path_to_pharos_config>"
    if "--help" in sys.argv:
        print usage
        sys.exit(0)

    if "--config" not in sys.argv:
        print usage
        sys.exit(1)

    try:
        i = sys.argv.index("--config")
        config_file = sys.argv[i+1]
        # verifies that the file exists, is readable, and formatted correctly
        yaml.safe_load(open(config_file))
        return config_file
    except Exception:
        print "Bad config file"
        sys.exit(1)


# reads args and starts the pharos listener in the background
config = checkArgs()
source_dir = os.path.dirname(os.path.realpath(__file__))
pharos_path = os.path.join(source_dir, "pharos.py")
subprocess.Popen(['/usr/bin/python', pharos_path, '--config', config])
