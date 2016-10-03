#!/bin/bash

for i in range $(seq 1 5);do
	qemu-kvm -m 512M -boot n -enable-kvm -net nic -net user,tftp=/srv/tftp/,bootfile=/pxelinux.0 &
done
