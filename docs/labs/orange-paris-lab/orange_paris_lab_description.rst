.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0

**************************
Lab Specification Template
**************************

Introduction
------------

Orange is hosting an OPNFV test lab at Chatillon (near Paris) facility.  The test lab would host
baremetal servers for the use of OPNFV community as part of the OPNFV Pharos Project.

The Orange Paris lab consist of 1 POD
    * POD for Fuel


Lab Resources
-------------

+-------------+------------+-----------------+----------+-----------+---------+-------+
| POD Name    | Project(s) | Project Lead(s) | Email(s) |  POD Role |  Status | Notes |
+-------------+------------+-----------------+----------+-----------+---------+-------+
| opnfv-integ |            |                 |          |  Dev/test |  Active |       |
+-------------+------------+-----------------+----------+-----------+---------+-------+

* **POD Name:** Use consistent naming / numbering to avoid confusion. Hyperlinked to POD description.
* **POD Role:** CI stable, CI latest, Dev/test, Stand-alone, Virtual, ...
* **Status:** Assigned, Configuring, Active, Troubleshooting, Available, ...


Acceptable Usage Policy
-----------------------

Define lab user policies and expectations


Remote Access Infrastructure
----------------------------

The Orange Paris OPNFV test lab is free to use for the OPNFV community.

A VPN is used to provide access to the Orange Paris Testlab.

To access the Testlab, please contact Auboin Cyril (cyril.auboin@orange.com) with the following
details:
* Name
* Organization
* Purpose of using the labs
* Dates start / end

Processing the request can take 3-4 business days.


Remote Access Procedure
-----------------------

Define lab process for requesting access to the lab (e.g. VPN guide, how to modify BIOS settings,
etc.)


Lab Documentation
-----------------

List lab specific documents here


Lab Topology
------------

Provide a diagram showing the network topology of lab including lights-out network. Any security
sensitive details should not be exposed publically. The following diagram is an example only.

.. image:: ./images/orange_paris_pod1.jpg
   :alt: Lab diagram not found
