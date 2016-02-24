.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.


Hardware
--------

A pharos compliant OPNFV test-bed provides:

- One CentOS 7 jump server on which the virtualized Openstack/OPNFV installer runs
- In the Brahmaputra release you may select a variety of deployment toolchains to deploy from the jump server.
- 5 compute / controller nodes (`BGS <https://wiki.opnfv.org/get_started/get_started_work_environment>`_ requires 5 nodes)
- A configured network topology allowing for LOM, Admin, Public, Private, and Storage Networks
- Remote access as defined by the Jenkins slave configuration guide

http://artifacts.opnfv.org/brahmaputra.1.0/docs/opnfv-jenkins-slave-connection.brahmaputra.1.0.html

**Servers**

**CPU:**

* Intel Xeon E5-2600v2 Series or newer

**Local Storage:**

Below describes the minimum for the Pharos spec, which is designed to provide enough capacity for
a reasonably functional environment. Additional and/or faster disks are nice to have and mayproduce
a better result.

* Disks: 2 x 1TB HDD + 1 x 100GB SSD (or greater capacity)
* The first HDD should be used for OS & additional software/tool installation
* The second HDD is configured for CEPH object storage
* The SSD should be used as the CEPH journal
* Performance testing requires a mix of compute nodes with CEPH (Swift+Cinder) and without CEPH storage
* Virtual ISO boot capabilities or a separate PXE boot server (DHCP/tftp or Cobbler)

**Memory:**

* 32G RAM Minimum

**Power Supply**

* Single power supply acceptable (redundant power not required/nice to have)
