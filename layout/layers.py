"""Shared canonical layout — defined once, generated for every keyboard.

Each layer is a 14-column x 4-row grid of canonical tokens (see ``names.py``).
Column convention (ZMK Totem native; 3w6 drops the two outer columns):

    col  0      = outer_l   (Totem only)
    cols 1-5    = left half
    cols 6-7    = centre gap (always empty)
    cols 8-12   = right half
    col  13     = outer_r   (Totem only)

Row 3 is the thumb cluster: the six thumb keys live in cols 4-9.
Empty positions are "".  A target emits the non-empty cells in row-major reading
order; with ``outer_keys=False`` it also skips cols 0/13, yielding 36 keys (3w6)
instead of 38 (Totem).  The grids themselves are identical for both boards.
"""

# Layer index order — shared by both targets (QMK omits the Totem-only tail).
LAYER_ORDER = [
    "COLEMAK_PC", "COLEMAK_MAC", "QWERTY_GAMING", "SYMBOLS",
    "BRACKETS_PC", "BRACKETS_MAC", "NUMBERS", "NAVIGATION_PC", "NAVIGATION_MAC",
    "SHORTCUTS_PC", "SHORTCUTS_MAC", "TMUX", "FUNCTION", "BLUETOOTH",
]

# Layers that exist only on boards with outer columns / wireless (Totem).
TOTEM_ONLY = {"BLUETOOTH"}

_E = ""  # empty grid position

