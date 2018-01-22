.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. (c) 2018 OPNFV and others.

Use eyaml to decrypt secret values
==================================

Prerequisites
-------------

#. Install eyaml and create keys (All of this should be done on the slave server)

    .. code-block:: bash

        $ sudo yum install rubygems || sudo apt-get install ruby
        $ sudo gem install hiera-eyaml
        $ eyaml createkeys

#. Move keys to /etc/eyaml_keys

    .. code-block:: bash

        $ sudo mkdir -p /etc/eyaml_keys/
        $ sudo mv ./keys/* /etc/eyaml_keys/
        $ sudo rmdir ./keys

#. Set up eyaml config.yaml

    .. code-block:: bash

        $ mkdir ~/.eyaml/
        $ cp config.example.yaml ~/.eyaml/config.yaml

Encryption
----------

#. Copy a PDF (yaml) to current directory (or edit the PDF in-place)

NOTE: There is a sample encrypted PDF located at `../pdf/pod1.encrypted.yaml`.
Data in that file is only an example and can't be decrypted without the PEM,
which is not provided.

    .. code-block:: bash

        $ cp ~/foo/securedlab/labs/lf/pod2.yaml .

#. Create some encrypted values

    .. code-block:: bash

        $ eyaml encrypt -s 'opnfv'

#. Replace values to be encrypted

    .. code-block:: yaml

        type: ipmi
        versions:
          - 2.0
        user: ENC[PKCS7 ...]
        pass: ENC[PKCS7 ...]

Decryption
----------

    .. code-block:: bash

        $ ./generate_config.py -y pod2.yaml -j ../installers/apex/pod_config.yaml.j2
