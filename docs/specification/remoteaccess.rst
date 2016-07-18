.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.


Remote Management
------------------

Remote access is required for …

  * Developers to access deploy/test environments (credentials to be issued per POD / user)
  * Connection of each environment to Jenkins master hosted by Linux Foundation for automated
    deployment and test

OpenVPN is generally used for remote however community hosted labs may vary due to company security
rules. For POD access rules / restrictions refer to individual lab documentation as each company may
have different access rules and acceptable usage policies.

Basic requirements:

  * SSH sessions to be established (initially on the jump server)
  * Packages to be installed on a system (tools or applications) by pullig from an external repo.

Firewall rules accomodate:

  * SSH sessions
  * Jenkins sessions

Lights-out management network requirements:

  * Out-of-band management for power on/off/reset and bare-metal provisioning
  * Access to server is through a lights-out-management tool and/or a serial console
  * Refer to applicable light-out mangement information from server manufacturer, such as ...

    * Intel lights-out
      `RMM <http://www.intel.com/content/www/us/en/server-management/intel-remote-management-module.html>`_
    * HP lights-out `ILO <http://www8.hp.com/us/en/products/servers/ilo/index.html>`_
    * CISCO lights-out `UCS <https://developer.cisco.com/site/ucs-dev-center/index.gsp>`_

Linux Foundation Lab is a UCS-M hardware environment with controlled access *as needed*

    * `Access rules and procedure <https://wiki.opnfv.org/display/pharos/Lflab+Hosting>`_ are
      maintained on the Wiki
    * `A list of people <https://wiki.opnfv.org/display/pharos/Lf+Support>`_ with access is
      maintained on the Wiki
    * Send access requests to infra-steering@lists.opnfv.org with the
      following information ...

      * Name:
      * Company:
      * Approved Project:
      * Project role:
      * Why is access needed:
      * How long is access needed (either a specified time period or define "done"):
      * What specific POD/machines will be accessed:
      * What support is needed from LF admins and LF community support team:

    * Once access is approved please follow instructions for setting up VPN access ...
      https://wiki.opnfv.org/get_started/lflab_hosting
    * The people who require VPN access must have a valid PGP key bearing a valid signature from LF
    * When issuing OpenVPN credentials, LF will be sending TLS certificates and 2-factor
      authentication tokens, encrypted to each recipient's PGP key

