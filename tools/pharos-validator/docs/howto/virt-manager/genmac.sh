#!/bin/bash
# generate a random mac address for the qemu nic
printf 'DE:AD:BE:EF:%02X:%02X\n' $((RANDOM%256)) $((RANDOM%256))
