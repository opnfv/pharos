.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 OPNFV Ulrich Kleber (Huawei)


Creating Scenarios
--------------------

General
^^^^^^^^^

A new scenario needs to be created, when a new combination of upstream
components or features shall be supported, that cannot be provided with the
existing scenarios in parallel to their existing features.

Typically new scenarios are created as children of existing scenarios.
They start as specific scenario and as they mature, they either merge back
their features to the parent or promote to a generic scenario.

Scenario Owners
^^^^^^^^^^^^^^^^

Each scenario must have an "owner". Scenario owners have the following responsibilities:

* The scenario owner is responsible for the contents and usage of the scenario.
* He shall define the contents for the scenario deployment:

  * The components and their versions that need to be deployed
  * Options for the deployment of such components, e.g. settings, optional features, ..
  * Which installers to use
  * Deployment options (HA, NOHA, hardware types, ..)

* He shall define the usage of the scenario in the development process:

  * Initiate integration to CI
  * Define which testcases to run
  * Applies that the scenario joins a release

* The owner maintains the Scenario Descriptor File (SDF)
* Drives for the scenario be supported by more installers

The scenario owner of a specific scenario typically comes from the feature project
that develops the features introduced by the scenario.

The scenario owner of a generic scenario will need to drive more integration tasks than
feature development. Thus he typically will come from a project with a broader scope
than a single feature, e.g. a testing project.
The scenario owner of a generic scenario needs to cover issues of all installers, so
only in exceptional cases he will come from an installer project.

Creating Generic Scenarios
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generic scenarios provide stable and mature deployments of an OPNFV release. Therefore
it is important to have generic scenarios in place that provide the main capabilities
needed for NFV environments. On the other hand the number of generic scenarios needs
to be limited because of resources.

* Creation of a new generic scenario needs TSC consensus.
* Typically the generic scenario is created by promoting an existing specific
  scenario. Thus the only the additional information needs to be provided.
* The scenario owner needs to verify that the scenario fulfills the above requirements.
* Since specific scenarios typically are owned by the project who have initiated it,
  and generic scenarios provide a much broader set of features, in many cases a
  change of owner is appropriate. In most cases it will be appropriate to assign
  a testing expert as scenario owner.

Creating Specific Scenarios
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As already stated, typically specific scenarios are created as children of existing
scenarios. The parent can be a generic or a specific scenario.

Creation of specific scenarios shall be very easy and can be done any time. However,
support might be low priority during a final release preparation, e.g. after a MS6.

* The PTL of the project developing the feature(s) or integrating a component etc can
  request the scenario (tbd from whom: CI or release manager, no need for TSC)
* The PTL shall provide some justification why a new scenario is needed.
  It will be approptiate to discuss that justification in the weekly technical
  discussion meeting.
* The PTL should have prepared that by finding support from one of the installers.
* The PTL should explain from which "parent scenario" (see below) the work will start,
  and what are the planned additions.
* The PTL shall assign a unique name. Naming rules will be set by TSC.
* The PTL shall provide some time schedule plans when the scenario wants to join
  a release, when he expects the scenario merge to other scenarios, and he expects
  the features may be made available in generic scenarios.
  A scenario can join a release at the MS0 after its creation.
* The PTL should explain the infrastructure requirements and clarify that sufficient
  resources are available for the scenario.
* The PTL shall assign a scenario owner.
* The scenario owner shall maintain the scenario descriptor file according to the
  template.
* The scenario owner shall drive the necessary discussions with installers and testing
  teams to get their support.
* In case the scenario needs new keywords in the SDF, the scenario owner shall discuss
  those with the installer teams and CI.
* The scenario owner shall initiate the scenario be integrated in CI and 
  participate in releases.
* When the scenario joins a release this needs to be done in time for the relevant
  milestones.


