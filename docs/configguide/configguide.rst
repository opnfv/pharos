.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.


==============================
Pharos Lab Configuration Guide
==============================

This section provides an overview for Pharos lab setup and operation. The tasks and expectations for configuring a
Pharos compliant lab are explained along with reference to relavant Pharos documents.

Overview of Community Lab Expectations
--------------------------------------

* Designated lab owners and project committers participate in the Pharos community (discussions, meetings, ...)
* Jira is used to track activities including lab operations (requests and support)
* Production resources are connected to Jenkins and available 24/7 (other than scheduled maintenance and troubleshooting)
* Lab resources are declared as either:

  * Development (bare-metal or virtual)
  * Production - latest (bare-metal)
  * Production - stable (bare-metal)

On-boarding Steps
-----------------

* Provide Pharos community with details of intended setup, including ...

  * Resources being offered
  * Lab owner name / contacts
  * Timelines for availablity for development and use in upcomming releases

* Update Pharos Wiki
  * Lab with location, owner

* Create and fill *New Lab* Wiki pages

  * Access policies
  * Usage guidelines for developers
  * Fill Lab and POD templates
  * POD allocations (updated as PODs are assigned or revoked)
  * Lab documentation with security sensitive infomation can be stored in the Pharos secure repo (will be available soon)

* Network Information
* Update Pharos infomation file i.e. pharos.rst
* labupdateguide.rst ... how to update Pharos Wiki start page; how to update map info
* Connect to CI

Jump Server Install
-------------------

* jumpserverinstall.rst

Lab Documentation
-----------------

* Pharos Wiki page
* Map Info



Revision: _sha1_

Build date: |today|
