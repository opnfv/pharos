.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

***************
Lab Setup Guide
***************

Provides an overview for setting up a Pharos lab. A full set of
:ref:`pharos_master` documents are maintained in the *pharos* repo.

Contributing to the Pharos Community
------------------------------------

The development, test and production activities rely on Pharos resources and support from the Pharos community. Lab
owners and Pharos project committers/contributors will evolve the vision for Pharos as well as expand lab capabilities
that are needed to help OPNFV be highly successful.

* Jira is used to track Pharos activities including lab operations
* PODs are connected to Jenkins and generally available 24/7 other than scheduled maintenance and troubleshooting
* Lab resources are declared as either for *Development (bare-metal or virtual)*, *Production latest (bare-metal)* or *Production stable (bare-metal)*

Declaring a Pharos Lab
----------------------

* Provide the Pharos community with details of the intended setup, including ...

  * Overview of resources are being offered to the community, intended purpose and known limitations
  * Lab owner name with contacts
  * Timelines for availablity for development, test, release production, ...

* Update the Pharos Wiki with lab details

  * Lab map, organization, contacts, status, location, resources, role, etc.
  * https://wiki.opnfv.org/pharos#community_labs
  * :ref:`pharos_wiki`

* Update the Pharos project information file "Current Labs"

  * :ref:`pharos_information`

* Create new Wiki pages for lab and POD specific information

  * Access procedures
  * Usage guidelines for developers
  * Update infomtation as PODs are re-assigned or usage/availability changes

* Fill Lab and POD templates ... :ref:`pharos_lab` ... :ref:`pharos_pod`

  * Note that security sensitive lab information should be stored in the secure Pharos repo

* Connect PODs to Jenkins/CI
