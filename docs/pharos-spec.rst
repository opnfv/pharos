Pharos Specification
=====================

Objectives / Scope
-------------------

Pharos defines the state of the deployment environment (i.e. pre-deployment state). While it defines the state of the environment it does not define the implementation of a test infrastructure. This guarantees that the OPNFV platform will sucessfully deploy and can be tested using the the automated toolchain.

A Pharos compliant lab ...
- Provides a secure, scalable, standard and HA environment
- Supports full deployment lifecycle (this requires a bare metal environment)
- Supports functional and performance testing
- Provides common tooling and test scenarios (including test cases and workloads) available to the community
- Provides mechanisms and procedures for secure remote access to the test environment

Virtualized environments will be useful for development but do not provide a fully featured deployment/test capability.

The high level architecture may be summarized as follows:

.. image:: images/pharos-archi1.jpg

Constraints of a Pharos compliant OPNFV test-bed environment
-------------------------------------------------------------

- One CentOS 7 Jump Server on which the virtualized Openstack/OPNFV installer runs
- Desired installer - may be Fuel, Foreman, etc
- 2 - 5 compute / controller nodes (`BGS <https://wiki.opnfv.org/get_started/get_started_work_environment>`_ requires 5 nodes)
- Network topology allowing for Lights-out management, Admin, Public, Private, and Storage Networks
- Remote access
- Test Tools

Target Systems State
---------------------

- Target system state includes default software components, network configuration, storage requirements `https://wiki.opnfv.org/get_started/get_started_system_state <https://wiki.opnfv.org/get_started/get_started_system_state>`


Rls 1 specification is modeled on setups used for integration/deployment with Fuel and Foreman ... 

* Draft of environment for BGS https://wiki.opnfv.org/get_started/get_started_work_environment
* Fuel environment https://wiki.opnfv.org/get_started/networkingblueprint
* Foreman environment https://wiki.opnfv.org/get_started_experiment1#topology

Hardware
---------

**Servers**

CPU:

* Intel Xeon E5-2600v2 Series (Ivy Bridge and newer, or similar)

Local Storage Configuration:

Below describes the minimum for the Pharos spec, which is designed to provide enough capacity for a reasonably functional environment. Additional and/or faster disks are nice to have and may produce a better result.

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

**Provisioning**

Jump Server Installation

  * OS: CentOS 7
  * KVM / Qemu
  * Installer (Foreman, Fuel, ...) in a VM
  * Tools

See `Jump Server Installation <https://wiki.opnfv.org/jump_server_installation_guide>`_ for detailed Jump Server installation details.

Test Tools - See `functest <http://artifacts.opnfv.org/functest/docs/functest.html>`_

Controller nodes - these are bare metal servers

Compute nodes - these bare metal servers

**Infrastructure naming conventions / recommendations**

The Pharos specificaiton provides recomendations for default logins and  naming conventions

See `Infrastructure naming conventions <https://wiki.opnfv.org/pharos/pharos_naming>`_
  

Remote management
------------------

**Remote access**

- Remote access is required for …

  1. Developers to access deploy/test environments (credentials to be issued per POD / user)
  2. Connection of each environment to Jenkins master hosted by Linux Foundation for automated deployment and test

- VPN is optional and dependent on company security rules (out of Pharos scope)
- POD access rules / restrictions …

  - Refer to individual test-bed as each company may have different access rules and procedures

- Basic requirement is for SSH sessions to be established (initially on jump server)
- Majority of packages installed on a system (tools or applications) will be pulled from an external storage solution so this type of things should be solved in a very general sense for the projects

Firewall rules

- SSH sessions
- Jenkins sessions

Lights-out Management:

- Out-of-band management for power on/off/reset and bare-metal provisioning
- Access to server is through lights-out-management tool and/or a serial console
- Intel lights-out ⇒ RMM http://www.intel.com/content/www/us/en/server-management/intel-remote-management-module.html
- HP lights-out ⇒ ILO http://www8.hp.com/us/en/products/servers/ilo/index.html
- CISCO lights-out ⇒ UCS https://developer.cisco.com/site/ucs-dev-center/index.gsp

Linux Foundation - VPN service for accessing Lights-Out Management (LOM) infrastructure for the UCS-M hardware

- People with admin access to LF infrastructure:

1. amaged@cisco.com
2. cogibbs@cisco.com
3. daniel.smith@ericsson.com
4. dradez@redhat.com
5. fatih.degirmenci@ericsson.com
6. fbrockne@cisco.com
7. jonas.bjurel@ericsson.com
8. jose.lausuch@ericsson.com
9. joseph.gasparakis@intel.com
10. morgan.richomme@orange.com
11. pbandzi@cisco.com
12. phladky@cisco.com
13. stefan.k.berg@ericsson.com
14. szilard.cserey@ericsson.com
15. trozet@redhat.com

- The people who require VPN access must have a valid PGP key bearing a valid signature from one of these three people. When issuing OpenVPN credentials, LF will be sending TLS certificates and 2-factor authentication tokens, encrypted to each recipient's PGP key.

Networking
-----------

Test-bed network

* 24 or 48 Port TOR Switch
* NICS - 1GE, 10GE - per server can be on-board or PCI-e
* Connectivity for each data/control network is through a separate NIC. This simplifies Switch Management however requires more NICs on the server and also more switch ports
* Lights-out network can share with Admin/Management

Network Interfaces

* Option 1: 4x1G Control, 2x40G Data, 48 Port Switch

  * 1 x 1G for ILMI (Lights out Management )
  * 1 x 1G for Admin/PXE boot
  * 1 x 1G for control Plane connectivity
  * 1 x 1G for storage
  * 2 x 40G (or 10G) for data network (redundancy, NIC bonding, High bandwidth testing)

* Option II: 1x1G Control, 2x 40G (or 10G) Data, 24 Port Switch

  * Connectivity to networks is through VLANs on the Control NIC. Data NIC used for VNF traffic and storage traffic segmented through VLANs

* Option III: 2x1G Control, 2x10G Data, 2x40G Storage, 24 Port Switch

  * Data NIC used for VNF traffic, storage NIC used for control plane and Storage segmented through VLANs (separate host traffic from VNF)
  * 1 x 1G for IPMI
  * 1 x 1G for Admin/PXE boot
  * 2 x 10G for control plane connectivity/Storage
  * 2 x 40G (or 10G) for data network

** Topology **

- Subnet, VLANs (may be constrained by existing lab setups or rules)
- IPs
- Types of NW - lights-out, public, private, admin, storage
- May be special NW requirements for performance related projects
- Default gateways

.. image:: images/bridge1.png

controller node bridge topology overview


.. image:: images/bridge2.png

compute node bridge topology overview

Architecture
-------------

** Network Diagram **

The Pharos architecture may be described as follow: Figure 1: Standard Deployment Environment

.. image:: images/opnfv-pharos-diagram-v01.jpg

Figure 1: Standard Deployment Environment


Tools
------

- Jenkins
- Tempest / Rally
- Robot
- Git repository
- Jira
- FAQ channel

Sample Network Drawings
-----------------------

Files for documenting lab network layout. These were contributed as Visio VSDX format compressed as a ZIP file. Here is a sample of what the visio looks like.

Download the visio zip file here: `opnfv-example-lab-diagram.vsdx.zip <https://wiki.opnfv.org/_media/opnfv-example-lab-diagram.vsdx.zip>`

.. image:: images/opnfv-example-lab-diagram.png

FYI: `Here <http://www.opendaylight.org/community/community-labs>` is what the OpenDaylight lab wiki pages look like.
