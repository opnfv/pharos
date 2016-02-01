Pharos compliant environment
----------------------------

A pharos compliant OPNFV test-bed provides:

  - One CentOS 7 jump server on which the virtualized Openstack/OPNFV installer runs
  - In the Brahmaputra release you may select a variety of deployment toolchains to deploy from the jump server.
  - 5 compute / controller nodes (`BGS <https://wiki.opnfv.org/get_started/get_started_work_environment>`_ requires 5 nodes)
  - A configured network topology allowing for LOM, Admin, Public, Private, and Storage Networks
  - Remote access as defined by the Jenkins slave configuration guide
    - http://artifacts.opnfv.org/brahmaputra.1.0/docs/opnfv-jenkins-slave-connection.brahmaputra.1.0.html

Hardware requirements
---------------------

**Servers**

CPU:

  * Intel Xeon E5-2600v2 Series (Ivy Bridge and newer, or similar)

Local Storage Configuration:

The minimum requirement for the Pharos spec is descirbed below,
this is designed to provide enough capacity for
a reasonably functional environment. Additional
and/or faster disks are nice to have and may
produce a better result.

  * Disks: 2 x 1TB + 1 x 100GB SSD
  * The first 1TB HDD should be used for OS & additional software/tool installation
  * The second 1TB HDD configured for CEPH object storage
  * Finally, the 100GB SSD should be used as the CEPH journal
  * Performance testing requires a mix of compute nodes that have CEPH(swift+Cinder) and without CEPH storage
  * Virtual ISO boot capabilities or a separate PXE boot server (DHCP/tftp or Cobbler)

Memory:

  * 32G RAM Minimum

Power Supply Single

  * Single power supply acceptable (redundant power not required/nice to have)

