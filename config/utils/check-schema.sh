#!/bin/bash -e
##############################################################################
# Copyright (c) 2018 Enea AB and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

export PATH=$PATH:/usr/local/bin/

VALIDATE_SCHEMA='./config/utils/validate_schema.py'
PDF_SCHEMA='./config/pdf/pod1.schema.yaml'
RC=0

while IFS= read -r lab_config; do
    pdf_cmd="${VALIDATE_SCHEMA} -s ${PDF_SCHEMA} -y ${lab_config}"
    echo "###################### ${lab_config} ######################"
    pdf_out=$(${pdf_cmd} |& sed 's|ENC\[PKCS.*\]|opnfv|g')
    if [ -z "${pdf_out}" ]; then
        SUMMARY+=";${lab_config#labs/};OK;\n"
        echo "[PDF] [OK] ${pdf_cmd}"
    else
        SUMMARY+=";${lab_config#labs/};ERROR;\n"
        RC=1
        echo "${pdf_out}"
        echo "[PDF] [ERROR] ${pdf_cmd}"
    fi
    echo ''
done < <(find 'labs' -name 'pod*.yaml')

cat <<EOF
###################### Schema Validation Matrix ######################

$(echo -e "${SUMMARY}" | sed -e 's/;/;| /g' | column -t -s ';')
EOF
exit "${RC}"
