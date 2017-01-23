############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
############################################################################

# Configuration details
include config.mk

# Variables passed down to subfolder make commands
export DESTDIR
export PREFIX

SHELL=/bin/sh
BUILD=build
TMPDIR=${BUILD}/tmp

all: pharosvalidator initrd.gz

${VALIDATORSRC}:
	cd $@ && ${PY} setup.py build;

#
# START initrd make instructions
#

download-alpine:
	mkdir -p ${TMPDIR}
	pushd ${TMPDIR}/ && wget -N \
		"${ALPINE_MIRROR}/${ALPINE_BRANCH}/main/x86_64/apk-tools-static-${ALPINE_VERSION}.apk" \
		&& tar -xzf apk-tools-static-*.apk && popd

# FULL PATH to chroot
CHROOT=$(shell pwd)/${BUILD}/pxe_initrd

initrd-update: download-alpine 
	# Run the alpine installer
	./${TMPDIR}/sbin/apk.static -X "${ALPINE_MIRROR}"/"${ALPINE_BRANCH}"/main \
		-U --allow-untrusted --root ${CHROOT} --initdb add alpine-base
	# Virtual devices for /dev
	if ! [ -a "${CHROOT}"/dev/ram0 ]; \
		then mknod -m 666 "${CHROOT}"/dev/ram0 b 1 1; \
	fi;

	if ! [ -a "${CHROOT}"/dev/zero ]; \
		then mknod -m 666 "${CHROOT}"/dev/zero c 1 5; \
	fi;

	if ! [ -a "${CHROOT}"/dev/full ]; \
		then mknod -m 666 "${CHROOT}"/dev/full c 1 7 ; \
	fi;

	if ! [ -a "${CHROOT}"/dev/random ]; \
		then mknod -m 666 "${CHROOT}"/dev/random c 1 8; \
	fi;

	if ! [ -a "${CHROOT}"/dev/urandom ]; \
		then mknod -m 644 "${CHROOT}"/dev/urandom c 1 9; \
	fi;

	if ! [ -a "${CHROOT}"/dev/tty1 ]; \
		then mknod -m 666 "${CHROOT}"/dev/tty1 c 4 1; \
	fi;

	if ! [ -a "${CHROOT}"/dev/tty2 ]; \
		then mknod -m 666 "${CHROOT}"/dev/tty2 c 4 2; \
	fi;

	if ! [ -a "${CHROOT}"/dev/tty3 ]; \
		then mknod -m 666 "${CHROOT}"/dev/tty3 c 4 3; \
	fi;

	if ! [ -a "${CHROOT}"/dev/tty4 ]; \
		then mknod -m 666 "${CHROOT}"/dev/tty4 c 4 4; \
	fi;

	if ! [ -a "${CHROOT}"/dev/tty5 ]; \
		then mknod -m 666 "${CHROOT}"/dev/tty5 c 4 5; \
	fi;

	if ! [ -a "${CHROOT}"/dev/tty6 ]; \
		then mknod -m 666 "${CHROOT}"/dev/tty6 c 4 6; \
	fi;

	if ! [ -a "${CHROOT}"/dev/tty ]; \
		then mknod -m 666 "${CHROOT}"/dev/tty c 5 0; \
	fi;

	if ! [ -a "${CHROOT}"/dev/console ]; \
		then mknod -m 666 "${CHROOT}"/dev/console c 5 1; \
	fi;

	if ! [ -a "${CHROOT}"/dev/ptmx ]; \
		then mknod -m 666 "${CHROOT}"/dev/ptmx c 5 2; \
	fi;

	# link /usr/bin to /bin for package installation purposespurposes
	chroot "${CHROOT}" /bin/ln -sf /bin /usr/bin

	# Get the latest alpine mirror
	mkdir -p "${CHROOT}/etc/apk"
	echo "${ALPINE_MIRROR}/${ALPINE_BRANCH}/main" > "${CHROOT}/etc/apk/repositories"

	######################################
	# Update all packages and custom files
	######################################
	# Install custom files to initrd
	cp -rfv ${INITRDSRC}/chroot_config/* ${CHROOT}

	# update all packages and install python3 deps
	chroot ${CHROOT} apk update
	chroot ${CHROOT} apk upgrade
	chroot ${CHROOT} apk add build-base gcc make abuild binutils \
		linux-headers musl-dev python3-dev python3 openssh 
	chroot ${CHROOT} pip3 install --upgrade pip netifaces watchdog
	# Remove all build tools for smaller initrd
	chroot ${CHROOT} apk del build-base gcc make abuild binutils linux-headers musl-dev python3-dev

	# Installs the validation tool within the initrd
	cd ${VALIDATORSRC} && python3 setup.py install --prefix=${CHROOT}/usr/

	# Enables required services with initrd's service manager
	chroot ${CHROOT} rc-update add mdev sysinit
	chroot ${CHROOT} rc-update add devfs sysinit
	chroot ${CHROOT} rc-update add dmesg sysinit
	chroot ${CHROOT} rc-update add hostname sysinit
	chroot ${CHROOT} rc-update add sysctl sysinit
	chroot ${CHROOT} rc-update add syslog sysinit
	chroot ${CHROOT} rc-update add initialnetwork sysinit

	chroot ${CHROOT} rc-update add mount-ro shutdown
	chroot ${CHROOT} rc-update add killprocs shutdown
	chroot ${CHROOT} rc-update add savecache shutdown

	chroot ${CHROOT} rc-update add sshd default

check-user:
	@if [[ $(shell id -u) != 0 ]];then \
		echo "INITRD BUILD MUST BE RUN AS ROOT" \
		&& /bin/false;fi

initrd.gz: check-user initrd-update
	######################################
	# Create the initrd.gz
	######################################
	cd ${CHROOT} && find . | cpio -o -H newc | gzip > /tmp/initrd.gz
	mv /tmp/initrd.gz .

install: all
	# Install the programs to the passed in PREFIX dir
	cd ${VALIDATORSRC} && \
		${PY} setup.py install --prefix=${DESTDIR}/${PREFIX}

	cp -rf initrd.gz ${DESTDIR}/${TFTPPATH}

	cp -rf ssh /etc/pharosvalidator/

.PHONY: clean
clean:
	cd ${VALIDATORSRC} && ${PY} setup.py clean --all;

	rm -rf ${BUILD}
	rm -f initrd.gz
