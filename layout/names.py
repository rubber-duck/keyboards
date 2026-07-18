"""Canonical macro-name registry — the single source of truth.

Every cell in the shared layout grids (``layout/layers.py``) is a bare canonical
token.  This module maps each token to its per-target expansion:

    MACROS[name] = (zmk_expansion, qmk_expansion)

* ``zmk_expansion`` / ``qmk_expansion`` is the text a ``#define <name> <expansion>``
  emits for that target, i.e. what the token expands to in the generated keymap.
* ``None`` means the token is not used on that target (e.g. Bluetooth keys on QMK);
  no ``#define`` is emitted and the token must never appear in that target's layers.
* If the expansion string equals the canonical name itself, the target skips the
  ``#define`` (identity): the name is already a valid keycode / enum there.  This is
  how QMK's custom keycodes (tmux ``TM_*``, ``PC_DLLS``/``PC_DLLE``) are handled —
  they are C ``enum`` members, not ``#define`` aliases.

"Swap the definition part" == pick the zmk or qmk column.  The layout never changes.
"""

# ── Plain keypresses ──────────────────────────────────────────────────────────
# canonical -> (zmk keycode, qmk keycode).  ZMK wraps in "&kp", QMK prefixes "KC_"
# is already baked into the qmk value so divergent spellings live in one place.
_PLAIN = {}
for _c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    _PLAIN[f"K_{_c}"] = (_c, f"KC_{_c}")
for _d, _n in zip("1234567890", "1234567890"):
    _PLAIN[f"K_{_d}"] = (f"N{_n}", f"KC_{_n}")
for _f in range(1, 13):
    _PLAIN[f"K_F{_f}"] = (f"F{_f}", f"KC_F{_f}")
_PLAIN.update({
    # punctuation / symbols (unshifted) — ZMK spelling vs QMK spelling
    "K_QUOTE":  ("SQT",   "KC_QUOT"),
    "K_COMMA":  ("COMMA", "KC_COMM"),
    "K_DOT":    ("DOT",   "KC_DOT"),
    "K_SLASH":  ("FSLH",  "KC_SLSH"),
    "K_BSLASH": ("BSLH",  "KC_BSLS"),
    "K_SEMI":   ("SEMI",  "KC_SCLN"),
    "K_MINUS":  ("MINUS", "KC_MINS"),
    "K_EQUAL":  ("EQUAL", "KC_EQL"),
    "K_GRAVE":  ("GRAVE", "KC_GRV"),
    "K_LBKT":   ("LBKT",  "KC_LBRC"),
    "K_RBKT":   ("RBKT",  "KC_RBRC"),
    # navigation cluster
    "K_HOME":   ("HOME",  "KC_HOME"),
    "K_END":    ("END",   "KC_END"),
    "K_PGUP":   ("PG_UP", "KC_PGUP"),
    "K_PGDN":   ("PG_DN", "KC_PGDN"),
    "K_LEFT":   ("LEFT",  "KC_LEFT"),
    "K_DOWN":   ("DOWN",  "KC_DOWN"),
    "K_UP":     ("UP",    "KC_UP"),
    "K_RIGHT":  ("RIGHT", "KC_RIGHT"),
    # thumb / editing
    "K_ESC":    ("ESC",   "KC_ESC"),
    "K_SPACE":  ("SPACE", "KC_SPC"),
    "K_TAB":    ("TAB",   "KC_TAB"),
    "K_ENTER":  ("RET",   "KC_ENT"),
    "K_BSPC":   ("BSPC",  "KC_BSPC"),
    "K_DEL":    ("DEL",   "KC_DEL"),
    # outer-column keys (Totem only, dropped on 3w6)
    "K_LSHFT":  ("LSHFT", "KC_LSFT"),
    "K_LGUI":   ("LGUI",  "KC_LGUI"),
})

