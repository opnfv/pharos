.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

***************
Lab Setup Guide
***************

Provides an overview for setting up a Pharos lab. A full set of
:ref:`pharos_master` documents are maintained in the *pharos* repo.

When setting up an OPNFV community lab ...

* Provide the Pharos community with details of the intended setup, including ...

  * Overview of resources are being offered to the community, intended purpose and known
    limitations
  * Lab owner name with contacts
  * Timelines for availablity for development, test, release production, ...

* Update the Pharos Wiki with lab details

  * Lab map, organization, contacts, status, location, resources, role, etc.
  * `Community labs <https://wiki.opnfv.org/display/pharos#PharosHome-Overview>`_
  * :ref:`pharos_wiki`

* Update the Pharos project information file "Current Labs"

  * :ref:`pharos_information`

* Submit a patch using Pharos template for lab( :ref:`pharos_lab`) and POD( :ref:`pharos_pod`)
  specific information in gerrit

  * Access procedures
  * Usage guidelines for developers
  * Update infomtation as PODs are re-assigned or usage/availability changes

* Create new Wiki pages and include the lab and POD content in the
  `pharos git <https://git.opnfv.org/pharos/>`_

* Connect PODs to Jenkins/CI

* Note: if the POD will be used for dynamical deployment with community installers, some security
  sensitive lab information should be stored in the secure Pharos repo :ref:`securedlab`

