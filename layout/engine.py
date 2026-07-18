"""Generation engine — shared grid walk + per-target layer formatting.

The only physical difference between boards is captured by ``outer_keys``:
Totem (ZMK) has the two outer columns (0/13) → 38 keys; the 3w6 (QMK) omits them
→ 36 keys.  Everything else is identical.
"""

from . import names
from .layers import GRIDS, LAYER_ORDER, TOTEM_ONLY

N_COLS = 14
OUTER_COLS = (0, 13)


def iter_cells(grid, outer_keys):
    """Yield non-empty tokens in row-major reading order.

    With ``outer_keys=False`` the two outer columns are treated as empty, so a
    38-key Totem grid collapses to the 36 keys the 3w6 actually has.
    """
    for row in grid:
        for col, token in enumerate(row):
            if not outer_keys and col in OUTER_COLS:
                continue
            if token != "":
                yield token


def target_layers(target):
    """Layer keys this target emits, in index order (QMK drops Totem-only tail)."""
    if target == "zmk":
        return list(LAYER_ORDER)
    return [k for k in LAYER_ORDER if k not in TOTEM_ONLY]


def used_tokens(target):
    """Set of canonical tokens referenced by this target's layers."""
    outer = target == "zmk"
    seen = set()
    for key in target_layers(target):
        seen.update(iter_cells(GRIDS[key], outer))
    return seen


def define_lines(target):
    """Grouped ``#define <name> <expansion>`` lines for every token this target
    uses, skipping identity aliases (name is already a keycode/enum there) and
    tokens with no expansion for the target."""
    used = used_tokens(target)
    idx = 0 if target == "zmk" else 1
    out = []
    for title, group in names.SECTIONS:
        block = []
        for name, pair in group.items():
            if name not in used:
                continue
            exp = pair[idx]
            if exp is None or exp == name:
                continue
            block.append(f"#define {name} {exp}")
        if block:
            out.append(f"// {title}")
            out.extend(block)
            out.append("")
    return "\n".join(out).rstrip() + "\n"


# ── ZMK layer formatting (14-col bindings grid) ───────────────────────────────

def format_zmk_layer(node_name, label, grid):
    """Render a ZMK ``keymap`` layer node.  Col 6 gets +6 padding (centre gap)."""
    col_widths = [max(len(grid[r][c]) for r in range(4)) for c in range(N_COLS)]

    def fmt_row(row_idx):
        parts = []
        for col in range(N_COLS):
            key = grid[row_idx][col]
            w = col_widths[col]
            pad = 6 if col == 6 else 2
            if col == N_COLS - 1:
                parts.append(key)
            else:
                parts.append(f"{key:<{w + pad}}")
        return "".join(parts).rstrip()

    return "\n".join([
        f"                {node_name} {{",
        f'label= "{label}";',
        "bindings = <",
        fmt_row(0),
        fmt_row(1),
        fmt_row(2),
        fmt_row(3),
        ">;",
        "                };",
    ])


# ── QMK layer formatting (LAYOUT_split_3x5_3 call) ────────────────────────────

def format_qmk_layer(layer_name, grid):
    """Render a QMK ``[layer] = LAYOUT_split_3x5_3(...)`` entry.

    The 36 collected cells map to three 10-key alpha rows and a 6-key thumb row;
    thumbs sit under the middle columns.  Col 4 gets +6 padding (the split gap)."""
    cells = list(iter_cells(grid, outer_keys=False))
    alpha = [cells[0:10], cells[10:20], cells[20:30]]
    thumbs = cells[30:36]
    thumb_row = ["", ""] + thumbs[0:3] + thumbs[3:6] + ["", ""]
    rows = alpha + [thumb_row]

    cw = [max(len(rows[r][c]) for r in range(4)) for c in range(10)]

    def fmt_row(r, last_row):
        last_non_empty = max(c for c in range(10) if rows[r][c] != "")
        parts = []
        for c in range(10):
            key = rows[r][c]
            w = cw[c]
            pad = 6 if c == 4 else 2
            if key == "":
                parts.append(" " * (w + 1 + pad))
            elif last_row and c == last_non_empty:
                parts.append(key)
            elif c == last_non_empty:
                parts.append(key + ",")
            else:
                parts.append(f"{key + ',':<{w + 1 + pad}}")
        return "".join(parts).rstrip()

    return "\n".join([
        f"    [{layer_name}] = LAYOUT_split_3x5_3(",
        "        " + fmt_row(0, False),
        "        " + fmt_row(1, False),
        "        " + fmt_row(2, False),
        "        " + fmt_row(3, True),
        "    ),",
    ])
