.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

.. _pharos_lab:

************************
ZTE SH Lab Specification
************************


Introduction
------------

ZTE SH Pharos lab currently has three PODs available in Shanghai. Each POD has 5 servers, 3
controller nodes and 2 computer nodes. These PODs are dedicated for use by Production/CI. These PODs
focus scenarios related with **test** projects, **installer** projects and performance enhancement
projects, such as KVM, OVS, FDS, etc.

Scenarios planned are list here:

- os-nosdn-kvm-ha
- os-nosdn-kvm_ovs-ha

Scenarios are defined in
`Colorado Scenario Status <https://wiki.opnfv.org/display/SWREL/Colorado+Scenario+Status>`_


Lab Resources
-------------

+----------+------------+-----------+-------------------------+------------+--------+-----------+
| POD Name | Project(s) | PTL(s)    | Email(s)                | POD Role   | Status | Notes     |
+----------+------------+-----------+-------------------------+------------+--------+-----------+
| POD1     | FUEL       | Gregory   | gelkinbard@mirantis.com | CI: latest | Active | Yardstick |
|          |            | Elkinbard |                         |            |        | Funtest   |
|          |            |           |                         |            |        | Doctor    |
|          |            |           |                         |            |        | Parser    |
+----------+------------+-----------+-------------------------+------------+--------+-----------+
| POD2     | FUEL       | Gregory   | gelkinbard@mirantis.com | CI: latest | Active | Qtip      |
|          |            | Elkinbard |                         |            |        |           |
+----------+------------+-----------+-------------------------+------------+--------+-----------+
| POD3     | FUEL       | Gregory   | gelkinbard@mirantis.com | CI: latest | Active | NFV-KVM   |
|          |            | Elkinbard |                         |            |        | OVSNFV    |
+----------+------------+-----------+-------------------------+------------+--------+-----------+

- `POD1-3 wiki page <https://wiki.opnfv.org/display/pharos/ZTE+SH+Testlab>`_
* `POD1 jenkins slave <https://build.opnfv.org/ci/computer/zte-pod1/>`_
* `POD2 jenkins slave <https://build.opnfv.org/ci/computer/zte-pod2/>`_
- `POD3 jenkins slave <https://build.opnfv.org/ci/computer/zte-pod3/>`_


Acceptable Usage Policy
-----------------------

Resources located in OPNFV ZTE SH lab shall only be used for CI, infra setup/configuration and
troubleshooting purposes. No development work is allowed in these PODs.


Remote Access Infrastructure
----------------------------

ZTE SH lab provide the OpenVPN access for you.


Remote Access Procedure
-----------------------

Access to this environment can be granted by sending an e-mail to: **yangyang1@zte.com.cn**.

Subject: opnfv zte-pod[1-3] access.

The following information should be provided in the request:

::

    Full name:
    E-mail:
    Organization:
    Why is access needed:
    How long is access needed:
    What specific Host will be accessed:
    What support is needed from zte admin:

Once access requirment is approved, the instructions for setting up VPN access will be send to you by mail.


Lab Documentation
-----------------


Lab Topology
------------

.. image:: ./images/zte_sh_lab_topology.png
   :alt: Lab diagram not found

All the PODs share the same **Jump Host** for only one public IP address is allocated for ZTE
Pharos Lab. Deploy servers are separated from Jump Host. Each POD has itsown **Deploy Server**.

**Jump Host**

+----------+--------+-------+---------------+---------+--------+-----------+--------------------+------------------+-------+
|          |        |       |               |         | Memory | Local     | 1GbE: NIC#/IP      | 10GbE: NIC#/IP   |       |
| Hostname | Vendor | Model | Serial Number | CPUs    | (GB)   | Storage   | MAC/VLAN/Network   | MAC/VLAN/Network | Notes |
+----------+--------+-------+---------------+---------+--------+-----------+--------------------+------------------+-------+
| Rabbit   | HP     | 5500  | -             | X5647x2 | 24     | 250GB SAS | IF0:               |                  |       |
|          |        |       |               |         |        | 2 TB HDD  | a0:36:9f:00:11:34/ |                  |       |
|          |        |       |               |         |        |           | 192.168.1.1/       |                  |       |
|          |        |       |               |         |        |           | native vlan/OA     |                  |       |
|          |        |       |               |         |        |           | IF1:               |                  |       |
|          |        |       |               |         |        |           | a0:36:9f:00:11:35/ |                  |       |
|          |        |       |               |         |        |           | 172.10.0.1/        |                  |       |
|          |        |       |               |         |        |           | vlan 103/Public    |                  |       |
|          |        |       |               |         |        |           | 172.20.0.1/        |                  |       |
|          |        |       |               |         |        |           | vlan 113/Public    |                  |       |
|          |        |       |               |         |        |           | 172.60.0.1/        |                  |       |
|          |        |       |               |         |        |           | vlan 163/Public    |                  |       |
|          |        |       |               |         |        |           | 172.70.0.1/        |                  |       |
|          |        |       |               |         |        |           | vlan 173/Public    |                  |       |
|          |        |       |               |         |        |           | IF2:               |                  |       |
|          |        |       |               |         |        |           | a0.36:9:00:11:37/  |                  |       |
|          |        |       |               |         |        |           | 116.228.53.183/    |                  |       |
|          |        |       |               |         |        |           | native vlan/       |                  |       |
|          |        |       |               |         |        |           | Internet           |                  |       |
+----------+--------+-------+---------------+---------+--------+-----------+--------------------+------------------+-------+

