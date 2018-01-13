#!/bin/bash
# SPDX-license-identifier: Apache-2.0
##############################################################################
# Copyright (c) 2016 Linux Foundation and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set +x
set +o errexit
export PATH=$PATH:/usr/local/bin/

GEN_CFG='./config/utils/generate_config.py'
INSTALLER_ADAPTERS='./config/installers/*'
TMPF='/tmp/out.yml' # should be outside Jenkins WS to prevent data leakage
RC=0

echo "Using $(yamllint --version)"

# Build a table header, using ';' as column sep
for adapter in 'PDF Verify Matrix' ${INSTALLER_ADAPTERS}; do
    SUMMARY+="$(basename "${adapter}");"
done

# Iterate all PDFs, check with each installer adapter, log results
while IFS= read -r lab_config; do
    SUMMARY+="\n${lab_config#labs/};"
    echo "###################### ${lab_config} ######################"
    for adapter in ${INSTALLER_ADAPTERS}; do
        pdf_inst=0
        pdf_inst_pass=0
        pdf_yaml_pass=0
        while IFS= read -r jinja_template; do
            pdf_gen_cmd="${GEN_CFG} -y ${lab_config} -j ${jinja_template}"
            if ${pdf_gen_cmd} > "${TMPF}"; then
                ((pdf_inst_pass+=1))
                echo "[GENERATE] [OK] ${pdf_gen_cmd}"
                if yamllint -s <(sed 's|ENC\[PKCS.*\]|opnfv|g' "${TMPF}"); then
                    ((pdf_yaml_pass+=1));
                    echo "[YAMLLINT] [OK] yamllint -s ${jinja_template%.j2}"
                else
                    echo "[YAMLLINT] [ERROR] yamllint -s ${jinja_template%.j2}"
                fi
            else
                echo "[GENERATE] [ERROR] ${pdf_gen_cmd}"
                RC=1
            fi
            ((pdf_inst+=1))
            echo ''
        done < <(find "${adapter}" -name '*.j2')
        SUMMARY+="${pdf_yaml_pass}/${pdf_inst_pass}/${pdf_inst};"
    done
done < <(find 'labs' -name 'pod*.yaml')
rm -f "${TMPF}"

cat <<EOF
###################### Result Matrix ######################

NOTE: tuple fmt: (valid YAML output/sucessful parse/templates).

$(echo -e "${SUMMARY}" | sed -e 's/^/;/g' -e 's/;/;| /g' | column -t -s ';')

To troubleshoot PDF parsing against a specific installer adapter,
execute the following commands locally (e.g. for zte-pod2/joid):
$ ./config/utils/generate_config.py \\
    -y labs/zte/pod2.yaml \\
    -j config/installers/joid/pod_config.yaml.j2

EOF
exit "${RC}"
