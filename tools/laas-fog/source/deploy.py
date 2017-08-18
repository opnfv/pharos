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

import sys
import yaml
from pod_manager import Pod_Manager

"""
This file is the first executed when a booking begins.
"""

usage = """
./deploy [--config CONFIG_FILE] [--host HOSTNAME] [--reset]
"""


def main(config_path, host):
    """
    starts the deployment with the given configuration.
    """
    config = yaml.safe_load(open(config_path))

    manager = Pod_Manager(config, requested_host=host)
    manager.start_deploy()


def reset(config_path, host):
    """
    Tells the Pod Manager to clean and reset the given host.
    """
    config = yaml.safe_load(open(config_path))
    Pod_Manager(config, requested_host=host, reset=True)


if __name__ == "__main__":
    # parse command line
    host = None

    if "--help" in sys.argv:
        print usage
        sys.exit(0)

    if "--config" in sys.argv:
        try:
            conf = sys.argv[1+sys.argv.index("--config")]
            open(conf)
        except Exception:
            print "bad config file"
            sys.exit(1)
    if "--host" in sys.argv:
        try:
            host = sys.argv[1+sys.argv.index("--host")]
        except:
            "host not provided. Exiting"
            sys.exit(1)

    try:
        config_file = yaml.safe_load(open(conf))
    except:
        print "Failed to read from config file"
        sys.exit(1)
    # reset or deploy host
    if "--reset" in sys.argv:
        reset(conf, host)
    else:
        main(conf, host)
