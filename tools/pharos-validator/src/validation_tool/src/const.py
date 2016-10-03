##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

## Various constant strings used throughout program
HARDWARE_TEST="pharos-validator-node"

## Pharos hardware specification
# memory
MIN_MEMSIZE = 32000000 # In Kb

# cpu
MIN_CPUFREQ = 1800.000 # In Mhz
MIN_CORECOUNT = 4

# storage
MIN_DISKCOUNT = 3
MIN_SSDCOUNT = 1
MIN_HDDSIZE = 1000 # In Gb
MIN_SSDSIZE = 100 # In Gb
# Smallest possible disk size
MIN_DISKSIZE = min(MIN_HDDSIZE, MIN_SSDSIZE)

# Virtual deployments
# Requirements are per node
APEX_REQ = {"cores": 2, \
            "ram": 8000000, \
            "disk": 40}

# Requirements are per node
COMPASS_REQ = {"cores": 4, \
               "ram": 4000000, \
               "disk": 100}

# Requirements are per node
JOID_REQ = {"cores": 4, \
               "ram": 4000000, \
               "disk": 100}

# Requirements are per node
FUEL_REQ = {"cores": 4, \
               "ram": 4000000, \
               "disk": 100}
