.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

**********************
Lab: OOL OPNFV Testbed
**********************

Introduction
------------

`Okinawa Open Laboratory (OOL)`_ provides the following facilities for OPNFV
testing. The testlab is now located only at Okinwa in Japan.

.. _Okinawa Open Laboratory (OOL): http://www.okinawaopenlabs.org/en/

Lab Resources
-------------

+--------------+--------------+-----------------+----------------------+-----------+-----------+-------+
| POD Name     | Project(s)   | Project Lead(s) | Email(s)             |  POD Role |  Status   | Notes |
+--------------+--------------+-----------------+----------------------+-----------+-----------+-------+
| `ool-pod1`_  |              |                 |                      | CI stable | Available |       |
+--------------+--------------+-----------------+----------------------+-----------+-----------+-------+
| ool-virtual1 | Doctor       | Ryota Mibu      | r-mibu@cq.jp.nec.com | CI review | Assigned  |       |
+--------------+--------------+-----------------+----------------------+-----------+-----------+-------+

.. _ool-pod1: https://build.opnfv.org/ci/computer/ool-pod1/

Acceptable Usage Policy
-----------------------

These resources provided to OPNFV are free to use by any OPNFV contributor or
committer for the purpose of OPNFV approved activities by permission of the
operator, but shall be used for CI, infra setup/configuration and
troubleshooting purposes.

Remote Access Infrastructure
----------------------------

OOL provide VPN(OpenVPN) to connect this testlab.

Remote Access Procedure
-----------------------

Access to this environment can be granted by sending a e-mail to: TBD

subject: opnfv_access_ool

Following information should be provided in the request:

* Full name
* e-mail
* Phone
* Organization
* Resources required
* How long is access needed
* PGP public key
* SSH public key

Granting access normally takes 2-3 business days.

Detailed access descriptions will be provided with your access grant e-mail.

Lab Documentation
-----------------

Lab Topology
------------

.. image:: images/ool-testlab.png
   :alt: not found
