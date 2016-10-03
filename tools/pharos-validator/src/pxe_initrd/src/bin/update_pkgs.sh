#!/bin/sh

source /etc/profile

# Update package list and upgrade all packages to the latest version
apk update && apk upgrade

# Install python3 and development tools to install a python module
apk add build-base gcc make abuild binutils linux-headers musl-dev python3-dev python3 openssh
pip3 install --upgrade pip netifaces watchdog

# Remove all the build tools to make the initrd smaller
apk del build-base gcc make abuild binutils linux-headers musl-dev python3-dev
