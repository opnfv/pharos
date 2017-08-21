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
import os
import yaml
from api.fog import FOG_Handler
from database import HostDataBase
from database import BookingDataBase

"""
This file just resets the host database with
all the hosts in fog, with all of them
showing as available

This file is just provided to make populating the host db easier.
If you wanted to do this yourself, you could do the following in
a python command prompt:
    from database import HostDataBase
    db = HostDataBase("/path/to/file")
    db.addHost("host-name")
    db.addHost("host-name")
    db.addHost("host-name")

"""
config = None
if "--config" in sys.argv:
    i = sys.argv.index("--config")
    if len(sys.argv) > i+1 and os.path.isfile(sys.argv[i+1]):
        try:
            config = yaml.safe_load(open(sys.argv[i+1]))
        except Exception:
            print "failed to read config file. exiting"
            sys.exit(1)
    else:
        print "config file not found. exiting"
        sys.exit(1)
else:
    print "no config file given. Specify file with '--config <FILE_PATH>'"
    sys.exit(1)

host = False
if "--host" in sys.argv or "--both" in sys.argv:
    host = True

booking = False
if "--booking" in sys.argv or "--both" in sys.argv:
    booking = True


if host:

    fog = FOG_Handler(
            config['fog']['server']
            )
    if os.path.isfile(config['fog']['api_key']):
        fog.getFogKeyFromFile(config['fog']['api_key'])
    else:
        fog.setFogKey(config['fog']['api_key'])

    if os.path.isfile(config['fog']['user_key']):
        fog.getUserKeyFromFile(config['fog']['user_key'])
    else:
        fog.setUserKey(config['fog']['user_key'])
    hosts = fog.getHostsinGroup("vm")
    host_names = []
    for host in hosts:
        host_names.append(host['name'])

    # creates the directory of the db, if it doesnt yet exist
    dbDir = os.path.dirname(config['database'])
    if not os.path.isdir(dbDir):
        os.makedirs(dbDir)

    db = HostDataBase(config['database'])

    # check if the table already exists or not
    try:
        db.cursor.execute("SELECT * FROM hosts")
    except Exception as err:
        if "no such table" in str(err):
            db.createTable()

    db.resetHosts(host_names)

if booking:
    db = BookingDataBase(config['database'])
    db.createTable()
    db.close()

else:
    print "you must specify the '--host', '--booking', or '--both' option"
    print "depending on which database you wish to reset"
    sys.exit(0)
