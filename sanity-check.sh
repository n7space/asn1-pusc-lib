#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUT_DIR=${DIR}/.build
MODULE_SCHEMA_FILE=asn1-lib-module-schema.json
GENERAL_SCHEMA_FILE=asn1-lib-general-schema.json
URL=https://raw.githubusercontent.com/n7mobile/asn1scc.IDE/master/schemas

rm -rf ${OUT_DIR}
mkdir -p ${OUT_DIR}
ret=$?
if [ $ret != 0 ]
then
	echo "Error creating directory: $ret"
	exit ret
fi

printf "\n\nGenerating Makefile files...\n"
(cd ${OUT_DIR} && qmake ../)
ret=$?
if [ $ret != 0 ]
then
	echo "Error generating makefile: $ret"
	exit ret
fi

printf "\n\nGenerating and building C files...\n"
make -C ${OUT_DIR}
ret=$?
if [ $ret != 0 ]
then
	echo "Error building C files: $ret"
	exit $ret
fi

printf "\n\nDownloading module schema...\n"
(cd ${OUT_DIR} && wget --no-cache ${URL}/${MODULE_SCHEMA_FILE})
ret=$?
if [ $ret != 0 ]
then
	echo "Error getting module json-schema: $ret"
	exit $ret
fi

printf "\n\nDownloading general info schema...\n"
(cd ${OUT_DIR} && wget --no-cache ${URL}/${GENERAL_SCHEMA_FILE})
ret=$?
if [ $ret != 0 ]
then
	echo "Error getting general json-schema: $ret"
	exit $ret
fi

printf "\n\nValidating modules metadata...\n"
find . -name meta.json -print0 \
    | xargs --verbose -I{} -0 jsonschema -i {} ${OUT_DIR}/${MODULE_SCHEMA_FILE}
ret=$?
if [ $ret != 0 ]
then
	echo "Error validating module's metadata: $ret"
	exit $ret
fi

printf "\n\nValidating general info...\n"
jsonschema -i info.json ${OUT_DIR}/${GENERAL_SCHEMA_FILE}
ret=$?
if [ $ret != 0 ]
then
	echo "Error validating general metadata: $ret"
	exit $ret
fi
