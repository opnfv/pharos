.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 OPNFV Ulrich Kleber (Huawei)


Generic Scenarios
------------------

Generic scenarios provide a stable environment for users who want to base their
products on them.

* Generic scenarios provide a basic combination of upstream components together
  with the superset of possible mature features that can be deployed on them.
* Generic scenarios should be supported by all installers.
* All generic scenarios in a release should have the same common major versions
  of the included upstream components.
  These upstream versions can then be seen as the upstream versions for the
  release. E.g. that way we can say: “OPNFV xxx contains OpenStack abc,
  ODL def, ONOS ghi, OVS jkl“.
  But most installers cannot directly reference any
  upstream version. This may lead to minor differences.
  Nevertheless features and test cases require all installers using the same
  major versions.
* Generic scenarios should use stable sources
  and lock the versions before the release by either pointing to a tag or sha1.
  According to the LF badging program it should be possible to reproduce
  the release from source again.
  Thus the upstream repos should be in safe locations.
  Also only tagged source versions should be used for the release, so the
  release can be reproduced identically for different purposes such as
  reproducing a baug reported by users and issuing the fix appropriately,
  even after the upstream project has applied patches.
  .. Editors note: There is discussion ongoing in INFRA and SEC working groups how
  .. to realize this. Thus the description is still a bit vague. Details will be
  .. added later either here or in some INFRA document.
* Generic scenarios should be stable and mature. Therefore they will be tested more
  thoroughly and run special release testing so a high level of stability can be
  provided.
* Generic scenarios will live through many OPNFV releases.
* More resources will be allocated to maintaining generic scenarios and they will
  have priority for CI resources.
  .. Editors note: Discussion ongoing in INFRA about toolchain issues.

Note: in some cases it might be difficult for an installer to support all generic
scenarios immediately. In this case an exception can be defined, but the installer
has to provide a plan how to achieve support for all generic scenarios.

Note: in some cases, upstream projects don‘t have proper CI process with
tagged stable versions. Also some installers‘ way of working doesn‘t allow
selecting the repo and tag. Thus a stepwise approach will be necessary to
fulfill this requirement.


