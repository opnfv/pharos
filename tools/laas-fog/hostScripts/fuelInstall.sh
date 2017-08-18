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

virsh start master

ret=''
while [ -z "$ret" ]; do
    echo "Master node is not accepting ssh. Sleeping 15 seconds..."
    sleep 15
    ret=$(nmap 10.20.0.2 -PN -p ssh | grep open)
done

ssh-keygen -f ~/.ssh/id_rsa -t rsa -N ''
sshpass -p r00tme  ssh-copy-id -o stricthostkeychecking=no root@10.20.0.2

ssh root@10.20.0.2 killall fuelmenu

echo "killed fuel menu. Waiting for installation to complete"

ans=''
while [ -z "$ans" ]; do
    echo "fuel api unavailable. Sleeping 15 seconds..."
    sleep 15
    ans=$(curl http://10.20.0.2:8000 2>/dev/null )
done
