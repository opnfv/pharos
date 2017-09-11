.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.


.. _pharos_wiki:

*************************
Updating Pharos Documents
*************************

Details about each Community Lab is found in 3 places:

 - Summary of lab including location, contacts, status, etc.
   on the `Pharos Project Wiki page <https://wiki.opnfv.org/display/pharos>`_
 - Lab specific details are provided with dedicated Wiki pages,
   see this `Example Lab <https://wiki.opnfv.org/display/pharos/Intel+Hosting>`_
 - Pharos repo docs ...

.. code: bash

    ├── development ... for pharos developer
    │   ├── design
    │   ├── overview
    │   └── requirement
    ├── index.rst
    └── release ... release documents
        ├── configguide
        │   ├── configguide.rst
        │   ├── jumpserverinstall.rst
        │   └── lab_update_guide.rst
        ├── images
        ├── information
        │   └── pharos.rst  ... project information file
        ├── release-notes
        │   ├── lab-description
        │   │   ├── inventory.rst
        │   │   ├── lab_description.rst
        │   │   └── pod_description.rst
        │   ├── labs ... lab specific documents
        │   ├── platformoverview
        │   │   └── labinfrastructure.rst
        │   └── specification
        │       ├── hardwarespec.rst
        │       ├── networkconfig.rst
        │       ├── objectives.rst
        │       └── remoteaccess.rst
        └── userguide
            ├── documentation-example.rst

Update Pharos repo
------------------

Clone the Pharos Git repository

 * git clone https://gerrit.opnfv.org/gerrit/pharos
 * Make the changes to Pharos project information file (docs/release/information/pharos.rst)
 * Submit changes for review
 * After code gets merged http://artifacts.opnfv.org/pharos/docs/release/information/pharos.html
   will contain your change


Update Pharos Wiki
------------------

Edit Wiki page

 * https://wiki.opnfv.org/pharos
 * Look for {{scrape>http://artifacts.opnfv.org/pharos/docs/release/information/pharos.html}}
 * Click "Preview" and see if your change is shown; if shown add a short "Edit summary" and click
   "Save" (Wiki does not auto update content)

You will see a section of code as shown below. Add your page to the bullet list with wiki link, nice
name, and location summary

Update the map info on the Pharos Project Page https://wiki.opnfv.org/display/pharos/Community+Labs

 * You will see a section of code as shown below. Add your lab infomation to the list with a comma
   separated list as follows:

    * Location
    * Contact
    * POD/vPOD
    * Role

