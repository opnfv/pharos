Use eyaml to decrypt secret values

Testing this patch.
Check out patch:

cd pharos/config/utils

Install eyaml and create keys:
yum install ruby-gems
gem install hiera-eyaml
eyaml createkeys

keys are put into ./keys/
move keys to /etc/eyaml_keys/
place config.yaml in ~/.eyaml/config.yaml

copy a yaml and a j2 to .
cp ~/foo/securedlab/labs/lf/pod2.yaml .
cp ~/foo/pharos/config/installers/apex/pod_config.yaml.j2 .

create some encrypted values:
eyaml encrypt -s 'opnfv'

replace user and pass values:

    type: ipmi
    versions:
      - 2.0
    user: ENC[PKCS7 ...]
    pass: ENC[PKCS7 ...]

decrypt secret values:

Run generate_config.py, it will output the decrypted values
eg: ./newgenerate_config.py -y pod2.yaml -j pod_config.yaml.j2
