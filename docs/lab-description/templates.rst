.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

.. Top level of Pharos templates and configuration files

****************************************
Pharos Templates and Configuration Files
****************************************

Lab and POD templates are provided to help lab owners document capabilities, configurations and network topologies.
Compute, network and storage specifications with network topology details are required to help developers use lab
resources efficiently while minimizing support needs. This also greatly assists with troubleshhoting. It is the
responsibility of the lab owner to keep individual lab documents updated and determine appropriate level of detail
that is exposed publically through the Wiki or maintained in a secure Pharos repo with controlled access.

While human readable configuration files are needed, the goal is for full automation of deployments. This requires
a common machine readable format for POD configurations as input to every installer. This is the "POD inventory"
common format file.


.. toctree::

   ./lab_description.rst
   ./pod_description.rst
   ./inventory.rst