# ── Home-row mods (hold = mod, tap = letter) ──────────────────────────────────
_MODS = {
    "HM_A": ("&mt LGUI A",  "LGUI_T(KC_A)"),
    "HM_R": ("&mt LALT R",  "LALT_T(KC_R)"),
    "HM_S": ("&mt LCTRL S", "LCTL_T(KC_S)"),
    "HM_T": ("&mt LSHFT T", "LSFT_T(KC_T)"),
    "HM_N": ("&mt RSHFT N", "RSFT_T(KC_N)"),
    "HM_E": ("&mt RCTRL E", "RCTL_T(KC_E)"),
    "HM_I": ("&mt RALT I",  "RALT_T(KC_I)"),
    "HM_O": ("&mt RGUI O",  "RGUI_T(KC_O)"),
}

# ── Layer-taps (hold = layer, tap = key).  Layer id spelling differs per target. ──
_LAYERTAPS = {
    "LT_SHRT_PC":  ("&lt SHORTCUTS_PC ESC",   "LT(_SHORTCUTS_PC, KC_ESC)"),
    "LT_BRKT_PC":  ("&lt BRACKETS_PC SPACE",  "LT(_BRACKETS_PC, KC_SPC)"),
    "LT_NAV_PC":   ("&lt NAVIGATION_PC TAB",  "LT(_NAVIGATION_PC, KC_TAB)"),
    "LT_SHRT_MAC": ("&lt SHORTCUTS_MAC ESC",  "LT(_SHORTCUTS_MAC, KC_ESC)"),
    "LT_BRKT_MAC": ("&lt BRACKETS_MAC SPACE", "LT(_BRACKETS_MAC, KC_SPC)"),
    "LT_NAV_MAC":  ("&lt NAVIGATION_MAC TAB", "LT(_NAVIGATION_MAC, KC_TAB)"),
    "LT_NUM":      ("&lt NUMBERS RET",        "LT(_NUMBERS, KC_ENT)"),
    "LT_SYM":      ("&lt SYMBOLS BSPC",       "LT(_SYMBOLS, KC_BSPC)"),
    "LT_FN":       ("&lt FUNCTION DEL",       "LT(_FUNCTION, KC_DEL)"),
    "LT_TMUX_L":   ("&lt TMUX G",             "LT(_TMUX, KC_G)"),
    "LT_TMUX_R":   ("&lt TMUX M",             "LT(_TMUX, KC_M)"),
}

# ── Shifted symbols (single keypress with shift applied) ──────────────────────
_SYMBOLS = {
    "SY_AT":   ("&kp LS(N2)",    "LSFT(KC_2)"),
    "SY_DLR":  ("&kp LS(N4)",    "LSFT(KC_4)"),
    "SY_HASH": ("&kp LS(N3)",    "LSFT(KC_3)"),
    "SY_PERC": ("&kp LS(N5)",    "LSFT(KC_5)"),
    "SY_ASTR": ("&kp LS(N8)",    "LSFT(KC_8)"),
    "SY_AMPR": ("&kp LS(N7)",    "LSFT(KC_7)"),
    "SY_PIPE": ("&kp LS(BSLH)",  "LSFT(KC_BSLS)"),
    "SY_CRET": ("&kp LS(N6)",    "LSFT(KC_6)"),
    "SY_TILD": ("&kp LS(GRAVE)", "LSFT(KC_GRV)"),
    "SY_PLUS": ("&kp LS(EQUAL)", "LSFT(KC_EQL)"),
    "SY_UNDS": ("&kp LS(MINUS)", "LSFT(KC_MINS)"),
    "SY_QUES": ("&kp LS(FSLH)",  "LSFT(KC_SLSH)"),
    "SY_LABR": ("&kp LS(COMMA)", "LSFT(KC_COMM)"),
    "SY_RABR": ("&kp LS(DOT)",   "LSFT(KC_DOT)"),
    "SY_LCBR": ("&kp LS(LBKT)",  "LSFT(KC_LBRC)"),
    "SY_RCBR": ("&kp LS(RBKT)",  "LSFT(KC_RBRC)"),
    "SY_LPRN": ("&kp LS(N9)",    "LSFT(KC_9)"),
    "SY_RPRN": ("&kp LS(N0)",    "LSFT(KC_0)"),
    "SY_CLN":  ("&kp LS(SEMI)",  "LSFT(KC_SCLN)"),
    "SY_DQUO": ("&kp LS(SQT)",   "LSFT(KC_QUOT)"),
    "SY_EXCL": ("&kp LS(N1)",    "LSFT(KC_1)"),
}

