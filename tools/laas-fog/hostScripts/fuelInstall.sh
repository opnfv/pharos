#!/bin/bash
#FUEL_ISO=$(curl https://www.opnfv.org/software/downloads | grep ISO | grep fuel| grep -o -e "http://artifacts.opnfv.org/fuel.*iso")

#wget $FUEL_ISO -O /vm/fuel.iso

virsh start master

ret=''
count=0
while [ -z "$ret" ]; do
    count=$(expr $count + 1)
    echo "Master node is not accepting ssh. Sleeping 15 seconds..."
    sleep 15
    ret=$(nmap 10.20.0.2 -PN -p ssh | grep open)
    #if [ $count -gt 60 ]; then
    #    echo "Host has timed out."
    #    exit 1
    #fi
done

${1}/expectKeygen.sh
${1}/expectKeyCopy.sh root@10.20.0.2 r00tme

ssh root@10.20.0.2 killall fuelmenu

echo "killed fuel menu. Waiting for installation to complete"

count=0
ans=''
while [ -z "$ans" ]; do
    count=$(expr $count + 1)
    echo "fuel api unavailable. Sleeping 15 seconds..."
    sleep 15
    ans=$(curl http://10.20.0.2:8000 2>/dev/null )
    #if [ $count -gt 60 ]; then
    #    echo "Host has timed out."
    #    exit 1
    #fi
done
