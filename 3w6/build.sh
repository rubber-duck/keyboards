#!/bin/bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$repo_root/../generate.py" 3w6
cd "$repo_root"

mkdir -p firmware
docker build -t qmk-builder .

docker run --rm \
    -v "$(pwd)/3w6_rgb:/qmk_firmware/keyboards/3w6_rgb:ro" \
    -v "$(pwd)/firmware:/qmk_firmware/.build:rw" \
    qmk-builder \
    qmk compile -kb 3w6_rgb -km default