# ── PC editor/OS actions (Ctrl-based).  Single keypresses unless noted. ────────
_ACTIONS_PC = {
    "PC_UNDO": ("&kp LC(Z)",        "C(KC_Z)"),
    "PC_CUT":  ("&kp LC(X)",        "C(KC_X)"),
    "PC_COPY": ("&kp LC(C)",        "C(KC_C)"),
    "PC_PSTE": ("&kp LC(V)",        "C(KC_V)"),
    "PC_REDO": ("&kp LC(LS(Z))",    "C(S(KC_Z))"),
    "PC_GOBK": ("&kp LA(LEFT)",     "A(KC_LEFT)"),
    "PC_WDLF": ("&kp LC(LEFT)",     "C(KC_LEFT)"),
    "PC_WDRT": ("&kp LC(RIGHT)",    "C(KC_RIGHT)"),
    "PC_GTBR": ("&kp LC(LS(BSLH))", "C(S(KC_BSLS))"),
    "PC_PRNT": ("&kp LC(P)",        "C(KC_P)"),
    "PC_GTLN": ("&kp LC(G)",        "C(KC_G)"),
    "PC_NVBK": ("&kp LC(MINUS)",    "C(KC_MINS)"),
    "PC_NVFW": ("&kp LC(EQUAL)",    "C(KC_EQL)"),
    "PC_SWFL": ("&kp LC(LS(O))",    "C(S(KC_O))"),
    "PC_CMDP": ("&kp LC(LS(P))",    "C(S(KC_P))"),
    "PC_SELA": ("&kp LC(A)",        "C(KC_A)"),
    "PC_SAVE": ("&kp LC(S)",        "C(KC_S)"),
    "PC_DLWD": ("&kp LC(BSPC)",     "C(KC_BSPC)"),
    "PC_DLFW": ("&kp LC(DEL)",      "C(KC_DEL)"),
    # multi-key: ZMK behavior-macro node, QMK custom keycode (identity → no #define)
    "PC_DLLS": ("&pc_dlls",         "PC_DLLS"),
    "PC_DLLE": ("&pc_dlle",         "PC_DLLE"),
    # shortcuts layer
    "PC_SCRN": ("&kp PSCRN",        "KC_PSCR"),
    "PC_LCMT": ("&kp LC(FSLH)",     "C(KC_SLSH)"),
    "PC_RPLA": ("&kp LC(LS(H))",    "C(S(KC_H))"),
    "PC_FNDA": ("&kp LC(LS(F))",    "C(S(KC_F))"),
    "PC_ZMIN": ("&kp LC(LS(EQUAL))", "C(S(KC_EQL))"),
    "PC_SREG": ("&kp LG(LS(S))",    "LGUI(S(KC_S))"),
    "PC_FMTD": ("&kp LS(LA(F))",    "LSA(KC_F)"),
    "PC_RPLC": ("&kp LC(H)",        "C(KC_H)"),
    "PC_FIND": ("&kp LC(F)",        "C(KC_F)"),
    "PC_ZMOT": ("&kp LC(MINUS)",    "C(KC_MINS)"),
    "PC_SREC": ("&kp LG(LA(R))",    "LGUI(A(KC_R))"),
    "PC_GDEF": ("&kp F12",          "KC_F12"),
    "PC_IMPL": ("&kp LC(F12)",      "C(KC_F12)"),
    "PC_QFIX": ("&kp LC(DOT)",      "C(KC_DOT)"),
    "PC_CTAB": ("&kp LC(W)",        "C(KC_W)"),
}

