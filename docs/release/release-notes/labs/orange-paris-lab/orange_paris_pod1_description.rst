.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

**************************
POD Specification Template
**************************

Introduction
------------

Orange is hosting an OPNFV test lab at Chatillon (near Paris) facility.  The test lab would host 4
(1 controller and 3 computes) baremetal servers for the use of OPNFV community as part of the OPNFV
Pharos Project.

Version: Brahmaputra
Installer: Fuel (with Ceph)

Additional Requirements
-----------------------

Server Specifications
---------------------

**Switch**

+-----------+----------+---------+---------------+-------+--------+---------+---------------------+------------------+------------------+----------+
|           |          |         |               |       |        | Local   | Lights-out network  | 1GbE: NIC#/IP    | 10GbE: NIC#/IP   |          |
|  Hostname |  Vendor  | Model   | Serial Number |  CPUs | Memory | storage | (IPMI): IP/MAC, U/P | MAC/VLAN/Network | MAC/VLAN/Network | Notes    |
+-----------+----------+---------+---------------+-------+--------+---------+---------------------+------------------+------------------+----------+
| pod1-     |  JUNIPER | EX-4550 | 750-045407    |       |        |         | 172.31.2.254        |                  |                  | 32 ports |
| switch    |          |         |               |       |        |         | CC:E1:7F:86:38:80   |                  |                  |          |
|           |          |         |               |       |        |         |                     |                  |                  |          |
+-----------+----------+---------+---------------+-------+--------+---------+---------------------+------------------+------------------+----------+

**Jump Host**

+-----------+---------+----------+---------------+----------------+--------+-----------+---------------------+------------------+------------------+-------+
|           |         |          |               |                |        | Local     | Lights-out network  | 1GbE: NIC#/IP    | 10GbE: NIC#/IP   |       |
|  Hostname |  Vendor | Model    | Serial Number |  CPUs          | Memory | storage   | (IPMI): IP/MAC, U/P | MAC/VLAN/Network | MAC/VLAN/Network | Notes |
+-----------+---------+----------+---------------+----------------+--------+-----------+---------------------+------------------+------------------+-------+
| pod1-     |  DELL   | Proliant |  CZJ40901PV   |  Intel Xeon    |  16 GB | 300GB SAS |                     | IF0: 172.31.13.5 |                  |       |
| jump-host |         | DL 360e  |               | E5-2430 v2.2   |        | 300GB SAS |                     |                  |                  |       |
|           |         | Gen8     |               | 2,5Ghz 24 core |        |           |                     |                  |                  |       |
+-----------+---------+----------+---------------+----------------+--------+-----------+---------------------+------------------+------------------+-------+

**Firewall**

+-----------+---------+------------+---------------+-------------+--------+-----------+---------------------+--------------------+------------------+-------+
|           |         |            |               |             |        | Local     | Lights-out network  | 1GbE: NIC#/IP      | 10GbE: NIC#/IP   |       |
|  Hostname |  Vendor | Model      | Serial Number |  CPUs       | Memory | storage   | (IPMI): IP/MAC, U/P | MAC/VLAN/Network   | MAC/VLAN/Network | Notes |
+-----------+---------+------------+---------------+-------------+--------+-----------+---------------------+--------------------+------------------+-------+
| pod1-     |  IBM    | @Server    |               |  Intel Xeon |   4 GB | 36GB SATA |                     | IF0: 161.105.211.2 |                  |       |
| firewall  |         | xSerie 336 |  KKTVY4M      |             |        | 36GB SATA |                     |                    |                  |       |
|           |         |            |               |             |        |           |                     |                    |                  |       |
+-----------+---------+------------+---------------+-------------+--------+-----------+---------------------+--------------------+------------------+-------+

**Controller Node**

+------------+---------+-----------+---------------+---------------+--------+-----------+---------------------+------------------------+------------------+-------+
|            |         |           |               |               |        | Local     | Lights-out network  | 1GbE: NIC#/IP          | 10GbE: NIC#/IP   |       |
|  Hostname  |  Vendor | Model     | Serial Number |  CPUs         | Memory | storage   | (IPMI): IP/MAC, U/P | MAC/VLAN/Network       | MAC/VLAN/Network | Notes |
+------------+---------+-----------+---------------+---------------+--------+-----------+---------------------+------------------------+------------------+-------+
| pod1-ctrl1 |  HP     |  Proliant |  CZJ40901PT   |  Intel Xeon   | 16GB   | 300GB SAS |                     | IF0: 9C:B6:54:95:E4:74 |                  |       |
|            |         |  DL 360e  |               |  E5-2430 v2.2 |        | 300GB SAS |                     |      Admin             |                  |       |
|            |         |  Gen8     |               |  2,5Ghz       |        |           |                     | IF1: 9C:B6:54:95:E4:75 |                  |       |
|            |         |           |               |  24 core      |        |           |                     |      18: Public        |                  |       |
|            |         |           |               |               |        |           |                     |      1500: Storage     |                  |       |
|            |         |           |               |               |        |           |                     |      17: Management    |                  |       |
|            |         |           |               |               |        |           |                     |      1502: Private     |                  |       |
+------------+---------+-----------+---------------+---------------+--------+-----------+---------------------+------------------------+------------------+-------+

