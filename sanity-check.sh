#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUT_DIR=${DIR}/.build
SCHEMA_FILE=asn1-lib-schema.json
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

printf "\n\nDownloading schema...\n"
(cd ${OUT_DIR} && wget --no-cache ${URL}/${SCHEMA_FILE})
ret=$?
if [ $ret != 0 ]
then
	echo "Error getting json-schema: $ret"
	exit $ret
fi

printf "\n\nValidating metadata...\n"
find . -name meta.json -print -exec jsonschema -i {} ${OUT_DIR}/${SCHEMA_FILE} \;
ret=$?
if [ $ret != 0 ]
then
	echo "Error validating metadata: : $ret"
	exit $ret
fi
