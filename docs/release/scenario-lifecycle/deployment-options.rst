.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 OPNFV Ulrich Kleber (Huawei)


Deployment Options
-------------------

What are deployment options?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Editors note: Some installers call it settings. Prefer options, because it allows
.. cases with multiple options.

During the analysis of scenario definitions in Colorado and Danube releases, it became
visible, that HA and NOHA deployment of otherwise identical scenarios shouldn't be
called different scenarios.

This understanding leads to the definition of another kind of attributes
in scenario definitions. Many scenarios can be deployed in different ways:

* **HA** configuration of OpenStack modules (that is redundancy using multiple
  controllers running OpenStack services) versus NOHA with only a single controller
  running a single instance of each OpenStack service
* Some scenarios can be deployed on intel and on ARM **hardware**.
* We can see the **installation tools** in the same way. Independent of the installer
  that was used for the deployment of a scenario, the same functionality will be
  provided and we can run the same testcases.

Please note that a scenario can support multiple deployment options. And a scenario
definition must specify at least one option of each type.

In future there will be more deployment options, e.g. redundancy models or other
clustering options of SDN controllers, or upscaling compute or control nodes.

CI Pipeline needs to test all configuration options of a scenario.

* Development cycles (verify-jobs, daily, weekly) don‘t need to run all
  options each time
* Release testing must cover all those combinations of configuration options that
  will be part of the release. Typically the HA configurations are released on
  bare metal with the allowed hardware options and all installers that can deploy
  those. Release of an NOHA option should be an exception, e.g. for a scenarios
  that are not mature yet.
* Virtual deployments are not mentioned here. All scenarios should allow virtual
  deployment where applicable.
  But in release testing, bare metal deployment will be necessary.
  CI will use virtual deployments as much as appropriate for resource reasons.


Deployment options or new scenarios
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In general we can say that a different scenario is needed when the set of components
is changed (or in some cases a general deploy-time configuration of a component). If
we deploy the same components in a different way, we can define this via deployment
options.

**Examples**

* Deploying different SDN controller or data plane (OVS/FD.IO) requires different
  scenario.
* HA/NOHA will deploy the same components on different number of nodes, so it is a
  deployment option.
* Different hardware types should not lead to new scenarios. Typically the same
  scenario can be deployed on multiple hardware.


HA and NOHA
^^^^^^^^^^^^^

Both, HA and NOHA options of a scenario are important.

* HA deployment is important to be released in major OPNFV releases, because
  telco deployments typically have strong requirements on availability.
* NOHA deployments require less resources and are sufficient for many use cases.
  For instance sandbox testing can be done easier and also automatic verification
  in the CI pipeline can make use of it.
* Generic scenarios shall support the HA and NOHA option.
* Specific scenarios can focus on the NOHA option if their features are independent
  from the controller redundancy. But before merging with generic scenarios, they
  should provide both options.


Hardware types
^^^^^^^^^^^^^^^^^

In its first releases, OPNFV could be deployed on Intel hardware only. Later, support
for ARM hardware was added and now 5 scenarios can already be deployed on both.


Virtual deployment
^^^^^^^^^^^^^^^^^^^^^^

Many, but not all scenarios can be deployed on virtual PODs. Therefore the scenario
definition shall specify whether virtual deployment is possible.

Typically a virtual HA deployment shall look very much the same as a bare-metal HA
deployment, that is the distribution of modules on nodes/VMs is similar. But there
might be cases where there are differences. Thus, the scenario specification needs
to provide the data for each separately.


Deployment tools
^^^^^^^^^^^^^^^^^^^

Deployment tools (installers) are in a very similar relation to the scenarios.
Each scenario can be deployed by one or more installer. Thus we can specify the
installers for a scenario as a deployment option.

However, the installers need additional detailed information for the deployment.
Every installer may not support the same HA, hardware, virtualization options,
or same distribution of modules. Each deployment may look slightly different
per installer.

The scenario definition needs to provide such information in a way it can be easily
consumed by the installers.



Other deployment options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This set of deployment options is based on what is required by Danube scenarios.
Future releases will most likely introduce additional deployment options.



