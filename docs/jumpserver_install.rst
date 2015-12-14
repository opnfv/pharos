**Jump Server Configuration:**

(Rough Placeholder, edit me)

**Fuel**

1. Obtain CentOS 7 Minimal ISO and install

  ``wget http://mirrors.kernel.org/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1503-01.iso``

2. Set parameters appropriate for your environment during installation

3. Disable NetworkManager

  ``systemctl disable NetworkManager``

4. Configure your /etc/sysconfig/network-scripts/ifcfg-* files for your network

5. Restart networking

  ``service network restart``

6. Edit /etc/resolv.conf and add a nameserver

  ``vi /etc/resolv.conf``

7. Install libvirt & kvm

  ``yum -y update``
  ``yum -y install kvm qemu-kvm libvirt``
  ``systemctl enable libvirtd``

8. Reboot:

  ``shutdown -r now``

9. If you wish to avoid annoying delay when use ssh to log in, disable DNS lookups:

  ``vi /etc/ssh/sshd_config``

  Uncomment "UseDNS yes", change 'yes' to 'no'.

  Save

10. Restart sshd

  ``systemctl restart sshd``

11. Install virt-install

  ``yum -y install virt-install``

12. Visit artifacts.opnfv.org and D/L the OPNFV Fuel ISO

13. Create a bridge using the interface on the PXE network, for example: br0

14. Make a directory owned by qemu:

  ``mkdir /home/qemu; mkdir -p /home/qemu/VMs/fuel-6.0/disk``

  ``chown -R qemu:qemu /home/qemu``

15. Copy the ISO to /home/qemu

  ``cd /home/qemu``

  ``virt-install -n opnfv-2015-05-22_18-34-07-fuel -r 4096 --vcpus=4
--cpuset=0-3 -c opnfv-2015-05-22_18-34-07.iso --os-type=linux --os-variant=rhel6 --boot hd,cdrom
--disk path=/home/qemu/VMs/mirantis-fuel-6.0/disk/fuel-vhd0.qcow2,bus=virtio,size=50,
format=qcow2 -w bridge=br0,model=virtio --graphics vnc,listen=0.0.0.0``

16. Temporarily flush the firewall rules to make things easier:

  ``iptables -F``

17. Connect to the console of the installing VM with your favorite VNC client.

18. Change the IP settings to match the pod, use an IP in the PXE/Admin network for the Fuel Master

**Foreman**

TBA
