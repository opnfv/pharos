#!/bin/bash
MYIP=$1
DESTINATION=$2
MYBRIDGE=10.20.1.1
DESTNETWORK=10.20.1.0/24
PORT=80
    
iptables -I INPUT 2 -d $MYIP -p tcp --dport $PORT -j ACCEPT
iptables -t nat -I INPUT 1 -d $MYIP -p tcp --dport $PORT -j ACCEPT
iptables -I FORWARD -p tcp --dport $PORT -j ACCEPT

iptables -t nat -I PREROUTING -p tcp -d $MYIP --dport $PORT -j DNAT --to-destination $DESTINATION:$PORT
iptables -t nat -I POSTROUTING -p tcp -s $DESTINATION ! -d $DESTNETWORK -j SNAT --to-source $MYIP

iptables -t nat -I POSTROUTING 2 -d $DESTINATION -j SNAT --to-source $MYBRIDGE
