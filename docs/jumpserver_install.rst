**Jump Server Configuration: **

(Rough Placeholder, edit me)

**Fuel**

- Obtain CentOS 7 Minimal ISO and install
- Set parameters appropriate for your environment during installation
- Disable NetworkManager
- Configure your /etc/sysconfig/network-scripts/ifcfg-* files for your network
- Restart networking
- Edit /etc/resolv.conf and add a nameserver
- yum -y update
- yum -y install kvm qemu-kvm libvirt
- systemctl enable libvirtd
- Reboot
- If you wish to avoid annoying delay when use ssh to log in, disable DNS lookups:
- vi /etc/ssh/sshd_config
- Uncomment "UseDNS yes", change 'yes' to 'no'.
  Save
- systemctl restart sshd
- yum -y install virt-install
- yum -y install lynx
- Visit artifacts.opnfv.org and D/L the OPNFV Fuel ISO
- Create a bridge using the interface on the PXE network, for example: br0
- Make a directory owned by qemu:
- mkdir /home/qemu; mkdir -p /home/qemu/VMs/fuel-6.0/disk
- chown -R qemu:qemu /home/qemu
- Copy the ISO to /home/qemu
- cd /home/qemu
- virt-install -n opnfv-2015-05-22_18-34-07-fuel -r 4096 --vcpus=4 --cpuset=0-3 -c opnfv-2015-05-22_18-34-07.iso --os-type=linux --os-variant=rhel6 --boot hd,cdrom --disk path=/home/qemu/VMs/mirantis-fuel-6.0/disk/fuel-vhd0.qcow2,bus=virtio,size=50,format=qcow2 -w bridge=br0,model=virtio --graphics vnc,listen=0.0.0.0
- Temporarily flush the firewall rules to make things easier:
- iptables -F
- Connect to the console of the installing VM with your favorite VNC client.
- Change the IP settings to match the pod, use an IP in the PXE network for the Fuel Master

**Foreman**

TBA
