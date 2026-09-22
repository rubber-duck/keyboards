#!/usr/bin/env python3
"""Single dispatcher — generate the keymap for one board or all boards.

Usage:
    python generate.py totem      # ZMK  -> totem/config/totem.keymap
    python generate.py 3w6        # QMK  -> 3w6/3w6_rgb/keymaps/default/keymap.c
    python generate.py draw       # keymap-drawer YAML -> keymap-drawer/keymap.yaml
    python generate.py all        # all of the above
    python generate.py all --check # fail if generated files are missing or stale

The layout is defined once in ``layout/`` with a single set of canonical macro
names; each board's ``targets/`` module only swaps the definition part (what each
name expands to) and the board-specific boilerplate.
"""

import argparse
import sys
from pathlib import Path

from layout import draw, engine
from targets import zmk, qmk

ROOT = Path(__file__).resolve().parent
TARGETS = {"totem": zmk, "3w6": qmk, "draw": draw}


def build(name, check=False):
    module = TARGETS[name]
    text = module.render()
    out = ROOT / module.OUTPUT
    if check:
        if not out.is_file() or out.read_bytes() != text.encode('utf-8'):
            print(f"[{name:5}] stale or missing: {module.OUTPUT}; run python generate.py all")
            return False
        print(f"[{name:5}] up to date: {module.OUTPUT}")
        return True
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(text.encode('utf-8'))
    if module.TARGET == "draw":
        detail = f"{len(engine.target_layers('zmk'))} layers"
    else:
        detail = f"{len(engine.target_layers(module.TARGET))} layers"
    print(f"[{name:5}] wrote {module.OUTPUT}  ({detail})")
    return True


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('target', choices=(*TARGETS, 'all'))
    parser.add_argument('--check', action='store_true',
                        help='check committed outputs without writing files')
    args = parser.parse_args(argv)
    names = list(TARGETS) if args.target == "all" else [args.target]
    ok = True
    for name in names:
        ok &= build(name, check=args.check)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
