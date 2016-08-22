.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

.. _pharos_lab:

*********************************
Ericssion OPNFV Lab Specification
*********************************


Introduction
------------

Ericsson OPNFV Lab currently has 2 Bare Metal and 3 Virtual PODs available globally (hosted in
the GIC). Each POD has 5 servers, comprised of 3 controller nodes (HA) and 2 computes nodes. NOTE:
(this make differ depending on scenario).

.. _pharos_pod:

These PODs are dedicated for use by Production/CI. These PODs focus on providing verification,
build, deploy and testing for scenarios related with **test** projects, **installer** projects and
perforamnce enhancement projects, such as KVM, OVS, FDS, etc.

In addition to the full-time CI/CD resources, the Ericsson OPNFV lab provides developer labs (DRs)
for project usage, testing and development.

Scenarios services by this lab are:

Scenario defitions can be found here:
`Colorado Scenario Status <https://wiki.opnfv.org/display/SWREL/Colorado+Scenario+Status>`_

Lab Resources
-------------

- `Ericsson Hostting And Request Page <https://wiki.opnfv.org/display/pharos/Ericsson+Hosting+and+Request+Process>`_

+------------+------------+------------+-------------------------------+------------+--------+---------+
| POD Name   | Project(s) | PTL(s)     | Email(s)                      | POD Role   | Status | Notes   |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| POD1       | CI/CD      | Daniel     | daniel.smith@ericsson.com     | CI: latest | Active | BM-CI   |
|            |            | Smith      |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| POD2       | CI/CD      | Daniel     | daniel.smith@ericsson.com     | CI: latest | Active | BM-CI   |
|            |            | Smith      |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| vPOD1      | CI/CD      | Fatih      | fatih.degirmenci@ericsson.com | CI: latest | Active | Virt-CI |
|            |            | Degirmenci |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| PHAROS-166 | FUEL       | Constant   | constant.wette@ericsson.com   | DR: B-rel  | Active | Nested  |
|            |            | Wette      |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| PHAROS-167 | OVSNFV     | Billy      | billy.omahoney@intel.com      | DR: C-rel  | Active | Hybrid  |
|            |            | O'Mahoney  |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| PHAROS-174 | GLUON      | Bin        | bh526r@att.com                | DR: D-rel  | Active | Nested* |
|            |            | Hu         |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| PHAROS-180 | SAVI       | Rick       | richard.brunner@ericsson.com  | DR: D-rel  | Active | Nested* |
|            |            |  Brunner   |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| PHAROS-181 | IPV6-MULTI | Bin        | bh526r@att.com                | DR: D-rel  | Active | Nested* |
|            |            |  Hu        |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| PHAROS-191 | AUTO-DEP   | Peter      | Peter.Barabas@ericsson.com    | DR: C-rel  | Active | Nested* |
|            |            |  Barabas   |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| PHAROS-199 | SDN-L3     | Tim        | Tim.Irnich@ericsson.com       | DR: C-rel  | Active | Nested* |
|            |            |  Irnich    |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| PHAROS-236 | LLT-TOOL   | Jose       | Jose.Lausuch@ericsson.com     | DR: C-rel  | Active | Nested* |
|            |            |  Lausuch   |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+
| PHAROS-253 | ODL-II     | Nikolas    | Nikolas.Hermanns@ericsson.com | DR: C-rel  | Active | Nested* |
|            |            |  Hermanns  |                               |            |        |         |
+------------+------------+------------+-------------------------------+------------+--------+---------+


- `ACTIVE CI/CD LAB SPECS <https://wiki.opnfv.org/pages/viewpage.action?pageId=6829012>`_
* `CI-ERICSSON-POD1 wiki page <https://wiki.opnfv.org/display/pharos/CI-ERICSSON-POD1>`_
* `CI-ERICSSON-POD1 wiki page <https://wiki.opnfv.org/display/pharos/CI-ERICSSON-POD2>`_
- `ACTIVE LAB SPECS <https://wiki.opnfv.org/display/pharos/Active+Lab+Specs>`_
* `PHAROS-166 wiki page <https://wiki.opnfv.org/display/pharos/PHAROS-166%3A+++++++PaaS+PoC>`_
* `PHAROS-167 wiki page <https://wiki.opnfv.org/display/pharos/PHAROS-167%3A+OVS-NFV+BareMetal+Lab>`_
* `PHAROS-174 wiki page <https://wiki.opnfv.org/display/pharos/PHAROS-174%3A+Gluon+PoC+for+OPNFV+Summit>`_
* `PHAROS-180 wiki page <https://wiki.opnfv.org/display/pharos/PHAROS-180%3A+++++++SAVI+CDN+POC>`_
* `PHAROS-181 wiki page <https://wiki.opnfv.org/display/pharos/PHAROS-181%3A+IPV6+Multisite>`_
* `PHAROS-191 wiki page <https://wiki.opnfv.org/display/pharos/PHAROS-191%3A+++++++Colorado+-+Autodeployer+Uplift>`_
* `PHAROS-199 wiki page <https://wiki.opnfv.org/display/pharos/PHAROS-199%3A+++++++ODL-L3+troubleshooting>`_
* `PHAROS-236 wiki page <https://wiki.opnfv.org/display/pharos/PHAROS-236%3A+Tracing+Tool+-+LLTng>`_
* `PHAROS-253 wiki page <https://wiki.opnfv.org/pages/viewpage.action?pageId=6828594>`_
- `Decommissioned Requets <https://wiki.opnfv.org/display/pharos/Decommissioned+Lab+Request>`_


Acceptable Usage Policy
-----------------------

Resources located in Ericsson OPNFV lab shall only be used for CI, infra setup/configuration and
troubleshooting purposes. No development work is allowed in these PODs. Development Work should
only be performed on the DR labs assigned to individual projects.


Remote Access Infrastructure
----------------------------

Ericsson OPNFV lab provides a SSH GW that allows for unlimited port-forwarding, as well as Remote
Desktop, VNC and SOCKS proxy capability allowing the end user to feel as though directly connected
to the lab.

Remote Access Procedure
-----------------------

Access to this environment can be granted by sending an e-mail to: **daniel.smith@ericsson.com**.

Subject: ericsson opnfv access.

The following information should be provided in the request:

::

    Full name:
    E-mail:
    Organization:
    Why is access needed:
    How long is access needed:
    Number of Hosts required:
    Topology Required (HA, SA):
    Feature/Plugins/Options Required (DPDK, ODL, ONOS):

Enclosed a copy of your id_rsa.pub (public key) with your request and a login will be created for you


Lab Documentation
-----------------


Lab Topology
------------

.. image:: ./images/ericsson_opnfv_topology.png
   :alt: Lab diagram not found

Each POD is an individual entity with its own set of independant networks allowing for
interconnection between DR labs, intra connectinos within multiple Nested DRs all without touching
the CI/CD running in production.

Refer to each Lab specific wiki page for IP and Login and Topology Information.

