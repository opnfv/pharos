.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.


Hardware
--------

A pharos compliant OPNFV test-bed provides:

- One CentOS/Ubuntu jump server on which the virtualized Openstack/OPNFV installer runs. For an ARM
  POD, the jump server should also be an ARM server
- 3 controller nodes
- 2 compute nodes
- A configured network topology allowing for LOM, Admin, Public, Private, and Storage Networks
- Remote access as defined by the Jenkins slave configuration guide
  http://artifacts.opnfv.org/octopus/brahmaputra/docs/octopus_docs/opnfv-jenkins-slave-connection.html#jenkins-slaves

In the Euphrates release you may select a variety of deployment toolchains to deploy from the
jump server.

**Servers**

**CPU:**

* Intel Xeon E5-2600v2 Series or newer
* AArch64 (64bit ARM architecture) compatible (ARMv8 or newer)

**Firmware:**

* BIOS/EFI compatible for x86-family blades
* EFI compatible for AArch64 blades

**Local Storage:**

Below describes the minimum for the Pharos spec, which is designed to provide enough capacity for
a reasonably functional environment. Additional and/or faster disks are nice to have and mayproduce
a better result.

* Disks: 2 x 1TB HDD + 1 x 100GB SSD (or greater capacity)
* The first HDD should be used for OS & additional software/tool installation
* The second HDD is configured for CEPH OSD
* The SSD should be used as the CEPH journal
* Performance testing requires a mix of compute nodes with CEPH (Swift+Cinder) and without CEPH storage
* Virtual ISO boot capabilities or a separate PXE boot server (DHCP/tftp or Cobbler)

**Memory:**

* 32G RAM Minimum

**Power Supply**

* Single power supply acceptable (redundant power not required/nice to have)
