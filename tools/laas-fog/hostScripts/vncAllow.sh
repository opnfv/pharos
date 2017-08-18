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

MYIP=X.X.X.X
PORT="5900:5905"
iptables -I INPUT 2 -d "$MYIP" -p tcp --dport "$PORT" -j ACCEPT
iptables -t nat -I INPUT 1 -d "$MYIP" -p tcp --dport "$PORT" -j ACCEPT
iptables -I FORWARD -p tcp --dport "$PORT" -j ACCEPT
iptables -I OUTPUT -p tcp --dport "$PORT" -j ACCEPT
