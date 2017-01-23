##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from collections import namedtuple

# Memory
MIN_MEMSIZE = 32000000 # In Kb

# Cpu
MIN_CPUFREQ = 1800.000 # In Mhz
MIN_CORECOUNT = 4

# Storage
MIN_DISKCOUNT = 3
MIN_SSDCOUNT = 1
MIN_HDDSIZE = 1000 # In Gb
MIN_SSDSIZE = 100 # In Gb

# Smallest possible disk size
MIN_DISKSIZE = min(MIN_HDDSIZE, MIN_SSDSIZE)

# Virtual deployments
# (Requirements are per node)
Opnfv_req = namedtuple("opnfv", ['CPU_CORES', 'MEMORY', 'DISK_CAP'])

APEX_REQ = Opnfv_req(4, 8000000, 40)

COMPASS_REQ = Opnfv_req(4, 4000000, 100)

JOID_REQ = Opnfv_req(4, 4000000, 100)

FUEL_REQ = Opnfv_req(4, 4000000, 100)
