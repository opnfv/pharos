Spirent Virtual Cloud Test Lab
===============================

A community provided metal resource hosted at Nephoscale, leveraged for SDN/NFV public testing and
OpenDaylight, OpenStack, OPNFV projects.

**Spirent VCT Lab** is currently working on 3 different **OpenStack** environments each one of them
deployed on different hardware configuration:

  * **OpenStack Juno - 2014.2.2 release** (CentOS 7, 20 Cores, 64 GB RAM, 1 TB SATA, 40 Gbps)
  * **OpenStack Juno - 2014.2.2 release** (Ubuntu 14.04, 8 cores, 32 GB RAM, 500 GB SATA, 10 Gbps)
  * **OpenStack Icehouse - 2014.1.3 release**
  * **OpenStack Icehouse - 2014.1.3 release**

----

There are a number of different networks referenced in the VPTC Design Blueprint.

  * Public Internet – 1 g
  * Private Management – 1g
  * Mission Clients – 10g
  * Mission Servers – 10g

These can be added or removed as specified by the test methodology.  There are 8 x 10 gige SFP+
ports available on a typical C100MP used for Avalanche Layer 4-7 testing.  The N4U offers 2 x 40
gige QSFP+ ports with the MX-2 Spirent Test Center Layer 2-3 testing.  There are 2 x Cumulus
switches with 32 ports of 40 gige QSFP+ ports for a total capacity of 256 ports of 10 gige. We use
QSFP+ to SFP+ break out cables to convert a single 40 gige port into 4 x 10 gige ports.  Together
these offer a flexible solution to allow up to 8 simultaneous tests to take place with physical
traffic generators at the same time.  Assuming a 10 to 1 oversubscription ratio we could handle 80
community users with the current environment.

For example:

  * An 80 Gbps test would need 4 port pairs of 10 gige each and require 8 mission networks.
  * Multiple clients sharing common test hardware might have dedicated management networks for their
    DUTs yet communicate with the APIs and Management services via a shared DMZ network protected by
    a firewall.
  * SSL and IPSec VPN will typically be leveraged to connect networks across the
    untrusted Internet or other third party networks.
  * Stand-alone DUT servers using STCv and AVv traffic generators could easily scale to hundreds of
    servers as needed.

.. image:: images/spirent_vptc-public-drawing.png
