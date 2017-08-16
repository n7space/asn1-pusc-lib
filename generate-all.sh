#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUT_DIR=${DIR}/generated
ASN1_FILES="$( find ${DIR} -name *.asn1 )"
ACN_FILES="$( find ${DIR} -name *.acn )"

printf '\nFound ASN.1 files:\n'
printf '%s\n' "${ASN1_FILES[@]}"
printf '\nFound ACN files:\n'
printf '%s\n' "${ACN_FILES[@]}"

printf '\nGenerating C files...\n'

rm -rf ${OUT_DIR}
mkdir -p ${OUT_DIR}
asn1.exe -o ${OUT_DIR} -c -ACN $ASN1_FILES $ACN_FILES || exit 1
