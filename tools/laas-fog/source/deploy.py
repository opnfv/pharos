#!/usr/bin/python
import sys
import subprocess
import os
import json
import time
from pod_manager import Pod_Manager

"""
This file basicaly does the same thing when run from the command line as 
pod_manager does, but using this file allows you to run the deploy in
the background and log the output to a file specified in the config
file.
"""


DEFAULT_CONF = '/root/laas/conf/laas.conf'

usage = """
./deploy [--config CONFIG_FILE] [--host HOSTNAME] [--reset]
"""
def main(config_path,host):
    config = json.loads(open(config_path).read())
    
    manager = Pod_Manager(config,requested_host=host)
    manager.start_deploy()


def reset(config_path,host):
    config = json.loads(open(config_path).read())
    manager = Pod_Manager(config,requested_host=host,reset=True)

if __name__ == "__main__":
    #get variables from command line
    conf = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    conf = os.path.join(conf,"conf/laas.conf")
    host = None

    if "--help" in sys.argv:
        print usage
        sys.exit(0)
    
    if "--config" in sys.argv:
        try:
            conf = sys.argv[1+sys.argv.index("--config")]
            open(conf)
        except Exception:
            print "bad config file, using default"
    if "--host" in sys.argv:
        try:
            host = sys.argv[1+sys.argv.index("--host")]
        except:
            "host not provided. Exiting"
            sys.exit(1)
   
    try:
        config_file = json.loads(open(conf).read())
    except:
        print "Failed to read from config file"
        sys.exit(1)

    if "--reset" in sys.argv:
        reset(conf,host)
    else:
        main(conf,host)
