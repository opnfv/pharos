#! /usr/bin/env bash
# Builds the pharosvalidator package as root (it must be built as root)
# then copies the finished package to /tmp. The script can either be called
# as root or with sudo

tarball=pharos-validator-1.tar.gz
specfile=pharosvalidator.spec
arch=x86_64

if [ "$(id -u)" != 0 ]; then
	echo "This script must be run as root (or with sudo)"
	exit 1
fi;

rpmdev-setuptree

cp "$specfile" ~/rpmbuild/SPECS/

# Prepare the "source package" for the rpm build process using .spec file
pushd ../../
tar -cvf "$tarball" pharos-validator
cp "$tarball" ~/rpmbuild/SOURCES
popd


cd ~/rpmbuild/

rpmlint SPECS/"$specfile"
printf "\n\nRPM BUILD PROCESS\n\n"
rpmbuild -ba SPECS/"$specfile"

cp -rfv RPMS/"$arch"/* /tmp/