**Compute Nodes**

+------------+---------+-----------+---------------+---------------+----------+------------+---------------------+------------------------+------------------+-------+
|            |         |           |               |               |          | Local      | Lights-out network  | 1GbE: NIC#/IP          | 10GbE: NIC#/IP   |       |
|  Hostname  |  Vendor | Model     | Serial Number |  CPUs         | Memory   | storage    | (IPMI): IP/MAC, U/P | MAC/VLAN/Network       | MAC/VLAN/Network | Notes |
+------------+---------+-----------+---------------+---------------+----------+------------+---------------------+------------------------+------------------+-------+
| pod1-node1 |  DELL   |  R730     |  8F3J642      |  Intel Xeon   | 128GB    | 250GB SATA |                     | IF0: EC:F4:BB:CB:62:9C |                  |       |
|            |         |           |               |  E5-2603 v3   | (8x16GB) | 480GB SSD  |                     |      Admin             |                  |       |
|            |         |           |               |  1,6Ghz       | 1600Mhz  | 480GB SSD  |                     | IF1: EC:F4:BB:CB:62:9A |                  |       |
|            |         |           |               |  12 core      |          |            |                     |      18: Public        |                  |       |
|            |         |           |               |               |          |            |                     |      1500: Storage     |                  |       |
|            |         |           |               |               |          |            |                     |      17: Management    |                  |       |
|            |         |           |               |               |          |            |                     |      1502: Private     |                  |       |
+------------+---------+-----------+---------------+---------------+----------+------------+---------------------+------------------------+------------------+-------+
| pod1-node2 |  HP     |  Proliant |  CZJ40901PS   |  Intel Xeon   | 16GB     | 300GB SAS  |                     | IF0: 9C:B6:54:95:D4:F0 |                  |       |
|            |         |  DL 360e  |               |  E5-2430 v2.2 |          | 300GB SAS  |                     |      Admin             |                  |       |
|            |         |  Gen8     |               |  2,5Ghz       |          |            |                     | IF1: 9C:B6:54:95:D4:F1 |                  |       |
|            |         |           |               |  24 core      |          |            |                     |      18: Public        |                  |       |
|            |         |           |               |               |          |            |                     |      1500: Storage     |                  |       |
|            |         |           |               |               |          |            |                     |      17: Management    |                  |       |
|            |         |           |               |               |          |            |                     |      1502: Private     |                  |       |
+------------+---------+-----------+---------------+---------------+----------+------------+---------------------+------------------------+------------------+-------+
| pod1-node3 |  DELL   |  R730     |  FG3J642      |  Intel Xeon   | 128GB    | 256GB SATA |                     | IF0: EC:F4:BB:CB:62:E4 |                  |       |
|            |         |           |               |  E5-2603 v3   | (8x16GB) | 480GB SSD  |                     |      Admin             |                  |       |
|            |         |           |               |  1,6Ghz       | 1600Mhz  | 480GB SSD  |                     | IF1: EC:F4:BB:CB:62:E2 |                  |       |
|            |         |           |               |  12 core      |          |            |                     |      18: Public        |                  |       |
|            |         |           |               |               |          |            |                     |      1500: Storage     |                  |       |
|            |         |           |               |               |          |            |                     |      17: Management    |                  |       |
|            |         |           |               |               |          |            |                     |      1502: Private     |                  |       |
+------------+---------+-----------+---------------+---------------+----------+------------+---------------------+------------------------+------------------+-------+

Users
-----

+------+-------+---------+------+-------+
| Name | Email | Company | Role | Notes |
+------+-------+---------+------+-------+
|      |       |         |      |       |
+------+-------+---------+------+-------+

Firewall Rules
--------------

+------------+------------+------+
| Port(s)    | Service    | Note |
+------------+------------+------+
| 22, 43, 80 | Jenkins CI |      |
+------------+------------+------+

POD Topology
------------

Provide a diagram showing the network topology of the POD. Any security sensitive details should not
be exposed publically and can be stored in the secure Pharos repo. The following diagram is an
example only.

.. image:: ./images/orange_paris_pod1.jpg
   :alt: POD diagram not found
