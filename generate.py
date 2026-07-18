#!/usr/bin/env python3
"""Single dispatcher — generate the keymap for one board or all boards.

Usage:
    python generate.py totem      # ZMK  -> totem/config/totem.keymap
    python generate.py 3w6        # QMK  -> 3w6/3w6_rgb/keymaps/default/keymap.c
    python generate.py draw       # keymap-drawer YAML -> keymap-drawer/keymap.yaml
    python generate.py all        # all of the above

The layout is defined once in ``layout/`` with a single set of canonical macro
names; each board's ``targets/`` module only swaps the definition part (what each
name expands to) and the board-specific boilerplate.
"""

import sys
from pathlib import Path

from layout import draw, engine
from targets import zmk, qmk

ROOT = Path(__file__).resolve().parent
TARGETS = {"totem": zmk, "3w6": qmk, "draw": draw}


def build(name):
    module = TARGETS[name]
    text = module.render()
    out = ROOT / module.OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    if module.TARGET == "draw":
        detail = f"{len(engine.target_layers('zmk'))} layers"
    else:
        detail = f"{len(engine.target_layers(module.TARGET))} layers"
    print(f"[{name:5}] wrote {module.OUTPUT}  ({detail})")


def main(argv):
    if len(argv) != 1 or argv[0] not in (*TARGETS, "all"):
        print(__doc__)
        return 2
    names = list(TARGETS) if argv[0] == "all" else [argv[0]]
    for name in names:
        build(name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
