#!/bin/bash
# SPDX-license-identifier: Apache-2.0
##############################################################################
# Copyright (c) 2018 Linux Foundation and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

set +x
set +o errexit
export PATH=$PATH:/usr/local/bin/

# Optional filtering of test matrix: per-lab, per-pod, per-installer
# e.g. To check zte-pod{2,3} against all installer adapters:
# ./config/utils/check-jinja2.sh zte 'pod(2|3)'
FILTER_LAB=${1:-*}                           # e.g. 'zte'  (glob)
FILTER_POD=${2:-(pod|virtual)[[:digit:]]+}   # e.g. 'pod1' (regex)
FILTER_IA=${3:-*}                            # e.g. 'fuel' (glob)

GEN_CFG='python ./config/utils/generate_config.py'
INSTALLER_ADAPTERS="./config/installers/${FILTER_IA}"
TMPF='/tmp/out.yml' # should be outside Jenkins WS to prevent data leakage
RC=0

echo "Using $(yamllint --version)"

# Build a table header, using ';' as column sep
for adapter in 'PDF Verify Matrix' ${INSTALLER_ADAPTERS}; do
    SUMMARY+="$(basename "${adapter}");"
done

# Iterate all PDFs, check with each installer adapter, log results
# shellcheck disable=SC2086
while IFS= read -r lab_config; do
    SUMMARY+="\n${lab_config#labs/};"
    idf_config="$(dirname "${lab_config}")/idf-$(basename "${lab_config}")"
    idf_installer=$(grep 'installer:' "${idf_config}" 2>/dev/null || echo)
    echo "###################### ${lab_config} ######################"
    for adapter in ${INSTALLER_ADAPTERS}; do
        pdf_inst=0
        pdf_inst_pass=0
        pdf_yaml_pass=0
        installer_name=$(basename "${adapter}")
        if [ -n "${idf_installer}" ] && echo "${idf_installer}" | \
                grep -vq "${installer_name}"; then
            SUMMARY+='-;'
            echo -n "[GENERATE] [SKIP] idf.installer defined and "
            echo -e "${installer_name} not listed, skipping.\n"
            continue
        fi
        while IFS= read -r jinja_template; do
            pdf_gen_cmd="${GEN_CFG} -y ${lab_config} -j ${jinja_template} \
                        -i $(dirname "${jinja_template}")"
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
done < <(find labs/${FILTER_LAB} -regextype egrep \
                                 -regex "labs/.+/${FILTER_POD}.yaml")
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
