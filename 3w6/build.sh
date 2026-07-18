#!/bin/bash

set -e

mkdir -p firmware
docker build -t qmk-builder .

docker run --rm \
    -v "$(pwd)/3w6_rgb:/qmk_firmware/keyboards/3w6_rgb:ro" \
    -v "$(pwd)/firmware:/qmk_firmware/.build:rw" \
    qmk-builder \
    qmk compile -kb 3w6_rgb -km default