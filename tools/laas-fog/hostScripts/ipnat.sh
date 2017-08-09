#!/bin/bash
MYIP=$1
DESTINATION=10.20.0.2
MYBRIDGE=10.20.0.1
DESTNETWORK=10.20.0.0/24
PORTS=(8000 8443)

for PORT in ${PORTS[@]}; do

    iptables -I INPUT 2 -d $MYIP -p tcp --dport $PORT -j ACCEPT
    iptables -t nat -I INPUT 1 -d $MYIP -p tcp --dport $PORT -j ACCEPT
    iptables -I FORWARD -p tcp --dport $PORT -j ACCEPT

    iptables -t nat -I PREROUTING -p tcp -d $MYIP --dport $PORT -j DNAT --to-destination $DESTINATION:$PORT
    iptables -t nat -I POSTROUTING -p tcp -s $DESTINATION ! -d $DESTNETWORK -j SNAT --to-source $MYIP

    iptables -t nat -I POSTROUTING 2 -d $DESTINATION -j SNAT --to-source $MYBRIDGE
done
