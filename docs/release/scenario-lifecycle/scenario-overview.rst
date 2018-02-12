.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 OPNFV Ulrich Kleber (Huawei)


.. Scenario Lifecycle
.. ==========================================

Note: This document is still work in progress.

Overview
-------------

Problem Statement:
^^^^^^^^^^^^^^^^^^^

OPNFV provides the NFV reference platform in different variants, where
each variant is called a "scenario".

OPNFV introduces scenarios in order to provide a way to deploy the stack
using different combinations of upstream components, or to provide
different sets of pre-defined configuration options for these
components.

In some cases a scenario is introduced in order to provide isolation of
a specific development effort from other ongoing development efforts,
similar to the purpose of a branch in a code repository.

A certain amount of effort and resources is required in order to include
a scenario in a release. The number of scenarios has increased over
time, so it is necessary to identify ways to manage the number of
scenarios and to avoid that their number grows infinitely. To enable
this, we have to clearly define how to handle the lifecycle of
scenarios, i.e. how to create, how to terminate, etc.


Scenario types:
^^^^^^^^^^^^^^^^^^^
Some OPNFV scenarios have an experimental nature, since they introduce
new technologies or features that are not yet mature or well integrated
enough to provide a stable release. Nevertheless there also needs to be
a way to provide the user with the opportunity to try these new features
in an OPNFV release context.

Other scenarios are used to provide stable environments for users
desiring a certain combination of upstream components or interested in
particular capabilities or use cases.

The new OPNFV scenario lifecycle process proposed herein will support
this by defining two types of scenarios:

* **Generic scenarios** cover a stable set of common features provided
by different components and target long-term usage and maintenance of
the scenario. Only stable versions of upstream components are allowed to
be deployed in a generic scenario. Across all generic scenarios in a
given OPNFV release, the same version of a given upstream component
should be deployed. Creation of generic scenarios and promotion of
specific to generic scenario requires TSC approval, see section 5.
Generic scenarios will get priority over specific scenarios in terms of
maintenance effort and CI resources.

* **Specific scenarios** are needed during development to introduce new
upstream components or new features. They are typically derived from a
generic scenario and are intended to bring their features back into the
parent generic scenario once they are mature enough. It is also possible
that multiple specific scenarios are merged before bringing them back to
the parent scenario, for example in order to test and develop the
integration of two specific features in isolation. Specific scenarios
can consume unreleased upstream versions or apply midstream patches.
Creation of specific scenarios is not gated, but if a project intends to
release a specific scenario, it has to indicate that in its release plan
at milestone MS1. The scenario itself can be created at any time, by
means of a simple request by a PTL to the release manager.

OPNFV scenarios are deployed using one of the OPNFV installer tools.
Deploying a scenario will normally be supported by multiple installers.
The capabilities provided by the resulting deployments should be
identical. The set of tests to run and their results should be the same,
independent of the installer that had been used. Performance or other
behavioral aspects outside the scope of existing OPNFV tests could be
different.


Parent-child and sibling relations:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a developer decides to define a new scenario, he typically will
take one of the existing scenarios and do some changes, such as:

* add additional components
* change a deploy-time configuration
* use a component in a more experimental version or with midstream
patches applied

In this case the already existing scenario is called a "parent" and the
new scenario would be a "child".

Typically parent scenarios are generic scenarios, but it is possible to
derive from specific scenarios as well. it is expected that the child
scenario develops its additions over some time up to a sufficient
maturity, and then merges back to the parent. This way a continuous
evolution of the generic scenarios as well as a manageable overall
number of scenairos is ensured.

In some cases a child scenario will diverge from its parent in a way
that cannot easily be combined with the parent. Therefore, is is also
possible to "promote" a scenario from specific to generic. If this is
foreseeable upfront, the specific scenario can also be derived as a
sibling rather that child.

Promoting a scenario from specific to generic or creating a new generic
scenario requires TSC approval. This document defines a process for
this, see section 5.


Scenario deployment options:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many OPNFV scenarios can be deployed in different variants that do not
justify creation of separate scenarios. An example would be HA (high
availability) or non-HA configuration of otherwise identical scenarios.
HA configurations deploy some components according to a redundancy
model. Deployment options will also be used if the same scenario can be
deployed on multiple types of hardware, i.e. Intel and ARM.

In these cases multiple deployment options are defined for the same
scenario. The set of distinguishable deployment option types (e.g.
redundancy, processor architecture, etc.) will be pre-determined and
each scenario will have to define at least one option for each option
type.

It is emphasized that virtual deployments vs. bare-metal deployments are
intentionally not considered as deployment options. This should be a
transparent feature of the installer based on the same scenario
definition.

For generic scenarios, there are certain expectations on the set of
supported deployment options, e.g. a generic scenario should support at
least an HA deployment and preferably both HA and non-HA.


Scenario descriptor file:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every scenario will be described in a scenario descriptor yaml file.
This file shall contain all the necessary information for different users, such
as the installers (which components to deploy etc.),
the ci process (resource requirements in order to identify the right pod, machines, etc.).

The scenario descriptor file will also document which installer
can be used for a scenario and how the CI process can trigger automatic deployment
for a scenario via one of the supported installers.


MANO scenarios:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In early OPNFV releases, scenarios covered components of the infrastructure,
that is NFVI and VIM.
With the introduction of MANO, an additional dimension for scenarios is needed.
The same MANO components need to be used together with each of the infrastructure
scenarios. Thus MANO scenarios will define the MANO components and a list of
infrastructure scenarios to work with. Please note that MANO scenarios follow
the same lifecycle and rules for generic and specific scenarios like the
infrastructure scenarios.

