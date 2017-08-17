.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.


Networking
----------

**Network Hardware**

  * 24 or 48 Port TOR Switch
  * NICs - Combination of 1GE and 10GE based on network topology options (per server can be on-board
    or use PCI-e)
  * Connectivity for each data/control network is through a separate NIC. This
    simplifies Switch Management however requires more NICs on the server and also more switch ports
  * BMC (Baseboard Management Controller) for lights-out mangement network using IPMI (Intelligent
    Platform Management Interface)

**Network Options**

  * Option I: 4x1G Control, 2x10G Data, 48 Port Switch

    * 1 x 1G for lights-out Management
    * 1 x 1G for Admin/PXE boot
    * 1 x 1G for control-plane connectivity
    * 1 x 1G for storage
    * 2 x 10G for data network (redundancy, NIC bonding, High bandwidth testing)

  * Option II: 1x1G Control, 2x 10G Data, 24 Port Switch

    * Connectivity to networks is through VLANs on the Control NIC
    * Data NIC used for VNF traffic and storage traffic segmented through VLANs

  * Option III: 2x1G Control, 2x10G Data, 2x10G Storage, 24 Port Switch

    * Data NIC used for VNF traffic
    * Storage NIC used for control plane and Storage segmented through VLANs (separate host traffic
      from VNF)
    * 1 x 1G for lights-out mangement
    * 1 x 1G for Admin/PXE boot
    * 2 x 10G for control-plane connectivity/storage
    * 2 x 10G for data network

Documented configuration to include:

 - Subnet, VLANs (may be constrained by existing lab setups or rules)
 - IPs
 - Types of NW - lights-out, public, private, admin, storage
 - May be special NW requirements for performance related projects
 - Default gateways

**Sample Network Drawings**

.. image:: ../../images/bridge2.png

.. image:: ../../images/opnfv-pharos-diagram-v01.jpg

.. image:: ../../images/opnfv-example-lab-diagram.png

Download the visio zip file here:
`opnfv-example-lab-diagram.vsdx.zip
<https://wiki.opnfv.org/_media/opnfv-example-lab-diagram.vsdx.zip>`_
