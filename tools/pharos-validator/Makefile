##############################################################################
# Copyright (c) 2015 Todd Gaunt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

include config.mk

# Variables passed down to subfolder make commands
export DESTDIR
export PREFIX

SHELL=/bin/sh

# Source paths
SRCDIR="src/"
PXE_INITRD=${SRCDIR}/pxe_initrd/
VALIDATION_TOOL=${SRCDIR}/validation_tool/

# makefile names
PXE_MAKE=pxe_initrd.mk


all: validation_tool pxe_initrd

##########################################
# The following forces rebuilding
##########################################
.PHONY: validation_tool ${VALIDATION_TOOL}
validation_tool: ${VALIDATION_TOOL}

${VALIDATION_TOOL}:
	pushd $@ && ./setup.py build && popd

##########################################
# The following forces rebuilding
##########################################
.PHONY: pxe_initrd ${PXE_INITRD}
pxe_initrd: ${PXE_INITRD}

${PXE_INITRD}:
	${MAKE} -C $@ -f ${PXE_MAKE} all
##########################################

install: all
	# Install the programs to the passed in PREFIX dir
	${MAKE} -C ${PXE_INITRD} -f ${PXE_MAKE} install
	pushd ${VALIDATION_TOOL} && ./setup.py install --prefix=${DESTDIR}/${PREFIX} && popd

.PHONY: clean
clean:
	${MAKE} -C ${PXE_INITRD} -f ${PXE_MAKE} clean
	pushd ${VALIDATION_TOOL} && ./setup.py clean --all && popd
