.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

.. Top level of Pharos templates and configuration files

****************************************
Pharos Templates and Configuration Files
****************************************

Lab and POD templates are provided to help lab owners document capabilities, configurations and
network topologies. Compute, network and storage specifications with network topology details are
required to help developers use lab resources efficiently while minimizing support needs. This also
greatly assists with troubleshoting. It is the responsibility of the lab owner to keep individual
lab documents updated and determine appropriate level of detail that is exposed publicly through
the Wiki or maintained in a secure Pharos repo
`securedlab <https://gerrit.opnfv.org/gerrit/#/admin/projects/securedlab>`_ with controlled access.
To avoid deplicated content, it is suggested to directly include the rst docs in the wiki.

Before Danube release, securedlab is only opened for Infra WG committers and installer projects's
contributors.  Since Euphrates release, it is opened for all the contributors of Pharos project, if
you are the owner of a community lab, please ask helpdesk to become a Pharos contributor in order
to submit your PDF to the securedlab repo.

The goal of the Pharos Project is automation of resource provisioning. This requires machine
readable inventory and network configuration files that follow common format.


.. toctree::
   :maxdepth: 2

   ./lab_description.rst
   ./pod_description.rst
   ./pdf.rst
