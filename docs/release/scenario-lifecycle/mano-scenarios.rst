.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 OPNFV Ulrich Kleber (Huawei)


MANO Scenarios
---------------

Since OPNFV organizes all deployments using scenarios, also MANO components need
to be covered by scenarios.

On the other side all NFVI/VIM level scenarios need to be orchestrated using a
set of components from the NFVO and VNFM layer.

The idea here is therefore to specify for a MANO scenario:

* The MANO components to deploy
* A list of supported NFVI/VIM level scenarios that can be orchestrated
  using this MANO scenario.

The MANO test cases will define the VNFs to use.

MANO scenarios will have more work to do if they require new nodes to be deployed on.
They should include this aspect in their resource planning/requests and contact
Infra/Pharos in case that a change of the Pharos spec is needed and new PODs need
to be made available based on the amended spec.

More details need to be investigated as we gain experience with the MANO scenarios



