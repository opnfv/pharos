#!/bin/bash
for disk in "$@"; do
    qemu-img create -f qcow2 "$disk" 100G
done
