Remote management
------------------

**Remote access**

Remote access is required for …

  1. Developers to access deploy/test environments (credentials to be issued per POD / user)
  2. Connection of each environment to Jenkins master hosted by Linux Foundation for automated deployment and test

OpenVPN is generally used for remote however community hosted labs may vary due to company security rules
POD access rules / restrictions …

  - Refer to individual test-bed as each company may have different access rules and acceptable usage policies

The Basic requirement is for SSH sessions to be established (initially on jump server)
and a majority of packages installed on a system (tools or applications) will be pulled from an external repo.

Firewall rules should include

  - SSH sessions
  - Jenkins sessions

Lights-out Management:

  - Out-of-band management for power on/off/reset and bare-metal provisioning
  - Access to server is through lights-out-management tool and/or a serial console
  - Intel lights-out ⇒ RMM <http://www.intel.com/content/www/us/en/server-management/intel-remote-management-module.html>_
  - HP lights-out ⇒ ILO <http://www8.hp.com/us/en/products/servers/ilo/index.html>_
  - CISCO lights-out ⇒ UCS <https://developer.cisco.com/site/ucs-dev-center/index.gsp>_

Linux Foundation - VPN service for accessing Lights-Out
Management (LOM) infrastructure for the UCS-M hardware

People with admin access to LF infrastructure:

  1. amaged@cisco.com
  2. cogibbs@cisco.com
  3. daniel.smith@ericsson.com
  4. dradez@redhat.com
  5. fatih.degirmenci@ericsson.com
  6. fbrockne@cisco.com
  7. jonas.bjurel@ericsson.com
  8. jose.lausuch@ericsson.com
  9. joseph.gasparakis@intel.com
  10. morgan.richomme@orange.com
  11. pbandzi@cisco.com
  12. phladky@cisco.com
  13. stefan.k.berg@ericsson.com
  14. szilard.cserey@ericsson.com
  15. trozet@redhat.com

The people who require VPN access must have a valid
PGP key bearing a valid signature from one of these
three people. When issuing OpenVPN credentials, LF
will be sending TLS certificates and 2-factor
authentication tokens, encrypted to each recipient's PGP key.

