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

# Build a table header, using ';' as column sep
SUMMARY='PDF Verify Matrix;YAML Lint;'
for adapter in ${INSTALLER_ADAPTERS}; do
    SUMMARY+="$(basename "${adapter}");"
done

# Iterate all PDFs, check with each installer adapter, log results
while IFS= read -r lab_config; do
    valid_yaml='OK'
    echo -e "\n\nyamllint -s ${lab_config}"
    if ! yamllint -s "${lab_config}"; then valid_yaml='FAIL'; fi
    SUMMARY+="\n${lab_config#labs/};${valid_yaml};"
    for adapter in ${INSTALLER_ADAPTERS}; do
        pdf_inst=0
        pdf_inst_pass=0
        pdf_yaml_pass=0
        while IFS= read -r jinja_template; do
            echo -e "\n${GEN_CFG} -y ${lab_config} -j ${jinja_template}"
            if "${GEN_CFG}" -y "${lab_config}" \
                            -j "${jinja_template}" > "${TMPF}"; then
                echo 'Result: PASS'
                ((pdf_inst_pass+=1))
                echo -e "\nyamllint -s ${jinja_template%.j2}"
                if yamllint -s "${TMPF}"; then ((pdf_yaml_pass+=1)); fi
            else
                echo 'Result: FAIL'
                RC=1
            fi
            ((pdf_inst+=1))
        done < <(find "${adapter}" -name '*.j2')
        SUMMARY+="${pdf_yaml_pass}/${pdf_inst_pass}/${pdf_inst};"
    done
done < <(find 'config' 'labs' -name 'pod*.yaml')

rm -f "${TMPF}"
echo -e '\n\nNOTE: tuple fmt: (valid YAML output/sucessful parse/templates).\n'
echo -e "${SUMMARY}" | sed -e 's/^/;/g' -e 's/;/;| /g' | column -t -s ';'

cat <<EOF

To troubleshoot PDF parsing against a specific installer adapter,
execute the following commands locally (e.g. for zte-pod2/joid):
$ ./config/utils/generate_config.py \\
    -y labs/zte/pod2.yaml \\
    -j config/installers/joid/pod_config.yaml.j2

EOF
exit "${RC}"
