#!/usr/bin/python
import subprocess
import sys
import os
import json
from pharos import Pharos_api

def checkArgs():
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
        json.loads(open(config_file).read()) #verifies that the file exists, is readable, and formatted correctly
        return config_file    
    except Exception:
        print "Bad config file"
        sys.exit(1)
    
    
config = checkArgs() 
pharos_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"pharos.py")
subprocess.Popen(['/usr/bin/python',pharos_path,'--config',config])

    
