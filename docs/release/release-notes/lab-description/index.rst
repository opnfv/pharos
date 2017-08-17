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
the Wiki or maintained in a secure Pharos repo with controlled access.

The goal of the Pharos Project is automation of resource provisioning. This requires machine
readable inventory and network configuration files that follow common format.


.. toctree::
   :maxdepth: 2

   ./lab_description.rst
   ./pod_description.rst
   ./inventory.rst
