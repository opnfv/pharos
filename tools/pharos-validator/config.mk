# pxe_initrd version
VERSION=1

# These variables let each project know where the others are
INITRDSRC=pxe_initrd
VALIDATORSRC=pharosvalidator

# Customize below to fit your system

# paths
PREFIX=/usr/
MANPREFIX=${PREFIX}/share/man
TFTPPATH=/var/lib/tftpboot
DESTDIR=/

# See MIRRORS.txt for available mirrors as of 2016-06-21, a new version of this file can be found at http://nl.alpinelinux.org/alpine/MIRRORS.txt
ALPINE_MIRROR="http://dl-cdn.alpinelinux.org/alpine"

# For latest bleeding edge software
ALPINE_VERSION="2.6.8-r1"
ALPINE_BRANCH="v3.5"

# Python interpreter
PY=python3.5
