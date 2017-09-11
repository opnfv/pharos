.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.


Jump Server Configuration
-------------------------

Jump server install procedures are maintained by each installer project. Addional Jump server
configuraton BKMs will be maintained here. Let's take CentOS7 for example. The below install
information was used for Fuel(up to Danube, and it is replaced by MCP since Euphrates).

**Procedure**

1. Obtain CentOS 7 Minimal ISO and install

  ``wget http://mirrors.kernel.org/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1503-01.iso``

2. Set parameters appropriate for your environment during installation

3. Disable NetworkManager

  ``systemctl disable NetworkManager``

4. Configure your /etc/sysconfig/network-scripts/ifcfg-* files for your network

5. Restart networking

  ``service network restart``

6. Edit /etc/resolv.conf and add a nameserver, for example 8.8.8.8

  ``echo nameserver 8.8.8.8 >> /etc/resolv.conf``

7. Install libvirt & kvm

  ``yum -y update``
  ``yum -y install kvm qemu-kvm libvirt``
  ``systemctl enable libvirtd``

8. Reboot:

  ``shutdown -r now``

9. Configure SSHD

  If you wish to avoid annoying delay when use ssh to log in, disable DNS lookups:

  When **UseDNS** is existed in the config file, update it:

  ``sed -i -e 's/^#*UseDNS\ \+yes/UseDNS no/' /etc/ssh/sshd_config``

  or append the setting when not existed:

  ``echo UseDNS no >> /etc/ssh/ssd_config``

  Disable Password Authenticaion for security:

  ``sed -i -e 's/^#PasswordAuthentication\ \+yes/PasswordAuthentication no/' /etc/ssh/sshd_config``

  If you want to disable IPv6 connections, comment IPv6 ListenAddress and change AddressFamily to inet:

  ``sed -i -e 's/^ListenAddress\ \+::/#ListenAddress ::/' /etc/ssh/sshd_config``
  ``sed -i -e 's/^AddressFamily\ \+any/AddressFamily inet/' /etc/ssh/sshd_config``

10. Restart sshd

  ``systemctl restart sshd``

11. Install virt-install

  ``yum -y install virt-install``

12. Visit artifacts.opnfv.org and D/L the OPNFV Fuel ISO

13. Create a bridge using the interface on the PXE network, for example: br0

  ``brctl addbr br0``

14. Make a directory owned by qemu:

  ``mkdir /home/qemu; mkdir -p /home/qemu/VMs/fuel-6.0/disk``

  ``chown -R qemu:qemu /home/qemu``

15. Copy the ISO to /home/qemu

  ``cd /home/qemu``

  ``virt-install -n opnfv-2015-05-22_18-34-07-fuel -r 4096 --vcpus=4
  --cpuset=0-3 -c opnfv-2015-05-22_18-34-07.iso --os-type=linux
  --os-variant=rhel6 --boot hd,cdrom --disk
  path=/home/qemu/VMs/mirantis-fuel-6.0/disk/fuel-vhd0.qcow2,bus=virtio,size=50,format=qcow2
  -w bridge=br0,model=virtio --graphics vnc,listen=0.0.0.0``

16. Temporarily flush the firewall rules to make things easier:

  ``iptables -F``

17. Connect to the console of the installing VM with your favorite VNC client.

18. Change the IP settings to match the pod, use an IP in the PXE/Admin network for the Fuel Master
