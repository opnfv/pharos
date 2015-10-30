===== Introduction =====
Huawei hosting San Jose will provide 1 full POD for baremetal deployment environment, 2 standalone server for virtual deployment, and 1 server with 6 executors for project's building and gate-testing.
All the resources have been attached to jenkins master, you can see the slaves below in [[https://build.opnfv.org/ci/|jenkins master]]:

  • huawei-us-build-1
  • huawei-us-deploy-vm-1
  • huawei-us-deploy-vm-1
  • huawei-us-deploy-bare-1
----

===== Overall Description =====

=== Hardware ===
  * One HP C7000 chassis with 12 dual socket server blades (E5 2680v2 haswell, 64 GB RAM and 2x400 GB SATA SSDs, 2x1GE + 2x10GE Intel-Niantec) and one HP iLO chassie management module.
  * 9 Huawei RH2285H V2 Rack Servers (128 GB RAM , 4.7 GB SATA SSDs, two Intel® Xeon® E5-2400 v2 series processors)
  * 1 Huawei S9300 10G switch for storage, managment and public traffic - 2x10GE to each server.
  * 1 Huawei S5300 1G switch for installing and Lights+out management traffic - 2x10GE to each server.
  * 1 VPN concentrator for remote access and management.
  * 1 Huawei firewall and router for public network secure access.



=== Hosting Topology ===
Below you'll find an overview of the hosting set-up:
{{:get_started:huawei_us_lab_-_new_page.jpeg?direct|}}
Figure 1: Huawei US lab OPNFV hosting environment overview


=== POD Network ===
  BMC/Lights+out management                             Install  Management  Public   Storage
                                                          PXE        +         +        +
                                                           |      vlan 101     |   vlan 102
  +                                                        +         +         +        +
  10.145.140.11                                       10.1.0.0/24    |         |        |
  +                                                        +    172.16.1.0/24  |        |
  |                                                        |         +  10.145.140.0/23 |
  |                                                        |         |         +    172.16.2.0/24
  |        +-----------------+                             |         |         |        +
  |        |                 | eth0                        |         |         |        |
  +--------+  Jumpserver     | 10.1.0.14                   |         |         |        |
  |        |  Ubuntu 14.04   +-----------------------------+         |         |        |
  |        |                 |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        |  user/pass      |                             |         |         |        |
  |        |  huawei/opnfv   |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        |                 |                             |         |         |        |
  |        +-----------------+                             |         |         |        |
  |                                                        |         |         |        |
  |                                                        |         |         |        |
  |                                                        |         |         |        |
  |       +----------------+                               |         |         |        |
  |       |             1  |                               |         |         |        |
  +-------+ +--------------+-+                             |         |         |        |
  |       | |             2  |                             |         |         |        |
  |       | | +--------------+-+                           |         |         |        |
  |       | | |             3  |                           |         |         |        |
  |       | | | +--------------+-+                         |         |         |        |
  |       | | | |             4  |                         |         |         |        |
  |       +-+ | | +--------------+-+                       |         |         |        |
  |         | | | |             5  +-----------------------+         |         |        |
  |         +-+ | |  nodes for     |                       |         |         |        |
  |           | | |  deploying     +---------------------------------+         |        |
  |           +-+ |  opnfv         |                       |         |         |        |
  |             | |                +-------------------------------------------+        |
  |             +-+                |                       |         |         |        |
  |               |                +----------------------------------------------------+
  |               +----------------+                       |         |         |        |
  |                                                        |         |         |        |
  |                                                        |         |         |        |
  |                                                        +         +         +        +


----

===== How to uses our resources? =====
  *Build Resource:
You can see the slaves named "huawei-us-build-[digit]" or "huawei-build-[digit]" in [[https://build.opnfv.org/ci/|jenkins master]]

These resources are dedicated to CI. If you want to use huawei resource to run some automated jobs, you donnot need to apply for the credentials, just specify the node as "huawei-build" . If have some other requirement or encounter any problem, please contact: [[weidong.shao@huawei.com]]


  *Deployment Resource:
You can see the slaves named "huawei-us-deploy-vm/bare-[digit]" or "huawei-deploy-vm/bare-[digit]" in [[https://build.opnfv.org/ci/|jenkins master]]

We have two types of deployment resources, virtual deployment environment and baremetal deployment environment. Both types of environment can be deployed by any types of installer, and provide the same testbed for testing and the same infrastructure for VNF.

You can access our deployment resources by applying for the VPN credentials, details please see the section below.

----

===== Access =====
This environment is free to use by any OPNFV contributor or committer for the purpose of OPNFV approved activities, you just need to obtain VPN credentials to access.

Access to this environment can be granted by sending a e-mail to:
  * [[weidong.shao@huawei.com]]
  * [[opnfv-helpdesk@rt.linuxfoundation.org]]

Following information should be provided in the request:
  * subject: opnfv_huawei_access
  * Full name
  * e-mail
  * Phone
  * Organization
  * OPNFV Contributor/Committer name :
  * OPNFV Project(s) Association:
  * LF ID:
  * Recommended by:
  * PGP public key (preferably registered with a PGP PKI server)
  * SSH public key

Granting access normally takes 3-5 business days.
----