GRIDS = {
    "COLEMAK_PC": [
        [_E,       "K_Q",  "K_W",  "K_F",  "K_P",  "K_B",       _E, _E, "K_J",       "K_L",  "K_U",     "K_Y",   "K_QUOTE", _E],
        [_E,       "HM_A", "HM_R", "HM_S", "HM_T", "LT_TMUX_L", _E, _E, "LT_TMUX_R", "HM_N", "HM_E",    "HM_I",  "HM_O",    _E],
        ["K_LSHFT", "K_Z", "K_X",  "K_C",  "K_D",  "K_V",       _E, _E, "K_K",       "K_H",  "K_COMMA", "K_DOT", "K_SLASH", "MO_BT"],
        [_E,       _E,     _E,     _E,     "LT_SHRT_PC", "LT_BRKT_PC", "LT_NAV_PC", "LT_NUM", "LT_SYM", "LT_FN", _E, _E, _E, _E],
    ],
    "COLEMAK_MAC": [
        [_E,       "K_Q",  "K_W",  "K_F",  "K_P",  "K_B",       _E, _E, "K_J",       "K_L",  "K_U",     "K_Y",   "K_QUOTE", _E],
        [_E,       "HM_A", "HM_R", "HM_S", "HM_T", "LT_TMUX_L", _E, _E, "LT_TMUX_R", "HM_N", "HM_E",    "HM_I",  "HM_O",    _E],
        ["K_LSHFT", "K_Z", "K_X",  "K_C",  "K_D",  "K_V",       _E, _E, "K_K",       "K_H",  "K_COMMA", "K_DOT", "K_SLASH", "MO_BT"],
        [_E,       _E,     _E,     _E,     "LT_SHRT_MAC", "LT_BRKT_MAC", "LT_NAV_MAC", "LT_NUM", "LT_SYM", "LT_FN", _E, _E, _E, _E],
    ],
    "QWERTY_GAMING": [
        [_E,      "K_Q", "K_W", "K_E", "K_R", "K_T", _E, _E, "K_Y", "K_U", "K_I",     "K_O",   "K_P",     _E],
        [_E,      "K_A", "K_S", "K_D", "K_F", "K_G", _E, _E, "K_H", "K_J", "K_K",     "K_L",   "K_SEMI",  _E],
        ["K_LGUI", "K_Z", "K_X", "K_C", "K_V", "K_B", _E, _E, "K_N", "K_M", "K_COMMA", "K_DOT", "K_SLASH", "MO_BT"],
        [_E,      _E,    _E,    _E,    "K_ESC", "K_SPACE", "K_TAB", "K_ENTER", "K_BSPC", "K_DEL", _E, _E, _E, _E],
    ],
    "SYMBOLS": [
        [_E,      "SY_AT",   "SY_DLR",  "SY_HASH", "SY_PERC",  "SY_ASTR", _E, _E, "SY_ASTR", "SY_PERC",  "SY_HASH", "SY_DLR",  "SY_AT",   _E],
        [_E,      "SY_AMPR", "SY_PIPE", "SY_CRET", "K_BSLASH", "K_SLASH", _E, _E, "K_SLASH", "K_BSLASH", "SY_CRET", "SY_PIPE", "SY_AMPR", _E],
        ["TRANS", "SY_TILD", "SY_PLUS", "K_MINUS", "SY_UNDS",  "SY_QUES", _E, _E, "SY_QUES", "SY_UNDS",  "K_MINUS", "SY_PLUS", "SY_TILD", "TRANS"],
        [_E,      _E,        _E,        _E,        "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", _E, _E, _E, _E],
    ],
    "BRACKETS_PC": [
        [_E,      "K_LBKT",  "K_RBKT",  "SY_LABR", "SY_RABR", "SY_CLN",  _E, _E, "SY_CLN",  "SY_LABR", "SY_RABR", "K_LBKT",  "K_RBKT",  _E],
        [_E,      "SY_LCBR", "SY_RCBR", "SY_LPRN", "SY_RPRN", "K_SEMI",  _E, _E, "K_SEMI",  "SY_LPRN", "SY_RPRN", "SY_LCBR", "SY_RCBR", _E],
        ["TRANS", "K_GRAVE", "K_QUOTE", "SY_DQUO", "SY_EXCL", "K_EQUAL", _E, _E, "K_EQUAL", "SY_EXCL", "SY_DQUO", "K_QUOTE", "K_GRAVE", "TRANS"],
        [_E,      _E,        _E,        _E,        "NONE", "NONE", "NONE", "NONE", "PC_DLWD", "PC_DLFW", _E, _E, _E, _E],
    ],
    "BRACKETS_MAC": [
        [_E,      "K_LBKT",  "K_RBKT",  "SY_LABR", "SY_RABR", "SY_CLN",  _E, _E, "SY_CLN",  "SY_LABR", "SY_RABR", "K_LBKT",  "K_RBKT",  _E],
        [_E,      "SY_LCBR", "SY_RCBR", "SY_LPRN", "SY_RPRN", "K_SEMI",  _E, _E, "K_SEMI",  "SY_LPRN", "SY_RPRN", "SY_LCBR", "SY_RCBR", _E],
        ["TRANS", "K_GRAVE", "K_QUOTE", "SY_DQUO", "SY_EXCL", "K_EQUAL", _E, _E, "K_EQUAL", "SY_EXCL", "SY_DQUO", "K_QUOTE", "K_GRAVE", "TRANS"],
        [_E,      _E,        _E,        _E,        "NONE", "NONE", "NONE", "NONE", "MC_DLWD", "MC_DLFW", _E, _E, _E, _E],
    ],
    "NUMBERS": [
        [_E,      "SY_ASTR", "K_9", "K_8", "K_7", "SY_PLUS",  _E, _E, "SY_PLUS",  "K_7", "K_8", "K_9", "SY_ASTR", _E],
        [_E,      "K_SLASH", "K_6", "K_5", "K_4", "K_MINUS",  _E, _E, "K_MINUS",  "K_4", "K_5", "K_6", "K_SLASH", _E],
        ["TRANS", "K_0",     "K_3", "K_2", "K_1", "K_EQUAL",  _E, _E, "K_EQUAL",  "K_1", "K_2", "K_3", "K_0",     "TRANS"],
        [_E,      _E,        _E,    _E,    "K_COMMA", "K_DOT", "K_ENTER", "NONE", "K_DOT", "K_COMMA", _E, _E, _E, _E],
    ],
    "NAVIGATION_PC": [
        [_E,      "PC_UNDO", "PC_CUT",  "PC_COPY", "PC_PSTE", "PC_REDO", _E, _E, "PC_GOBK", "PC_WDLF", "PC_GTBR", "PC_GTBR", "PC_WDRT", _E],
        [_E,      "K_HOME",  "K_PGDN",  "K_PGUP",  "K_END",   "PC_PRNT", _E, _E, "PC_PRNT", "K_LEFT",  "K_DOWN",  "K_UP",    "K_RIGHT", _E],
        ["TRANS", "PC_GTLN", "PC_NVBK", "PC_NVFW", "PC_SWFL", "PC_CMDP", _E, _E, "PC_CMDP", "PC_SWFL", "PC_NVFW", "PC_NVBK", "PC_GTLN", "TRANS"],
        [_E,      _E,        _E,        _E,        "PC_SELA", "PC_SAVE", "NONE", "NONE", "PC_DLLS", "PC_DLLE", _E, _E, _E, _E],
    ],
    "NAVIGATION_MAC": [
        [_E,      "MC_UNDO", "MC_CUT",  "MC_COPY", "MC_PSTE", "MC_REDO", _E, _E, "MC_GOBK", "MC_WDLF", "MC_GTBR", "MC_GTBR", "MC_WDRT", _E],
        [_E,      "K_HOME",  "K_PGDN",  "K_PGUP",  "K_END",   "MC_PRNT", _E, _E, "MC_PRNT", "K_LEFT",  "K_DOWN",  "K_UP",    "K_RIGHT", _E],
        ["TRANS", "MC_GTLN", "MC_NVBK", "MC_NVFW", "MC_SWFL", "MC_CMDP", _E, _E, "MC_CMDP", "MC_SWFL", "MC_NVFW", "MC_NVBK", "MC_GTLN", "TRANS"],
        [_E,      _E,        _E,        _E,        "MC_SELA", "MC_SAVE", "NONE", "NONE", "MC_DLLS", "MC_DLLE", _E, _E, _E, _E],
    ],
    "SHORTCUTS_PC": [
        [_E,      "PC_SCRN", "PC_LCMT", "PC_RPLA", "PC_FNDA", "PC_ZMIN", _E, _E, "PC_ZMIN", "PC_FNDA", "PC_RPLA", "PC_LCMT", "PC_SCRN", _E],
        [_E,      "PC_SREG", "PC_FMTD", "PC_RPLC", "PC_FIND", "PC_ZMOT", _E, _E, "PC_ZMOT", "PC_FIND", "PC_RPLC", "PC_FMTD", "PC_SREG", _E],
        ["TRANS", "PC_SREC", "PC_GDEF", "PC_IMPL", "PC_QFIX", "PC_CTAB", _E, _E, "PC_CTAB", "PC_QFIX", "PC_IMPL", "PC_GDEF", "PC_SREC", "TRANS"],
        [_E,      _E,        _E,        _E,        "TRANS", "TRANS", "TRANS", "TRANS", "TRANS", "TRANS", _E, _E, _E, _E],
    ],
    "SHORTCUTS_MAC": [
        [_E,      "MC_SCRN", "MC_LCMT", "MC_RPLA", "MC_FNDA", "MC_ZMIN", _E, _E, "MC_ZMIN", "MC_FNDA", "MC_RPLA", "MC_LCMT", "MC_SCRN", _E],
        [_E,      "MC_SREG", "MC_FMTD", "MC_RPLC", "MC_FIND", "MC_ZMOT", _E, _E, "MC_ZMOT", "MC_FIND", "MC_RPLC", "MC_FMTD", "MC_SREG", _E],
        ["TRANS", "MC_SREC", "MC_GDEF", "MC_IMPL", "MC_QFIX", "MC_CTAB", _E, _E, "MC_CTAB", "MC_QFIX", "MC_IMPL", "MC_GDEF", "MC_SREC", "TRANS"],
        [_E,      _E,        _E,        _E,        "TRANS", "TRANS", "TRANS", "TRANS", "TRANS", "TRANS", _E, _E, _E, _E],
    ],
    "TMUX": [
        [_E,      "TM_W1",   "TM_W2",   "TM_W3",   "TM_W4",   "TM_W5",   _E, _E, "TM_W6",  "TM_W7",   "TM_W8",   "TM_W9",   "TM_W0",   _E],
        [_E,      "TM_NEW",  "TM_PREV", "TM_NEXT", "TM_LAST", "TM_TREE", _E, _E, "TM_TREE", "TM_LEFT", "TM_DOWN", "TM_UP",   "TM_RGHT", _E],
        ["TRANS", "TM_SPLH", "TM_SPLV", "TM_ZOOM", "TM_KILL", "TM_RENM", _E, _E, "TM_DET",  "TM_RLFT", "TM_RDWN", "TM_RUP",  "TM_RRGT", "TRANS"],
        [_E,      _E,        _E,        _E,        "TRANS", "TRANS", "TRANS", "TRANS", "TRANS", "TRANS", _E, _E, _E, _E],
    ],
    "FUNCTION": [
        [_E,      "TO_PC",   "K_F9", "K_F8", "K_F7", "K_F10", _E, _E, "K_F10", "K_F7", "K_F8", "K_F9", "TO_PC",   _E],
        [_E,      "TO_MAC",  "K_F6", "K_F5", "K_F4", "K_F11", _E, _E, "K_F11", "K_F4", "K_F5", "K_F6", "TO_MAC",  _E],
        ["TRANS", "TO_GAME", "K_F3", "K_F2", "K_F1", "K_F12", _E, _E, "K_F12", "K_F1", "K_F2", "K_F3", "TO_GAME", "TRANS"],
        [_E,      _E,        _E,     _E,     "NONE", "NONE", "NONE", "NONE", "NONE", "NONE", _E, _E, _E, _E],
    ],
    "BLUETOOTH": [
        [_E,      "BT0_PC", "BT1_MAC", "BT2",     "BT3",     "BT4",   _E, _E, "TRANS", "TRANS", "TRANS", "TRANS", "TO_PC",   _E],
        [_E,      "TRANS",  "TRANS",   "TRANS",   "TRANS",   "TRANS", _E, _E, "TRANS", "TRANS", "TRANS", "TRANS", "TO_MAC",  _E],
        ["TRANS", "BT_CLEAR", "OUT_TOGGLE", "SYS_RST", "BOOTLDR", "TRANS", _E, _E, "TRANS", "TRANS", "TRANS", "TRANS", "TO_GAME", "TRANS"],
        [_E,      _E,       _E,        _E,        "TRANS", "TRANS", "TRANS", "TRANS", "TRANS", "TRANS", _E, _E, _E, _E],
    ],
}
