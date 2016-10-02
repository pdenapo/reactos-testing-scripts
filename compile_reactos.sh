#!/bin/bash 
# Bash script for compiling ReactOs - Should be run under ReactOS BE
# Dependencies: uses jq for parsing the config.json file
CONFIG_FILE="config.json"
SRC_DIR=$(jq --raw-output .reactos_src_dir < $CONFIG_FILE)
if [[ $SRC_DIR ]]; then
    echo "reactos_src_dir= ${SRC_DIR}"
else
    echo "reactos_src_dir not defined in $CONFIG_FILE"
    exit 1
fi
BUILD_DIR=$(jq --raw-output .reactos_build_dir < $CONFIG_FILE)
if [[ $BUILD_DIR ]]; then
    echo "reactos_build_dir= ${SRC_DIR}"
else
    echo "reactos_build_dir not defined in $CONFIG_FILE"
    exit 1
fi
rm --recursive --force $BUILD_DIR
mkdir -p $BUILD_DIR
cd $BUILD_DIR
$SRC_DIR/reactos/configure.sh
cd $BUILD_DIR/reactos
ninja bootcd

