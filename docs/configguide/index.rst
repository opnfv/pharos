.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

.. Top level of Pharos configuration documents.

********************
Pharos Configuration
********************

OPNFV development, test and production activities rely on Pharos resources and support from the
Pharos community. Lab owners and Pharos project committers/contributors will evolve the vision for
Pharos as well as expand lab capabilities that are needed to help OPNFV be highly successful.

Pharos configuration documents provide information on how to setup hardware and networks in a
Pharos compliant lab. Jira is used to track Pharos activities including lab operations. Lab
resources can be used for and declared as either *Development (bare-metal or virtual)* or
*Production/CI (bare-metal or virtual)*. If a resource is used for and declared as *Development*
resource, it can not be used for and declared as *Production/CI* resource at the same time and vice
versa. Changing the resource declation must be brought in to Infra WG. Production/CI PODs are
required to be connected to OPNFV Jenkins and available on a 24/7 basis other than scheduled
maintenance and troubleshooting. Jenkins slave status can be seen on `Jenkins dashboard
https://build.opnfv.org/ci/computer/`.

.. toctree::
   :maxdepth: 2

   ./configguide.rst
   ./lab_update_guide.rst
   ./jumpserverinstall.rst
