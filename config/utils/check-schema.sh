#!/bin/bash -e
# SPDX-license-identifier: Apache-2.0
##############################################################################
# Copyright (c) 2018 Enea AB and others.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

export PATH=$PATH:/usr/local/bin/

# We only have one schema version for now, so we can hard set it here
VALIDATE_SCHEMA='./config/utils/validate_schema.py'
PDF_SCHEMA='./config/pdf/pod1.schema.yaml'
RC=0

# Iterate all PDFs, check with each installer adapter, log results
pdf_schema_cmd="${VALIDATE_SCHEMA} -s ${PDF_SCHEMA}"
while IFS= read -r lab_config; do
    echo "###################### ${lab_config} ######################"
    if ${pdf_schema_cmd} -y "${lab_config}"
    then
        SUMMARY+=";${lab_config#labs/};OK;\n"
        echo "[SCHEMA] [OK] ${pdf_schema_cmd} -y ${lab_config}"
    else
        SUMMARY+=";${lab_config#labs/};ERROR;\n"
        RC=1
        echo "[SCHEMA] [ERROR] ${pdf_schema_cmd} -y ${lab_config}"
    fi
    echo ''
done < <(find 'labs' -name 'pod*.yaml')

cat <<EOF
###################### Schema Validation Matrix ######################

$(echo -e "${SUMMARY}" | sed -e 's/;/;| /g' | column -t -s ';')
EOF
exit "${RC}"
