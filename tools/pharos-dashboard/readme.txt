##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


The dashboard is deployed using docker-compose.
Application / database files are saved in /var/lib/pharos_dashboard/.

Deployment:

- clone the repository
- complete the config.env.sample file and save it as config.env
- install docker, docker-compose and bower
- run 'bower install' in ./src/static/ to fetch javascript dependencies
- run 'make build' to build the containers
- run 'make up' to run the dashboard

Updating:

- make stop
- git pull
- run 'bower install' if javascript dependencies changed
- make build
- make start

If there is migrations that need user input (like renaming a field), they need to be run manually!

Logs / Shell access:

- there is some shortcuts in the makefile