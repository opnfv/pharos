#!/usr/bin/python
import sys
import os
import json
from api.fog import FOG_Handler
from database import HostDataBase
from database import BookingDataBase

"""
This file just resets the host database with all the hosts in fog, with all of them
showing as available
"""
config = None
if "--config" in sys.argv:
    i = sys.argv.index("--config")
    if len(sys.argv) > i+1 and os.path.isfile(sys.argv[i+1]):
        try:
            config = json.loads(open(sys.argv[i+1]).read())
        except Exception:
            print "failed to read config file. exiting"
            sys.exit(1)
    else:
        print "config file not found. exiting"
        sys.exit(1)
else:
    print "no config file given. Specify file with '--config <FILE_PATH>'"
    sys.exit(1)

if "--host" in sys.argv:

    fog = FOG_Handler(config['fog_server'],fogKey=config['fog_api_key'],userKey=config['fog_user_key'])
    hosts = fog.getHostsinGroup("vm")
    host_names = []
    for host in hosts:
        host_names.append(host['name'])

    #creates the directory of the db, if it doesnt yet exist
    dbDir = os.path.dirname(config['database'])
    if not os.path.isdir(dbDir):
        os.makedirs(dbDir)

    db = HostDataBase(config['database'])

    #check if the table already exists or not
    try:
        db.cursor.execute("SELECT * FROM hosts")
    except Exception as err:
        if "no such table" in str(err):
            db.createTable()

    db.resetHosts(host_names)

elif "--booking" in sys.argv:
    db = BookingDataBase(config['database'])
    db.createTable()
    db.close()

else:
    print "you must specify either the '--host' or '--booking' option"
    print "depending on which database you wish to reset"
    sys.exit(0)



