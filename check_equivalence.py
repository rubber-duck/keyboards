#!/usr/bin/env python3
"""Verify the merged generator produces the SAME effective layout as the two
original generators, by expanding both to concrete keycodes and diffing per
layer / per position.  Only macro *names* changed; expansions must be identical.

Run from the keyboards/ repo root.  Points at the original repos for the baseline.
"""

import importlib.util
import re
import sys
from pathlib import Path

from layout import engine, names
from layout.layers import GRIDS, LAYER_ORDER, TOTEM_ONLY

ORIG_ZMK = Path("/home/dev/zmk-config-totem/format_keymap.py")
ORIG_QMK = Path("/home/dev/qmk-config-3w6/generate_keymap.py")


def _load(path, modname):
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── ZMK ───────────────────────────────────────────────────────────────────────

def _zmk_defines(header):
    """Parse '#define NAME REST' -> {NAME: REST} from the original header."""
    out = {}
    for line in header.splitlines():
        m = re.match(r"#define\s+(\S+)\s+(.+)$", line.strip())
        if m and not m.group(1)[0].isdigit():
            name, rest = m.group(1), m.group(2).strip()
            # skip the numeric layer-index defines
            if re.fullmatch(r"\d+", rest):
                continue
            out[name] = rest
    return out


def _zmk_expand_old(cell, defs):
    """Expand an original ZMK grid cell to its concrete '&...' binding."""
    if cell.startswith("&"):
        head, _, tail = cell[1:].partition(" ")
        if head in defs:                      # e.g. &k_at -> & + 'kp LS(N2)'
            return "&" + defs[head] + (" " + tail if tail else "")
        return cell                           # &kp Q, &trans, &tm_w1, ...
    if cell in defs:                          # bare alias: hm_a -> '&mt LGUI A'
        return defs[cell]
    return cell


def zmk_old_layers():
    mod = _load(ORIG_ZMK, "orig_zmk")
    defs = _zmk_defines(mod.header)
    result = {}
    for name, label, grid in mod.layers:
        seq = [_zmk_expand_old(c, defs) for row in grid for c in row if c != ""]
        result[label.replace(" ", "_")] = seq
    return result


def zmk_new_layers():
    result = {}
    for key in LAYER_ORDER:
        seq = [names.expansion(t, "zmk")
               for t in engine.iter_cells(GRIDS[key], outer_keys=True)]
        result[key] = seq
    return result


# ── QMK ───────────────────────────────────────────────────────────────────────

def _qmk_defines(header):
    out = {}
    for line in header.splitlines():
        m = re.match(r"#define\s+([A-Za-z_]\w*)\s+(.+)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


# custom-keycode spelling differences (enum members, not #defines)
_QMK_NORM = {"CK_PC_DLLS": "PC_DLLS", "CK_PC_DLLE": "PC_DLLE"}
_QMK_NORM.update({f"TM_WN{d}": f"TM_W{d}" for d in "1234567890"})


def _qmk_expand(cell, defs):
    cell = defs.get(cell, cell)
    return _QMK_NORM.get(cell, cell)


def qmk_old_layers():
    mod = _load(ORIG_QMK, "orig_qmk")
    defs = _qmk_defines(mod.header)
    result = {}
    for name, ltype, grid in mod.layers:
        if ltype == "mirrored":
            rows = [grid[r] + grid[r][::-1] for r in range(3)] + [grid[3]]
        else:
            rows = grid
        seq = [_qmk_expand(c, defs) for row in rows for c in row if c != ""]
        result[name.lstrip("_")] = seq
    return result


def qmk_new_layers():
    result = {}
    for key in LAYER_ORDER:
        if key in TOTEM_ONLY:
            continue
        seq = []
        for t in engine.iter_cells(GRIDS[key], outer_keys=False):
            exp = names.expansion(t, "qmk")
            seq.append(_QMK_NORM.get(exp, exp) if exp == t else exp)
        result[key] = seq
    return result


# ── diff ──────────────────────────────────────────────────────────────────────

def compare(kind, old, new):
    ok = True
    for layer in old:
        if layer not in new:
            print(f"  [{kind}] {layer}: missing in new")
            ok = False
            continue
        o, n = old[layer], new[layer]
        if len(o) != len(n):
            print(f"  [{kind}] {layer}: length {len(o)} -> {len(n)}")
            ok = False
        for i, (a, b) in enumerate(zip(o, n)):
            if a != b:
                print(f"  [{kind}] {layer}[{i}]: {a!r} != {b!r}")
                ok = False
    extra = set(new) - set(old)
    if extra:
        print(f"  [{kind}] new-only layers (expected for Totem): {sorted(extra)}")
    return ok


def main():
    ok = True
    print("ZMK (Totem) equivalence:")
    ok &= compare("zmk", zmk_old_layers(), zmk_new_layers())
    print("QMK (3w6) equivalence:")
    ok &= compare("qmk", qmk_old_layers(), qmk_new_layers())
    print("\n" + ("ALL LAYERS MATCH ✓" if ok else "MISMATCH ✗"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
