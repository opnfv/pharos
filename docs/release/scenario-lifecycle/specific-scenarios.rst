.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 OPNFV Ulrich Kleber (Huawei)


Specific Scenarios
------------------

Specific scenarios are used for OPNFV development and help to isolate a path of development.

* Specific scenarios typically focus on a feature or topic.
* Specific scenarios allow to advance in development for their main feature without
  de-stabilizing other features.
* Specific scenarios provide additional flexibility in their handling to allow the
  development be agile.
* Specific scenarios can use new version of their main upstream component or even
  apply midstream patches during OPNFV deployment, i.e. the deployable artifact
  is created via cross community CI or even only in OPNFV and not upstream.
* Specific scenarios should have a limited life time. After a few releases, the feature
  development should have matured and the feature made available different configurations
  if possible. Typically the scenario then should be merged with other scenarios, best
  with generic scenarios.
* Normally specific scenarios will be released within the major OPNFV releases. But
  they don't need to fulfill maturity requirements (stable upstream versions and repos,
  stability testing), and can deviate in the used upstream versions.
* In exceptional cases we might release a specific scenario independently, in case there
  is a need. Thus specific scenarios provide a way to a more DevOps-like process.
* Specific scenarios will likely have a shorter support period after release as they are of
  interest to a smaller user community vs generic scenarios.
* They will be granted less CI resources than generic scenarios, e.g. for periodic
  CI jobs.
* We may need to prioritize resources post-release for maintenance / regression testing.


