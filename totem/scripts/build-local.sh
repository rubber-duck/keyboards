#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build_yaml="${BUILD_YAML:-$repo_root/build.yaml}"
config_dir="${CONFIG_DIR:-$repo_root/config}"
workspace="${ZMK_LOCAL_WORKSPACE:-$repo_root/.build/zmk}"
firmware_dir="${FIRMWARE_DIR:-$repo_root/firmware}"
image="${ZMK_DOCKER_IMAGE:-zmkfirmware/zmk-build-arm:stable}"
engine="${CONTAINER_ENGINE:-}"

if [[ -z "$engine" ]]; then
  if command -v docker >/dev/null 2>&1; then
    engine=docker
  elif command -v podman >/dev/null 2>&1; then
    engine=podman
  else
    echo "ERROR: docker or podman is required" >&2
    exit 1
  fi
fi

if [[ ! -f "$build_yaml" ]]; then
  echo "ERROR: build matrix not found: $build_yaml" >&2
  exit 1
fi

if [[ ! -d "$config_dir" ]]; then
  echo "ERROR: config directory not found: $config_dir" >&2
  exit 1
fi

mkdir -p "$workspace" "$workspace/.home" "$workspace/config" "$firmware_dir"
find "$workspace/config" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
cp -R "$config_dir"/. "$workspace/config/"

python3 - "$build_yaml" >"$workspace/build-matrix.tsv" <<'PY'
import re
import sys

items = []
current = None
for raw in open(sys.argv[1], encoding="utf-8"):
    line = raw.rstrip()
    if re.match(r"^\s*-\s+", line):
        if current:
            items.append(current)
        current = {}
        line = re.sub(r"^\s*-\s+", "", line)
    elif current is None:
        continue
    else:
        line = line.strip()

    match = re.match(r"([A-Za-z0-9_-]+):\s*(.*)$", line)
    if match and current is not None:
        key, value = match.groups()
        current[key] = value.strip().strip('"\'')

if current:
    items.append(current)

for item in items:
    board = item.get("board", "")
    if not board:
        continue
    shield = item.get("shield", "")
    artifact = item.get("artifact-name", "")
    snippet = item.get("snippet", "")
    cmake_args = item.get("cmake-args", "")
    print("\t".join([board, shield, artifact, snippet, cmake_args]))
PY

if [[ ! -s "$workspace/build-matrix.tsv" ]]; then
  echo "ERROR: no build entries found in $build_yaml" >&2
  exit 1
fi

cat >"$workspace/build-inside.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail

cd /workspace

if [[ ! -d .west ]]; then
  west init -l config
fi

west update --fetch-opt=--filter=tree:0
west zephyr-export

mkdir -p artifacts

while IFS=$'\t' read -r board shield artifact_name snippet cmake_args; do
  display_name="${shield:+$shield - }$board"
  default_artifact="${shield:+$shield-}${board//\//_}-zmk"
  artifact_name="${artifact_name:-$default_artifact}"
  build_dir="build/$artifact_name"

  west_args=()
  if [[ -n "$snippet" ]]; then
    west_args+=("-S" "$snippet")
  fi

  cmake_extra=(-DZMK_CONFIG=/workspace/config)
  if [[ -n "$shield" ]]; then
    cmake_extra+=("-DSHIELD=$shield")
  fi
  if [[ -n "$cmake_args" ]]; then
    read -r -a parsed_cmake_args <<<"$cmake_args"
    cmake_extra+=("${parsed_cmake_args[@]}")
  fi

  echo "==> Building $display_name"
  west build -s zmk/app -d "$build_dir" -p -b "$board" "${west_args[@]}" -- "${cmake_extra[@]}"

  if [[ -f "$build_dir/zephyr/zmk.uf2" ]]; then
    cp "$build_dir/zephyr/zmk.uf2" "artifacts/$artifact_name.uf2"
  elif [[ -f "$build_dir/zephyr/zmk.bin" ]]; then
    cp "$build_dir/zephyr/zmk.bin" "artifacts/$artifact_name.bin"
  else
    echo "ERROR: no firmware artifact produced for $display_name" >&2
    exit 1
  fi
done < build-matrix.tsv
SH
chmod +x "$workspace/build-inside.sh"

"$engine" run --rm \
  --workdir /workspace \
  --user "$(id -u):$(id -g)" \
  -e HOME=/workspace/.home \
  -v "$workspace:/workspace" \
  "$image" \
  /workspace/build-inside.sh

find "$firmware_dir" -mindepth 1 -maxdepth 1 -type f \( -name '*.uf2' -o -name '*.bin' \) -delete
cp "$workspace"/artifacts/* "$firmware_dir"/

echo "Firmware artifacts:"
ls -lh "$firmware_dir"
