#!/bin/bash
MYIP=X.X.X.X
PORT=5900:5905
iptables -I INPUT 2 -d $MYIP -p tcp --dport $PORT -j ACCEPT
iptables -t nat -I INPUT 1 -d $MYIP -p tcp --dport $PORT -j ACCEPT
iptables -I FORWARD -p tcp --dport $PORT -j ACCEPT
iptables -I OUTPUT -p tcp --dport $PORT -j ACCEPT
