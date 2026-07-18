# keyboards

One layout, two boards. A single generator produces the keymaps for both my
split keyboards from **one shared layout definition**:

| Board | Firmware | Keys | Generated file |
|-------|----------|------|----------------|
| [Totem](totem/) | ZMK  | 38 (2 extra outer pinky keys, wireless) | `totem/config/totem.keymap` |
| [3w6](3w6/)     | QMK  | 36 (wired, per-key RGB)                 | `3w6/3w6_rgb/keymaps/default/keymap.c` |

## How it works

The layout ("what key goes where") is defined **once**; only the *definition
part* ("what each macro name expands to") is swapped per board.

```
generate.py            # dispatcher: python generate.py totem|3w6|draw|all
layout/
  layers.py            # the shared 14x4 canonical grids, one per layer
  names.py             # canonical token -> (ZMK expansion, QMK expansion)
  engine.py            # grid walk (outer_keys flag) + per-target formatting
  draw.py              # canonical token -> display legend (keymap-drawer YAML)
targets/
  zmk.py               # ZMK boilerplate: behaviors, macros{} node, keymap wrapper
  qmk.py               # QMK boilerplate: enums, tmux table, RGB/OS-detection code
totem/ , 3w6/          # self-contained, buildable board configs
keymap-drawer/         # generated keymap.yaml (visualization definition)
check_equivalence.py   # proves output matches the two original generators
```

Every grid cell is a **canonical token** (`K_Q`, `HM_A`, `LT_SYM`, `SY_AT`,
`TM_W1`, …). Each board's `targets/` module maps those names to its own syntax —
e.g. the home-row `A` is `HM_A`, which becomes `&mt LGUI A` on ZMK and
`LGUI_T(KC_A)` on QMK. The generated keymaps therefore use identical names in the
layout section and differ only in the `#define`/definition header.

### The one physical difference

The Totem has two extra outer-pinky keys (cols 0 and 13 of the 14-wide grid) and a
Bluetooth layer; the 3w6 does not. This is the single knob `outer_keys`:
`targets/zmk.py` sets it `True` (38 keys), `targets/qmk.py` sets it `False`
(cols 0/13 dropped → 36 keys). The grids themselves are the same for both.

## Regenerate

```sh
python generate.py all          # regenerate both keymaps
python check_equivalence.py     # verify vs the original per-board generators
```

Run the generator after **any** layout edit — it is not wired into the build.

## Visualize the layers

`generate.py draw` writes a [keymap-drawer](https://github.com/caksoylar/keymap-drawer)
definition to `keymap-drawer/keymap.yaml` (the shared split 3x5+3 core, all layers,
with tap/hold legends). Render it to SVG:

```sh
pipx install keymap-drawer          # or: pip install keymap-drawer
keymap draw keymap-drawer/keymap.yaml > keymap-drawer/keymap.svg
```

The Totem's two extra outer keys (home-row Shift and hold-for-Bluetooth) aren't in
the ortho drawing — noted at the top of the YAML.

## Build

```sh
cd totem && bash scripts/build-local.sh      # ZMK  (Docker)
cd 3w6   && ./build.sh                        # QMK  (Docker)
```

## Editing the layout

* **Move/assign a key:** edit the grid in [`layout/layers.py`](layout/layers.py).
  Changes apply to both boards automatically.
* **Add a new key/behavior:** add a canonical token to
  [`layout/names.py`](layout/names.py) with its ZMK and QMK expansion, then use it
  in a grid. Multi-key/tmux/Bluetooth behaviors also need their node (ZMK) or
  custom keycode (QMK) in the relevant `targets/` module.
* **tmux macros** must stay aligned with `~/.tmux/keybindings.conf`.
