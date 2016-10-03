#!/bin/sh

# Source profile for $PATH just in case it wasn't auto-loaded
source /etc/profile

rc-update add mdev sysinit
rc-update add devfs sysinit
rc-update add dmesg sysinit
rc-update add hostname sysinit
rc-update add sysctl sysinit
rc-update add syslog sysinit
rc-update add initialnetwork sysinit
#rc-update add networking sysinit
#rc-update add bootmisc sysinit
#rc-update add hwclock sysinit

rc-update add mount-ro shutdown
rc-update add killprocs shutdown
rc-update add savecache shutdown

rc-update add sshd default
