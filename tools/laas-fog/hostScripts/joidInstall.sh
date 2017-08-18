#!/bin/bash
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

# parses the passed scenario
args=($(echo "$1" | tr "-" "\n"))
# args is array: [os, nosdn, nofeature, noha]

# the deploy script expects 'none' rather than 'nofeature'
if [ "nofeature" == "${args[2]}" ]; then
    args[2]="none"
fi
# grabs the joid repo
git clone "https://gerrit.opnfv.org/gerrit/joid.git"
# working directory has to be where 03-maasdeploy is
cd joid/ci
# virtualy deploy maas
./03-maasdeploy.sh virtual
# deploys OPNFV with the given scenario
./deploy.sh -o newton -s "${args[1]}" -t "${args[3]}" -l default -d xenial -m openstack -f "${args[2]}"
