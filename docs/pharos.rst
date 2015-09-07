Project: Testbed infrastructure (Pharos)
#########################################


The Pharos project deals with the creation of a distributed and federated NFV test capability that will be hosted by a number of companies in the OPNFV community. The goals consist in managing the list of community platforms, describing the different community platforms, offering timeslots and tools to perform tests, sharing the results and the best practices, supporting any test campaigns of the projects of the community (e.g. [[opnfv_functional_testing | functional testing project]], [[platform_performance_benchmarking|Qtip]], [[get_started|BGS]], [[oscar/project_proposal|oscar]],...). Pharos shall provide the infrastructure and the tooling needed by the different projects.


.. image:: images/opnfv-test.jpg

Community Test Labs
--------------------

A summary of all Community Hosted OPNFV test labs (existing and planned) is also kept on the `wiki home page <https://wiki.opnfv.org/start#opnfv_community_labs>`. This section here contains additional details and project relationship mappings.  //NOTE: Please follow `these instructions <https://wiki.opnfv.org/lab_update_guide>` when updating this list.//

+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| Map       | Hosting       |  Home page                                           | Contact person                              | Comments                            | Location             |
|  Position |  Organization |                                                      |                                             |                                     |                      |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 1         | Spirent       | https://wiki.opnfv.org/pharos/spirentvctlab          | Iben Rodriguez                              | OpenDaylight, NFV, SDN, &           | Nephoscale           |
|           |               |                                                      |      iben.rodriguez@spirent.com             | OpenStack testing in progress       | San Jose, CA         |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 2         | China Mobile  |                                                      | Fu Qiao                                     | PODs dedicated for BGS and          | Beijing, China       |
|           |               |                                                      |      fuqiao@chinamobile.com                 | Functest                            |                      |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 3         | Ericsson      | https://wiki.opnfv.org/get_started/ericsson_hosting  | Jonas Bjurel                                |                                     | Montreal, Canada     |
|           |               |                                                      |         jonas.bjurel@ericsson.com           |                                     |                      |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 4         | Huawei        |                                                      | Radoaca Vasile                              | TBD                                 | Xi an, China         |
|           |               |                                                      |         radoaca.vasile@huawei.com           |                                     |                      |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 5         | Intel         | https://wiki.opnfv.org/get_started/intel_hosting     | Trevor Cooper                               | Operational with PODs dedicated to  | Intel Labs; Hillsboro|
|           |               |                                                      |         trevor.cooper@intel.com             | BGS and vSwitch projects            | Oregon               |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 6         | Orange        |                                                      | Morgan Richomme                             | Available Q1 2015                   | Orange Labs;         |
|           |               |                                                      |         morgan.richomme@orange.com          |                                     | Lannion, France      |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 7         | Cable Labs    |                                                      |                                             | TBD                                 |                      |
|           |               |                                                      |                                             |                                     |                      |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 8         | Dell          |                                                      | Wenjing Chu                                 | TBD                                 | Santa Clara, CA      |
|           |               |                                                      |         Wenjing_Chu@DELL.com                |                                     |                      |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 9         | Huawei        |                                                      | Sean Chen                                   | TBD                                 | Santa Clara, CA      |
|           |               |                                                      |                                             |                                     |                      |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+
| 10        | ZTE           |                                                      | Zhihui Wu                                   | BGS  Parser  Yardstick              | Nan jing, China      |
|           |               |                                                      |         wu.zhihui1@zte.com.cn               |                                     |                      |
+-----------+---------------+------------------------------------------------------+---------------------------------------------+-------------------------------------+----------------------+



Pharos management
------------------

- `Project proposal <https://wiki.opnfv.org/opnfv_testbed_infrastructure>`_
- A "Pharos compliant" environment is the `standard configuration of a deployed system <https://wiki.opnfv.org/pharos/pharos_specification>`_ for test purposes
- `Testing <https://wiki.opnfv.org/pharos_testing>`_ on "Pharos compliant" environment
- `Project draft release <https://wiki.opnfv.org/pharos_draft_release>`_
- `Task follow-up <https://wiki.opnfv.org/pharos_tasks>`_
- `FAQ <https://wiki.opnfv.org/pharos_faq>`_
- `meeting & minutes page] <https://wiki.opnfv.org/wiki/test_and_performance_meetings>`_ <- this page needs to be moved and renamed

Pharos project - Key facts
---------------------------

- Project Creation Date:  January 8, 2015
- Project Category:  Integration & Testing
- Lifecycle State:  Incubation
- Primary Contact:  Trevor  <trevor.cooper@intel.com>
- Project Lead:  Trevor  <trevor.cooper@intel.com>
- Jira Project Name:  Testbed infrastructure Project
- Jira Project Prefix:  PHAROS
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

- Contributors:

  - Iben Rodriguez <iben.rodriguez@spirent.com>


- IRC : freenode.net #opnfv-pharos `http://webchat.freenode.net/?channels=opnfv-pharos <http://webchat.freenode.net/?channels=opnfv-pharos>`_
- Mailing List : no dedicated mailing list - use opnfv-tech-discuss and tag your emails with [Pharos] in the subject for easier filtering
- Meetings :

  - `meetings <https://wiki.opnfv.org/wiki/test_and_performance_meetings>`_

- Repository:  pharos

**Documentation tracking**

Revision: _sha1_

Build date:  _date_


