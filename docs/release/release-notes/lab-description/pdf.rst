.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2016 OPNFV.

********************
Pod Description File
********************

The PDF(Pod Descrition File) provides template for POD's hardware information for all the
installers in yaml. The target is to use the same PDF file to deploy a POD by any installer with
any scenario it supports. It is the base of the dynamic CI , LaaS(Lab as a Service) and
SDF(Scenario Description File).

Currently Jinja template is used to transfer the PDF to the specific installer's
template. PDF, Jinja template and the transfering tools are all stored in :ref:`securedlab`.
You can find the latest PDF template in
https://gerrit.opnfv.org/gerrit/#/c/38283/8/labs/lf/pod4.yaml.

