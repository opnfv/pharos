##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

include config.mk

# Don't customize these
CHROOT=initrd-build
DATADIR=src
ETC=etc

# Perform all but install commands
all: initrd.gz

ready-source:
	mkdir -p tmp
	pushd tmp/ && wget -N \
		"${mirror}/${branch}/main/x86_64/apk-tools-static-${version}.apk" \
		&& tar -xzf apk-tools-static-*.apk && popd

initrd.gz: ready-source
	# Run the alpine installer
	./tmp/sbin/apk.static -X "${mirror}"/"${branch}"/main \
		-U --allow-untrusted --root "${CHROOT}" --initdb add alpine-base
	# Virtual devices for /dev
	if ! [ -a "${CHROOT}"/dev/ram0 ];then mknod -m 666 "${CHROOT}"/dev/ram0 b 1 1 ;fi
	if ! [ -a "${CHROOT}"/dev/zero ];then mknod -m 666 "${CHROOT}"/dev/zero c 1 5 ;fi
	if ! [ -a "${CHROOT}"/dev/full ];then mknod -m 666 "${CHROOT}"/dev/full c 1 7 ;fi
	if ! [ -a "${CHROOT}"/dev/random ];then mknod -m 666 "${CHROOT}"/dev/random c 1 8 ;fi
	if ! [ -a "${CHROOT}"/dev/urandom ];then mknod -m 644 "${CHROOT}"/dev/urandom c 1 9 ;fi
	if ! [ -a "${CHROOT}"/dev/tty1 ];then mknod -m 666 "${CHROOT}"/dev/tty1 c 4 1 ;fi
	if ! [ -a "${CHROOT}"/dev/tty2 ];then mknod -m 666 "${CHROOT}"/dev/tty2 c 4 2 ;fi
	if ! [ -a "${CHROOT}"/dev/tty3 ];then mknod -m 666 "${CHROOT}"/dev/tty3 c 4 3 ;fi
	if ! [ -a "${CHROOT}"/dev/tty4 ];then mknod -m 666 "${CHROOT}"/dev/tty4 c 4 4 ;fi
	if ! [ -a "${CHROOT}"/dev/tty5 ];then mknod -m 666 "${CHROOT}"/dev/tty5 c 4 5 ;fi
	if ! [ -a "${CHROOT}"/dev/tty6 ];then mknod -m 666 "${CHROOT}"/dev/tty6 c 4 6 ;fi
	if ! [ -a "${CHROOT}"/dev/tty ];then mknod -m 666 "${CHROOT}"/dev/tty c 5 0 ;fi
	if ! [ -a "${CHROOT}"/dev/console ];then mknod -m 666 "${CHROOT}"/dev/console c 5 1 ;fi
	if ! [ -a "${CHROOT}"/dev/ptmx ];then mknod -m 666 "${CHROOT}"/dev/ptmx c 5 2 ;fi
	# link /usr/bin to /bin for package installation purposespurposes
	chroot "${CHROOT}" /bin/ln -sf /bin /usr/bin
	# Get the latest alpine mirror
	mkdir -p "${CHROOT}/etc/apk"
	echo "${mirror}/${branch}/main" > "${CHROOT}/etc/apk/repositories"
	######################################
	# Update all packages and custom files
	######################################
	mkdir -p "${CHROOT}/usr/src/"
	# Copy over custom scripts/files
	cp -rfv "../validation_tool/" "${CHROOT}/usr/src/"
	echo "${DATADIR}/"
	cp -rfv "${DATADIR}"/* "${CHROOT}/"
	# Run a script to update all packages
	chroot "${CHROOT}" /bin/update_pkgs.sh
	# Installs the validation tool into the chroot directory
	chroot "${CHROOT}" /bin/install_validation_tool.sh
	# Enables required services with initrd's service manager
	chroot "${CHROOT}" /bin/enable_services.sh
	######################################
	# Create the initrd.gz
	######################################
	cd "${CHROOT}" && find . | cpio -o -H newc | gzip > ../initrd.gz

install: all 
	mkdir -p "${DESTDIR}"/"${TFTPPATH}"
	cp -rf "${ETC}"/* "${DESTDIR}"/"${TFTPPATH}"/
	cp -rf initrd.gz "${DESTDIR}"/"${TFTPPATH}"/

.PHONY: clean
clean:
	rm -f initrd.gz
	rm -rf "${CHROOT}"
	rm -f apk-tools-static-*.apk
	rm -rf tmp/
