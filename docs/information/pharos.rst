.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

.. OPNFV Pharos Project Information file.

.. _pharos_information:

**************************
Pharos Project Information
**************************

Introduction
------------

The `Pharos Project <https://www.opnfv.org/developers/pharos>`_ deals with developing an OPNFV lab infrastructure that is geographically and technically diverse.
This will greatly assist in developing a highly robust and stable OPNFV platform. Community labs are hosted by
individual companies and there is also an OPNFV lab hosted by the Linux Foundation that has controlled access for key
development and production activities. The **Pharos Specification** defines a "compliant" deployment and test
environment. Pharos is responsible for defining lab capabilities, developing management/usage policies and process;
and a support plan for reliable access to project and release resources. Community labs are provided as a service by
companies and are not controlled by Pharos however our goal is to provide easy visibility of all lab capabilities
and their usage at all-times.

A requirement of Pharos labs is to provide *bare-metal* for development, deployment and testing. This is resource
intensive from a hardware and support perspective while providing remote access can also be very challenging due to
corporate IT policies. Achieving a consistent *look and feel* of a federated lab infrastructure continues to be an
objective. Virtual environments are also useful and provided by some labs. Jira is currently used for tracking lab
operational issues as well as for Pharos project activities.

Future lab capabilities are currently focussed on 1) Deployment automation 2) Dashboards (for capability and usage)
3) *Virtual Labs* for developer on-boarding.

* Pharos page: https://www.opnfv.org/developers/pharos
* Pharos project Wiki: https://wiki.opnfv.org/pharos
* `Pharos Planning <https://wiki.opnfv.org/pharos_rls_b_plan>`_

Project Communication
---------------------

* `Jira <https://jira.opnfv.org/projects/PHAROS/summary>`_
* `Weekly Pharos meeting <https://wiki.opnfv.org/meetings#pharos_meetings>`_
* `Weekly coordination meeting for Test related projects <https://wiki.opnfv.org/meetings/test>`_
* IRC: freenode.net #opnfv-pharos http://webchat.freenode.net/?channels=opnfv-pharos
* Mailing List: use opnfv-tech-discuss and tag your emails with [Pharos] in the subject for filtering

Project Release Artifacts
-------------------------

* Project Repository: https://gerrit.opnfv.org/gerrit/#/q/pharos
* Continuous Integration https://build.opnfv.org/ci/view/pharos/
* Documentation: http://artifacts.opnfv.org/pharos/docs/

Pharos Lab Process
------------------

* Process for requesting lab access and support https://wiki.opnfv.org/pharos_rls_b_support
* Pharos Lab Governance and Policies https://wiki.opnfv.org/pharos_policies
* Status of Community labs https://wiki.opnfv.org/pharos_rls_b_labs

Current Labs
------------

An interactive map of OPNFV lab locations, lab owners and other lab information is maintained on the `Pharos Wiki
<https://wiki.opnfv.org/pharos#community_labs>`_

+----+---------------+----------------------------------------------------------+----------------------+
|    | **Hosted by** |  **Home page**                                           | **Location**         |
| #  |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 1  | Linux         | https://wiki.opnfv.org/get_started/lflab_hosting         | Portland, Oregon     |
|    |  Foundation   |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 2  | Spirent       | https://wiki.opnfv.org/pharos/spirentvctlab              | Nephoscale, CA       |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 3  | China Mobile  | https://wiki.opnfv.org/lab2_chinamobile_hosting          | Beijing, China       |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 4  | Dell          | https://wiki.opnfv.org/dell_hosting                      | Santa Clara, CA      |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 5  | Enea          | https://wiki.opnfv.org/enea-pharos-lab                   | Kista, Sweden        |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 6  | Ericsson      | https://wiki.opnfv.org/get_started/ericsson_hosting      | Montreal, Canada     |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 7  | Huawei        | https://wiki.opnfv.org/lab4_huawei                       | Xi an, China         |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 8  | Huawei        | https://wiki.opnfv.org/get_started/huawei_sc_hosting     | Santa Clara, CA      |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 9  | Intel         | https://wiki.opnfv.org/get_started/intel_hosting         | Hillsboro, Oregon    |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 10 | Orange        | https://wiki.opnfv.org/opnfv-orange                      | Lannion, France      |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 11 | Orange        | https://wiki.opnfv.org/opnfv-orange                      | Paris, France        |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+
| 12 | ZTE           | https://wiki.opnfv.org/zte-nj-testlab                    | Nan Jing, China      |
|    |               |                                                          |                      |
+----+---------------+----------------------------------------------------------+----------------------+


Pharos project Key Facts
------------------------

**Key Project Facts are maintained in the Pharos INFO file in teh project repo**

.. Should reference Project Fact File using ".. include:: ../../INFO" but this does not work as out of docs tree,
.. currently limitation of the docs-build script. Planned to be resolved for Rls C. This is a copy of the INFO
.. file and will be removed once include directive works.
.. NOTE: UPDATE THE INFO FILE IF ANY CHANGES ARE MADE TO PROJECT FACTS IN THIS DOCUMENT

- Project: Testbed infrastructure (Pharos)
- Project Creation Date:  January 8, 2015
- Project Category:  Integration & Testing
- Lifecycle State:  Mature
- Primary Contact:  Trevor  <trevor.cooper@intel.com>
- Project Lead:  Trevor  <trevor.cooper@intel.com>
- Jira Project Name:  Testbed infrastructure Project
- Jira Project Prefix:  PHAROS
- Mailing list tag: [pharos]
- IRC: Server:freenode.net Channel:#opnfv-pharos
- Repository: pharos

- Committers:

  - Trevor Cooper<trevor.cooper@intel.com>
  - Fu Qiao <fuqiao@chinamobile.com>
  - Sheng-ann Yu <sheng-ann.yu@ericsson.com>
  - Wenjing Chu <Wenjing_Chu@DELL.com>
  - Chris Donley <C.Donley@cablelabs.com>
  - Morgan Richomme <morgan.richomme@orange.com>
  - Erica Johnson <erica.johnson@iol.unh.edu>
  - Hui Deng <denghui@chinamobile.com>
  - Prabu Kuppuswamy <prabu.kuppuswamy@spirent.com>
  - Sean Chen <s.chen@huawei.com>
  - Saikrishna M Kotha <saikrishna.kotha@xilinx.com>
  - Eugene Yu <yuyijun@huawei.com>
