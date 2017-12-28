#!/bin/bash -e
##############################################################################
# Copyright (c) 2018 Enea AB and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

export PATH=$PATH:/usr/local/bin/

VALIDATE_SCHEMA='python ./config/utils/validate_schema.py'
PDF_SCHEMA='./config/pdf/pod1.schema.yaml'
IDF_SCHEMA='./config/pdf/idf-pod1.schema.yaml'
RC=0

SUMMARY+=";;PDF;IDF;\n"
while IFS= read -r lab_config; do
    idf_config="$(dirname "${lab_config}")/idf-$(basename "${lab_config}")"
    pdf_cmd="${VALIDATE_SCHEMA} -s ${PDF_SCHEMA} -y ${lab_config}"
    idf_cmd="${VALIDATE_SCHEMA} -s ${IDF_SCHEMA} -y ${idf_config}"
    echo "###################### ${lab_config} ######################"
    pdf_out=$(${pdf_cmd} 2>&1 | sed 's|ENC\[PKCS.*\][\\n]*|opnfv|g')
    if [ -z "${pdf_out}" ]; then
        SUMMARY+=";${lab_config#labs/};OK;"
        echo "[PDF] [OK] ${pdf_cmd}"
    else
        SUMMARY+=";${lab_config#labs/};ERROR;"
        RC=1
        echo "${pdf_out}"
        echo "[PDF] [ERROR] ${pdf_cmd}"
    fi
    if [ ! -f "${idf_config}" ]; then
        SUMMARY+="-;\n"
    elif ${idf_cmd}; then
        SUMMARY+="OK;\n"
        echo "[IDF] [OK] ${idf_cmd}"
    else
        SUMMARY+="ERROR;\n"
        RC=1
        echo "[IDF] [ERROR] ${idf_cmd}"
    fi
    echo ''
done < <(find 'labs' -name 'pod*.yaml' -or -name 'virtual*.yaml')

cat <<EOF
###################### Schema Validation Matrix ######################

$(echo -e "${SUMMARY}" | sed -e 's/;/;| /g' | column -t -s ';')
EOF
exit "${RC}"
