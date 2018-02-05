.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 OPNFV Ulrich Kleber (Huawei)


Scenario Descriptor Files
----------------------------

What are Scenario Descriptor Files?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every scenario is described in its own descriptor file.
The scenario descriptor file will be used by several parties:

* Installer tools will read from it the list of components to be installed
  and the configuration (e.g. deployment options and necessary details) to use.
* The dynamic CI process will read from it the prerequisites of the scenario
  to select the resource that has the needed capabilities for the deployment.
  It will also select the installer
  from the list of supported installers and the other deployment options as
  supported in their combination.

  The dynamic CI process will provide the installers with the deployment option
  to use for a particular deployment.

* The scenario owner needs to provide the descriptor file.

  When compiling it the scenario owner typically needs to work together with
  the installers, so the installers will support the required components and
  options.
* The testing framework can read from the scenario descriptor file necessary
  information to know which features can be tested on the scenario.
* The scenario descriptor file will also contain some maintenance information


Structure of the file
^^^^^^^^^^^^^^^^^^^^^^^^^^

The scenario descriptor file is a yaml file. The syntax will allow to specify
additional descriptor files, to make it better readable or structure common
configurations across multiple scenarios.

The file has following main sections:

* metadata (owner, history, description)
* list of components (names, versions, submodules)
* deployment options (HA/NOHA, hardware&virtualization, installers, including
  possible combinations and necessary details)
* other prerequisites (e.g. memory requirement more than pharos spec)
* list of features to be tested

More information to be provided in next version of this document. The file will
be defined based on the installer-specific files for scenario specification
used by the 4 installers in Danube release. Thus it will be made sure that the
information needed by the installers will be covered.

All scenario files will be stored in a central repo, e.g. Octopus. There will
also be a commented template to help create scenario descriptor files.


Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^

In Danube timeframe only Fuel installer has some metadata in the descriptor file.
The new template contains:

* Unique name

  This is a free name, there is a recommendation to take fish for names, matching
  OPNFV release naming with rivers.

* A free text title

  This should be a short descriptive text telling the main purpose

* A version number for the descriptor file

  Three digits, separated with dots, as used by Fuel in Danube

* Creation date
* Comment

  The file should contain a clear description of the purpose of the scenario,
  including the main benefits and major features.
  If applicable, the parent scenario should be mentioned.

* First OPNFV version to use the scenario
* Author/Owner

* A list of additional contact persons, e.g. from installers or major components

Components
^^^^^^^^^^^^^^^^

In this section all components are listed together with their version.
For some components in addtion submodules can be listed.

More details will be added.


Deployment options
^^^^^^^^^^^^^^^^^^^^^^^^^^

This section will list the supported deployment options. In each category at least
one option must be supported.

* hardware (cpu) types (intel or ARM)
* Virtualization (bare-metal or vPOD)
* availability (HA or NOHA)

  This subsection needs to specify also what does an HA deployment need, e.g.:

::

  availability:

    - type: HA
        nodes:
          - name: host1
            roles:
              - openstack-controller
              - odl
              - ceph-adm
              - ceph-mon
          - name: host2
            roles:
              - openstack-controller
              - odl
              - ceph-adm
              - ceph-mon
          - name: host3
            roles:
              - openstack-controller
              - odl
              - ceph-adm
              - ceph-mon
          - name: host4
              - openstack-compute
              - ceph-osd
          - name: host5
              - openstack-compute
              - ceph-osd
    - type: NOHA
        hosts:
          - name: host1
            roles:
              - openstack-controller
              - odl
              - ceph-adm
              - ceph-mon
          - name: host2
              - openstack-compute
              - ceph-osd
          - name: host3
              - openstack-compute
              - ceph-osd



* deployment tool (apex, compass, fuel, daisy, joid)

  In the section for each deployment tool, the combinations of the first three
  options have to be listed, e.g.:

::

  deployment-tools:

    - type: fuel
         cpu: intel
         pod: baremetal
         availability: HA
    - type: fuel
         cpu: intel
         pod: virtual
         availability: HA
    - type: fuel
         cpu: intel
         pod: virtual
         availability: NOHA

Please note that this allows easy definition of other availability options
including scaling and redundant configuration of SDN controllers.


Prerequisites
^^^^^^^^^^^^^^^^^^^^^^^^^^

This section will list additional prerequisites. Currently there is only
one case where a scenario has additional prerequisites to the Pharos spec.
E.g. a component could requires more RAM on the nodes than defined in
Pharos spec.
In general it should be preferred to issue such requirements to pharos
using the pharos change request process, but in some cases in might be
better to specify additional prerequisites.

Another use case for these prerequisites will be usage of specilized
hardware, e.g. for acceleration. This needs further study.

The section can be empty or omitted.


Testcases
^^^^^^^^^^^^^^^^

This section will provide information for functest and yardstick to decide
on the proper test cases for the scenario.

More details will be added.


Shared settings
^^^^^^^^^^^^^^^^

This descriptor file might get quite long and complex. Also some of the settings
will be shared between several scenarios, e.g. a long OpenStack module list.

Therefore it shall be possible to reference another file like a macro.
In that case all the file content is included in that place, e.g.:

::

  availability:

    - type: HA
        file: odl-ha-configuration.yaml


