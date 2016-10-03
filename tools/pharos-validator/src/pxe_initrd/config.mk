# pxe_initrd version
VERSION=1

# Customize below to fit your system

# paths
PREFIX=/usr/
MANPREFIX=${PREFIX}/share/man
TFTPPATH=/var/lib/tftpboot
DESTDIR=/

# See MIRRORS.txt for available mirrors as of 2016-06-21, a new version of this file can be found at http://nl.alpinelinux.org/alpine/MIRRORS.txt
mirror="http://dl-cdn.alpinelinux.org/alpine/"

# For latest bleeding edge software
version="2.6.7-r1"
branch="edge"

# For a stable versioned release
#version="2.6.7-r0"
#branch="latest-stable"