# ── Mac actions (Cmd/Gui-based mirror of the PC set) ──────────────────────────
_ACTIONS_MC = {
    "MC_UNDO": ("&kp LG(Z)",        "G(KC_Z)"),
    "MC_CUT":  ("&kp LG(X)",        "G(KC_X)"),
    "MC_COPY": ("&kp LG(C)",        "G(KC_C)"),
    "MC_PSTE": ("&kp LG(V)",        "G(KC_V)"),
    "MC_REDO": ("&kp LG(LS(Z))",    "G(S(KC_Z))"),
    "MC_GOBK": ("&kp LC(MINUS)",    "C(KC_MINS)"),
    "MC_WDLF": ("&kp LA(LEFT)",     "A(KC_LEFT)"),
    "MC_WDRT": ("&kp LA(RIGHT)",    "A(KC_RIGHT)"),
    "MC_GTBR": ("&kp LG(LS(BSLH))", "G(S(KC_BSLS))"),
    "MC_PRNT": ("&kp LG(P)",        "G(KC_P)"),
    "MC_GTLN": ("&kp LC(G)",        "C(KC_G)"),
    "MC_NVBK": ("&kp LG(MINUS)",    "G(KC_MINS)"),
    "MC_NVFW": ("&kp LG(EQUAL)",    "G(KC_EQL)"),
    "MC_SWFL": ("&kp LG(LS(O))",    "G(S(KC_O))"),
    "MC_CMDP": ("&kp LG(LS(P))",    "G(S(KC_P))"),
    "MC_SELA": ("&kp LG(A)",        "G(KC_A)"),
    "MC_SAVE": ("&kp LG(S)",        "G(KC_S)"),
    "MC_DLWD": ("&kp LA(BSPC)",     "A(KC_BSPC)"),
    "MC_DLFW": ("&kp LA(DEL)",      "A(KC_DEL)"),
    # Mac delete-to-line are single keycodes (no macro needed)
    "MC_DLLS": ("&kp LG(BSPC)",     "G(KC_BSPC)"),
    "MC_DLLE": ("&kp LC(K)",        "C(KC_K)"),
    # shortcuts layer
    "MC_SCRN": ("&kp LG(LS(N3))",   "G(S(KC_3))"),
    "MC_LCMT": ("&kp LG(FSLH)",     "G(KC_SLSH)"),
    "MC_RPLA": ("&kp LG(LS(H))",    "G(S(KC_H))"),
    "MC_FNDA": ("&kp LG(LS(F))",    "G(S(KC_F))"),
    "MC_ZMIN": ("&kp LG(LS(EQUAL))", "G(S(KC_EQL))"),
    "MC_SREG": ("&kp LG(LS(N4))",   "G(S(KC_4))"),
    "MC_FMTD": ("&kp LS(LA(F))",    "S(A(KC_F))"),
    "MC_RPLC": ("&kp LG(LA(F))",    "G(A(KC_F))"),
    "MC_FIND": ("&kp LG(F)",        "G(KC_F)"),
    "MC_ZMOT": ("&kp LG(MINUS)",    "G(KC_MINS)"),
    "MC_SREC": ("&kp LG(LS(N5))",   "G(S(KC_5))"),
    "MC_GDEF": ("&kp F12",          "KC_F12"),
    "MC_IMPL": ("&kp LG(F12)",      "G(KC_F12)"),
    "MC_QFIX": ("&kp LG(DOT)",      "G(KC_DOT)"),
    "MC_CTAB": ("&kp LG(W)",        "G(KC_W)"),
}

