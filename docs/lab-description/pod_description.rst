.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

.. _pharos_pod:

**************************
POD Specification Template
**************************

Introduction
------------

Add an summary of the POD usage (Project, CI stable, CI latest, dev/test, stand-alone servers, etc.)


Additional Requirements
-----------------------

Describe any addional POD requirements beyond a standard Pharos compliant POD e.g. test equipment,
shared usage, ...


Server Specifications
---------------------

**Jump Host**

+----------+--------+-------+---------------+-----------+--------+-----------+---------------------+-------------------+-------------------+-------+
|          |        |       |               |           |        | Local     | Lights-out network  | 1GbE: NIC#/IP     | 10GbE: NIC#/IP    |       |
| Hostname | Vendor | Model | Serial Number | CPUs      | Memory | Storage   | (IPMI): IP/MAC, U/P | MAC/VLAN/Network  | MAC/VLAN/Network  | Notes |
+----------+--------+-------+---------------+-----------+--------+-----------+---------------------+-------------------+-------------------+-------+
| jump     | Dell   | R730  | ABCDEF007     | E5-2699x2 | 64 GB  | 240GB SSD | 10.10.10.10         | IF0: 10.2.117.36  | IF2: 10.2.12.1    |       |
|          |        |       |               |           |        | 1 TB SATA | 00:1E:67:D4:36:9A   | 00:1E:67:4F:B7:B1 | 00:1E:67:4F:B7:B4 |       |
|          |        |       |               |           |        |           | root/root           | VLAN 984          | VLAN 202          |       |
|          |        |       |               |           |        |           |                     | Public            | Private           |       |
|          |        |       |               |           |        |           |                     | IF1: 10.2.1.1     | IF3: 10.2.13.1    |       |
|          |        |       |               |           |        |           |                     | 00:1E:67:4F:B7:B2 | 00:1E:67:4F:B7:B5 |       |
|          |        |       |               |           |        |           |                     | VLAN 201          | VLAN 203          |       |
|          |        |       |               |           |        |           |                     | Admin             | Storage           |       |
+----------+--------+-------+---------------+-----------+--------+-----------+---------------------+-------------------+-------------------+-------+


**Compute Nodes**

+----------+--------+-------+---------------+------+--------+---------+---------------------+------------------+------------------+-------+
|          |        |       |               |      |        | Local   | Lights-out network  | 1GbE: NIC#/IP    | 10GbE: NIC#/IP   |       |
| Hostname | Vendor | Model | Serial Number | CPUs | Memory | Storage | (IPMI): IP/MAC, U/P | MAC/VLAN/Network | MAC/VLAN/Network | Notes |
+----------+--------+-------+---------------+------+--------+---------+---------------------+------------------+------------------+-------+
| node1    |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
+----------+--------+-------+---------------+------+--------+---------+---------------------+------------------+------------------+-------+
| node2    |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
+----------+--------+-------+---------------+------+--------+---------+---------------------+------------------+------------------+-------+
| node3    |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
+----------+--------+-------+---------------+------+--------+---------+---------------------+------------------+------------------+-------+
| node4    |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
+----------+--------+-------+---------------+------+--------+---------+---------------------+------------------+------------------+-------+
| node5    |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
|          |        |       |               |      |        |         |                     |                  |                  |       |
+----------+--------+-------+---------------+------+--------+---------+---------------------+------------------+------------------+-------+

VPN Users
---------

+----------+--------------+---------+-------------+------------+
| Name     | Email        | Project | Role        | Notes      |
+----------+--------------+---------+-------------+------------+
| joe user | ju@gmail.com | Pharos  | contributer | CI support |
+----------+--------------+---------+-------------+------------+


Firewall Rules
--------------

+------------+------------+-------+
| Port(s)    | Service    | Notes |
+------------+------------+-------+
| 22, 43, 80 | Jenkins CI |       |
+------------+------------+-------+


POD Topology
------------

Provide a diagram showing the network topology of the POD. Any security sensitive details should not
be exposed publically and can be stored in the secure Pharos repo. The following diagram is an
example only.

.. image:: ./images/pod_topology_example.png
   :alt: POD diagram not found
