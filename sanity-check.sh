#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUT_DIR=${DIR}/.build

rm -rf ${OUT_DIR}
mkdir -p ${OUT_DIR}
(cd ${OUT_DIR} && qmake ../)
make -C ${OUT_DIR}