# ── tmux prefix macros (Ctrl-A then a key).  ZMK behavior-macro node vs QMK
#    custom keycode (identity → no #define; the enum carries the name). ─────────
_TMUX = {}
for _cn, _node in {
    "TM_W1": "tm_w1", "TM_W2": "tm_w2", "TM_W3": "tm_w3", "TM_W4": "tm_w4",
    "TM_W5": "tm_w5", "TM_W6": "tm_w6", "TM_W7": "tm_w7", "TM_W8": "tm_w8",
    "TM_W9": "tm_w9", "TM_W0": "tm_w0",
    "TM_NEW": "tm_new", "TM_PREV": "tm_prev", "TM_NEXT": "tm_next",
    "TM_LAST": "tm_last", "TM_TREE": "tm_tree",
    "TM_LEFT": "tm_left", "TM_DOWN": "tm_down", "TM_UP": "tm_up", "TM_RGHT": "tm_right",
    "TM_SPLH": "tm_splh", "TM_SPLV": "tm_splv", "TM_ZOOM": "tm_zoom",
    "TM_KILL": "tm_kill", "TM_RENM": "tm_renm", "TM_DET": "tm_det",
    "TM_RLFT": "tm_rlft", "TM_RDWN": "tm_rdwn", "TM_RUP": "tm_rup", "TM_RRGT": "tm_rrgt",
}.items():
    _TMUX[_cn] = (f"&{_node}", _cn)  # QMK: identity, name is the enum member

# ── Base-layer switches ───────────────────────────────────────────────────────
_SWITCHES = {
    "TO_PC":   ("&to COLEMAK_PC",    "DF(_COLEMAK_PC)"),
    "TO_MAC":  ("&to COLEMAK_MAC",   "DF(_COLEMAK_MAC)"),
    "TO_GAME": ("&to QWERTY_GAMING", "DF(_QWERTY_GAMING)"),
    "MO_BT":   ("&mo BLUETOOTH",     None),  # Totem-only (wireless); no QMK equivalent
}

# ── Bluetooth layer keys (Totem/ZMK only) ─────────────────────────────────────
_BT = {
    "BT0_PC":  ("&bt0_pc",       None),
    "BT1_MAC": ("&bt1_mac",      None),
    "BT2":     ("&bt2",          None),
    "BT3":     ("&bt3",          None),
    "BT4":     ("&bt4",          None),
    # Renamed to avoid shadowing ZMK's built-in BT_CLR / OUT_TOG macros
    "BT_CLEAR":  ("&bt BT_CLR",   None),
    "OUT_TOGGLE": ("&out OUT_TOG", None),
    "SYS_RST": ("&sys_reset",    None),
    "BOOTLDR": ("&bootloader",   None),
}

# ── Special ───────────────────────────────────────────────────────────────────
_SPECIAL = {
    "TRANS": ("&trans", "KC_TRNS"),
    "NONE":  ("&none",  "KC_NO"),
}


def _zmk_plain(code):
    return f"&kp {code}"


# Plain keys become their final (zmk, qmk) form; other groups already hold it.
_PLAIN_MACROS = {n: (_zmk_plain(z), q) for n, (z, q) in _PLAIN.items()}

# Ordered sections — drives readable, grouped #define output per target.
SECTIONS = [
    ("Plain keys",            _PLAIN_MACROS),
    ("Home-row mods",         _MODS),
    ("Layer-taps",            _LAYERTAPS),
    ("Shifted symbols",       _SYMBOLS),
    ("PC actions",            _ACTIONS_PC),
    ("Mac actions",           _ACTIONS_MC),
    ("tmux macros",           _TMUX),
    ("Base-layer switches",   _SWITCHES),
    ("Bluetooth (Totem)",     _BT),
    ("Special",               _SPECIAL),
]

# Assemble the full registry: canonical -> (zmk, qmk)
MACROS = {}
for _title, _group in SECTIONS:
    MACROS.update(_group)


def expansion(name, target):
    """Return the (target) expansion string for a canonical token, or None."""
    pair = MACROS[name]
    return pair[0] if target == "zmk" else pair[1]
