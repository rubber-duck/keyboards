/* Copyright 2021 weteor
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include QMK_KEYBOARD_H
#include "os_detection.h"

enum layers
{
    _COLEMAK_PC = 0,
    _COLEMAK_MAC,
    _QWERTY_GAMING,
    _SYMBOLS,
    _BRACKETS_PC,
    _BRACKETS_MAC,
    _NUMBERS,
    _NAVIGATION_PC,
    _NAVIGATION_MAC,
    _SHORTCUTS_PC,
    _SHORTCUTS_MAC,
    _TMUX,
    _FUNCTION,
};

// Custom keycodes for multi-key macros
enum custom_keycodes {
    PC_DLLS = SAFE_RANGE, // Delete to line start (Shift+Home, Backspace)
    PC_DLLE,              // Delete to line end (Shift+End, Delete)
    TM_W1,
    TM_W2,
    TM_W3,
    TM_W4,
    TM_W5,
    TM_W6,
    TM_W7,
    TM_W8,
    TM_W9,
    TM_W0,
    TM_NEW,
    TM_PREV,
    TM_NEXT,
    TM_LAST,
    TM_TREE,
    TM_LEFT,
    TM_DOWN,
    TM_UP,
    TM_RGHT,
    TM_SPLH,
    TM_SPLV,
    TM_ZOOM,
    TM_KILL,
    TM_RENM,
    TM_DET,
    TM_RLFT,
    TM_RDWN,
    TM_RUP,
    TM_RRGT,
};

// Plain keys
#define K_A KC_A
#define K_B KC_B
#define K_C KC_C
#define K_D KC_D
#define K_E KC_E
#define K_F KC_F
#define K_G KC_G
#define K_H KC_H
#define K_I KC_I
#define K_J KC_J
#define K_K KC_K
#define K_L KC_L
#define K_M KC_M
#define K_N KC_N
#define K_O KC_O
#define K_P KC_P
#define K_Q KC_Q
#define K_R KC_R
#define K_S KC_S
#define K_T KC_T
#define K_U KC_U
#define K_V KC_V
#define K_W KC_W
#define K_X KC_X
#define K_Y KC_Y
#define K_Z KC_Z
#define K_1 KC_1
#define K_2 KC_2
#define K_3 KC_3
#define K_4 KC_4
#define K_5 KC_5
#define K_6 KC_6
#define K_7 KC_7
#define K_8 KC_8
#define K_9 KC_9
#define K_0 KC_0
#define K_F1 KC_F1
#define K_F2 KC_F2
#define K_F3 KC_F3
#define K_F4 KC_F4
#define K_F5 KC_F5
#define K_F6 KC_F6
#define K_F7 KC_F7
#define K_F8 KC_F8
#define K_F9 KC_F9
#define K_F10 KC_F10
#define K_F11 KC_F11
#define K_F12 KC_F12
#define K_QUOTE KC_QUOT
#define K_COMMA KC_COMM
#define K_DOT KC_DOT
#define K_SLASH KC_SLSH
#define K_BSLASH KC_BSLS
#define K_SEMI KC_SCLN
#define K_MINUS KC_MINS
#define K_EQUAL KC_EQL
#define K_GRAVE KC_GRV
#define K_LBKT KC_LBRC
#define K_RBKT KC_RBRC
#define K_HOME KC_HOME
#define K_END KC_END
#define K_PGUP KC_PGUP
#define K_PGDN KC_PGDN
#define K_LEFT KC_LEFT
#define K_DOWN KC_DOWN
#define K_UP KC_UP
#define K_RIGHT KC_RIGHT
#define K_ESC KC_ESC
#define K_SPACE KC_SPC
#define K_TAB KC_TAB
#define K_ENTER KC_ENT
#define K_BSPC KC_BSPC
#define K_DEL KC_DEL

// Home-row mods
#define HM_A LGUI_T(KC_A)
#define HM_R LALT_T(KC_R)
#define HM_S LCTL_T(KC_S)
#define HM_T LSFT_T(KC_T)
#define HM_N RSFT_T(KC_N)
#define HM_E RCTL_T(KC_E)
#define HM_I RALT_T(KC_I)
#define HM_O RGUI_T(KC_O)

// Layer-taps
#define LT_SHRT_PC LT(_SHORTCUTS_PC, KC_ESC)
#define LT_BRKT_PC LT(_BRACKETS_PC, KC_SPC)
#define LT_NAV_PC LT(_NAVIGATION_PC, KC_TAB)
#define LT_SHRT_MAC LT(_SHORTCUTS_MAC, KC_ESC)
#define LT_BRKT_MAC LT(_BRACKETS_MAC, KC_SPC)
#define LT_NAV_MAC LT(_NAVIGATION_MAC, KC_TAB)
#define LT_NUM LT(_NUMBERS, KC_ENT)
#define LT_SYM LT(_SYMBOLS, KC_BSPC)
#define LT_FN LT(_FUNCTION, KC_DEL)
#define LT_TMUX_L LT(_TMUX, KC_G)
#define LT_TMUX_R LT(_TMUX, KC_M)

// Shifted symbols
#define SY_AT LSFT(KC_2)
#define SY_DLR LSFT(KC_4)
#define SY_HASH LSFT(KC_3)
#define SY_PERC LSFT(KC_5)
#define SY_ASTR LSFT(KC_8)
#define SY_AMPR LSFT(KC_7)
#define SY_PIPE LSFT(KC_BSLS)
#define SY_CRET LSFT(KC_6)
#define SY_TILD LSFT(KC_GRV)
#define SY_PLUS LSFT(KC_EQL)
#define SY_UNDS LSFT(KC_MINS)
#define SY_QUES LSFT(KC_SLSH)
#define SY_LABR LSFT(KC_COMM)
#define SY_RABR LSFT(KC_DOT)
#define SY_LCBR LSFT(KC_LBRC)
#define SY_RCBR LSFT(KC_RBRC)
#define SY_LPRN LSFT(KC_9)
#define SY_RPRN LSFT(KC_0)
#define SY_CLN LSFT(KC_SCLN)
#define SY_DQUO LSFT(KC_QUOT)
#define SY_EXCL LSFT(KC_1)

// PC actions
#define PC_UNDO C(KC_Z)
#define PC_CUT C(KC_X)
#define PC_COPY C(KC_C)
#define PC_PSTE C(KC_V)
#define PC_REDO C(S(KC_Z))
#define PC_GOBK A(KC_LEFT)
#define PC_WDLF C(KC_LEFT)
#define PC_WDRT C(KC_RIGHT)
#define PC_GTBR C(S(KC_BSLS))
#define PC_PRNT C(KC_P)
#define PC_GTLN C(KC_G)
#define PC_NVBK C(KC_MINS)
#define PC_NVFW C(KC_EQL)
#define PC_SWFL C(S(KC_O))
#define PC_CMDP C(S(KC_P))
#define PC_SELA C(KC_A)
#define PC_SAVE C(KC_S)
#define PC_DLWD C(KC_BSPC)
#define PC_DLFW C(KC_DEL)
#define PC_SCRN KC_PSCR
#define PC_LCMT C(KC_SLSH)
#define PC_RPLA C(S(KC_H))
#define PC_FNDA C(S(KC_F))
#define PC_ZMIN C(S(KC_EQL))
#define PC_SREG LGUI(S(KC_S))
#define PC_FMTD LSA(KC_F)
#define PC_RPLC C(KC_H)
#define PC_FIND C(KC_F)
#define PC_ZMOT C(KC_MINS)
#define PC_SREC LGUI(A(KC_R))
#define PC_GDEF KC_F12
#define PC_IMPL C(KC_F12)
#define PC_QFIX C(KC_DOT)
#define PC_CTAB C(KC_W)

// Mac actions
#define MC_UNDO G(KC_Z)
#define MC_CUT G(KC_X)
#define MC_COPY G(KC_C)
#define MC_PSTE G(KC_V)
#define MC_REDO G(S(KC_Z))
#define MC_GOBK C(KC_MINS)
#define MC_WDLF A(KC_LEFT)
#define MC_WDRT A(KC_RIGHT)
#define MC_GTBR G(S(KC_BSLS))
#define MC_PRNT G(KC_P)
#define MC_GTLN C(KC_G)
#define MC_NVBK G(KC_MINS)
#define MC_NVFW G(KC_EQL)
#define MC_SWFL G(S(KC_O))
#define MC_CMDP G(S(KC_P))
#define MC_SELA G(KC_A)
#define MC_SAVE G(KC_S)
#define MC_DLWD A(KC_BSPC)
#define MC_DLFW A(KC_DEL)
#define MC_DLLS G(KC_BSPC)
#define MC_DLLE C(KC_K)
#define MC_SCRN G(S(KC_3))
#define MC_LCMT G(KC_SLSH)
#define MC_RPLA G(S(KC_H))
#define MC_FNDA G(S(KC_F))
#define MC_ZMIN G(S(KC_EQL))
#define MC_SREG G(S(KC_4))
#define MC_FMTD S(A(KC_F))
#define MC_RPLC G(A(KC_F))
#define MC_FIND G(KC_F)
#define MC_ZMOT G(KC_MINS)
#define MC_SREC G(S(KC_5))
#define MC_GDEF KC_F12
#define MC_IMPL G(KC_F12)
#define MC_QFIX G(KC_DOT)
#define MC_CTAB G(KC_W)

// Base-layer switches
#define TO_PC DF(_COLEMAK_PC)
#define TO_MAC DF(_COLEMAK_MAC)
#define TO_GAME DF(_QWERTY_GAMING)

// Special
#define TRANS KC_TRNS
#define NONE KC_NO

#define TMUX_FIRST TM_W1
#define TMUX_LAST TM_RRGT

static const uint16_t tmux_command_keys[] = {
    KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0,
    KC_C, KC_P, KC_N, KC_L, KC_W,
    KC_LEFT, KC_DOWN, KC_UP, KC_RIGHT,
    KC_H, KC_V, KC_Z, KC_X, KC_COMM, KC_D,
    S(KC_H), S(KC_J), S(KC_K), S(KC_L),
};
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [_COLEMAK_PC] = LAYOUT_split_3x5_3(
        K_Q,   K_W,   K_F,         K_P,         K_B,            K_J,        K_L,     K_U,      K_Y,    K_QUOTE,
        HM_A,  HM_R,  HM_S,        HM_T,        LT_TMUX_L,      LT_TMUX_R,  HM_N,    HM_E,     HM_I,   HM_O,
        K_Z,   K_X,   K_C,         K_D,         K_V,            K_K,        K_H,     K_COMMA,  K_DOT,  K_SLASH,
                      LT_SHRT_PC,  LT_BRKT_PC,  LT_NAV_PC,      LT_NUM,     LT_SYM,  LT_FN
    ),

    [_COLEMAK_MAC] = LAYOUT_split_3x5_3(
        K_Q,   K_W,   K_F,          K_P,          K_B,             K_J,        K_L,     K_U,      K_Y,    K_QUOTE,
        HM_A,  HM_R,  HM_S,         HM_T,         LT_TMUX_L,       LT_TMUX_R,  HM_N,    HM_E,     HM_I,   HM_O,
        K_Z,   K_X,   K_C,          K_D,          K_V,             K_K,        K_H,     K_COMMA,  K_DOT,  K_SLASH,
                      LT_SHRT_MAC,  LT_BRKT_MAC,  LT_NAV_MAC,      LT_NUM,     LT_SYM,  LT_FN
    ),

    [_QWERTY_GAMING] = LAYOUT_split_3x5_3(
        K_Q,  K_W,  K_E,    K_R,      K_T,        K_Y,      K_U,     K_I,      K_O,    K_P,
        K_A,  K_S,  K_D,    K_F,      K_G,        K_H,      K_J,     K_K,      K_L,    K_SEMI,
        K_Z,  K_X,  K_C,    K_V,      K_B,        K_N,      K_M,     K_COMMA,  K_DOT,  K_SLASH,
                    K_ESC,  K_SPACE,  K_TAB,      K_ENTER,  K_BSPC,  K_DEL
    ),

    [_SYMBOLS] = LAYOUT_split_3x5_3(
        SY_AT,    SY_DLR,   SY_HASH,  SY_PERC,   SY_ASTR,      SY_ASTR,  SY_PERC,   SY_HASH,  SY_DLR,   SY_AT,
        SY_AMPR,  SY_PIPE,  SY_CRET,  K_BSLASH,  K_SLASH,      K_SLASH,  K_BSLASH,  SY_CRET,  SY_PIPE,  SY_AMPR,
        SY_TILD,  SY_PLUS,  K_MINUS,  SY_UNDS,   SY_QUES,      SY_QUES,  SY_UNDS,   K_MINUS,  SY_PLUS,  SY_TILD,
                            NONE,     NONE,      NONE,         NONE,     NONE,      NONE
    ),

    [_BRACKETS_PC] = LAYOUT_split_3x5_3(
        K_LBKT,   K_RBKT,   SY_LABR,  SY_RABR,  SY_CLN,       SY_CLN,   SY_LABR,  SY_RABR,  K_LBKT,   K_RBKT,
        SY_LCBR,  SY_RCBR,  SY_LPRN,  SY_RPRN,  K_SEMI,       K_SEMI,   SY_LPRN,  SY_RPRN,  SY_LCBR,  SY_RCBR,
        K_GRAVE,  K_QUOTE,  SY_DQUO,  SY_EXCL,  K_EQUAL,      K_EQUAL,  SY_EXCL,  SY_DQUO,  K_QUOTE,  K_GRAVE,
                            NONE,     NONE,     NONE,         NONE,     PC_DLWD,  PC_DLFW
    ),

    [_BRACKETS_MAC] = LAYOUT_split_3x5_3(
        K_LBKT,   K_RBKT,   SY_LABR,  SY_RABR,  SY_CLN,       SY_CLN,   SY_LABR,  SY_RABR,  K_LBKT,   K_RBKT,
        SY_LCBR,  SY_RCBR,  SY_LPRN,  SY_RPRN,  K_SEMI,       K_SEMI,   SY_LPRN,  SY_RPRN,  SY_LCBR,  SY_RCBR,
        K_GRAVE,  K_QUOTE,  SY_DQUO,  SY_EXCL,  K_EQUAL,      K_EQUAL,  SY_EXCL,  SY_DQUO,  K_QUOTE,  K_GRAVE,
                            NONE,     NONE,     NONE,         NONE,     MC_DLWD,  MC_DLFW
    ),

    [_NUMBERS] = LAYOUT_split_3x5_3(
        SY_ASTR,  K_9,  K_8,      K_7,    SY_PLUS,      SY_PLUS,  K_7,    K_8,      K_9,  SY_ASTR,
        K_SLASH,  K_6,  K_5,      K_4,    K_MINUS,      K_MINUS,  K_4,    K_5,      K_6,  K_SLASH,
        K_0,      K_3,  K_2,      K_1,    K_EQUAL,      K_EQUAL,  K_1,    K_2,      K_3,  K_0,
                        K_COMMA,  K_DOT,  K_ENTER,      NONE,     K_DOT,  K_COMMA
    ),

    [_NAVIGATION_PC] = LAYOUT_split_3x5_3(
        PC_UNDO,  PC_CUT,   PC_COPY,  PC_PSTE,  PC_REDO,      PC_GOBK,  PC_WDLF,  PC_GTBR,  PC_GTBR,  PC_WDRT,
        K_HOME,   K_PGDN,   K_PGUP,   K_END,    PC_PRNT,      PC_PRNT,  K_LEFT,   K_DOWN,   K_UP,     K_RIGHT,
        PC_GTLN,  PC_NVBK,  PC_NVFW,  PC_SWFL,  PC_CMDP,      PC_CMDP,  PC_SWFL,  PC_NVFW,  PC_NVBK,  PC_GTLN,
                            PC_SELA,  PC_SAVE,  NONE,         NONE,     PC_DLLS,  PC_DLLE
    ),

    [_NAVIGATION_MAC] = LAYOUT_split_3x5_3(
        MC_UNDO,  MC_CUT,   MC_COPY,  MC_PSTE,  MC_REDO,      MC_GOBK,  MC_WDLF,  MC_GTBR,  MC_GTBR,  MC_WDRT,
        K_HOME,   K_PGDN,   K_PGUP,   K_END,    MC_PRNT,      MC_PRNT,  K_LEFT,   K_DOWN,   K_UP,     K_RIGHT,
        MC_GTLN,  MC_NVBK,  MC_NVFW,  MC_SWFL,  MC_CMDP,      MC_CMDP,  MC_SWFL,  MC_NVFW,  MC_NVBK,  MC_GTLN,
                            MC_SELA,  MC_SAVE,  NONE,         NONE,     MC_DLLS,  MC_DLLE
    ),

    [_SHORTCUTS_PC] = LAYOUT_split_3x5_3(
        PC_SCRN,  PC_LCMT,  PC_RPLA,  PC_FNDA,  PC_ZMIN,      PC_ZMIN,  PC_FNDA,  PC_RPLA,  PC_LCMT,  PC_SCRN,
        PC_SREG,  PC_FMTD,  PC_RPLC,  PC_FIND,  PC_ZMOT,      PC_ZMOT,  PC_FIND,  PC_RPLC,  PC_FMTD,  PC_SREG,
        PC_SREC,  PC_GDEF,  PC_IMPL,  PC_QFIX,  PC_CTAB,      PC_CTAB,  PC_QFIX,  PC_IMPL,  PC_GDEF,  PC_SREC,
                            TRANS,    TRANS,    TRANS,        TRANS,    TRANS,    TRANS
    ),

    [_SHORTCUTS_MAC] = LAYOUT_split_3x5_3(
        MC_SCRN,  MC_LCMT,  MC_RPLA,  MC_FNDA,  MC_ZMIN,      MC_ZMIN,  MC_FNDA,  MC_RPLA,  MC_LCMT,  MC_SCRN,
        MC_SREG,  MC_FMTD,  MC_RPLC,  MC_FIND,  MC_ZMOT,      MC_ZMOT,  MC_FIND,  MC_RPLC,  MC_FMTD,  MC_SREG,
        MC_SREC,  MC_GDEF,  MC_IMPL,  MC_QFIX,  MC_CTAB,      MC_CTAB,  MC_QFIX,  MC_IMPL,  MC_GDEF,  MC_SREC,
                            TRANS,    TRANS,    TRANS,        TRANS,    TRANS,    TRANS
    ),

    [_TMUX] = LAYOUT_split_3x5_3(
        TM_W1,    TM_W2,    TM_W3,    TM_W4,    TM_W5,        TM_W6,    TM_W7,    TM_W8,    TM_W9,   TM_W0,
        TM_NEW,   TM_PREV,  TM_NEXT,  TM_LAST,  TM_TREE,      TM_TREE,  TM_LEFT,  TM_DOWN,  TM_UP,   TM_RGHT,
        TM_SPLH,  TM_SPLV,  TM_ZOOM,  TM_KILL,  TM_RENM,      TM_DET,   TM_RLFT,  TM_RDWN,  TM_RUP,  TM_RRGT,
                            TRANS,    TRANS,    TRANS,        TRANS,    TRANS,    TRANS
    ),

    [_FUNCTION] = LAYOUT_split_3x5_3(
        TO_PC,    K_F9,  K_F8,  K_F7,  K_F10,      K_F10,  K_F7,  K_F8,  K_F9,  TO_PC,
        TO_MAC,   K_F6,  K_F5,  K_F4,  K_F11,      K_F11,  K_F4,  K_F5,  K_F6,  TO_MAC,
        TO_GAME,  K_F3,  K_F2,  K_F1,  K_F12,      K_F12,  K_F1,  K_F2,  K_F3,  TO_GAME,
                         NONE,  NONE,  NONE,       NONE,   NONE,  NONE
    ),
};

// Define colors for layers
#define BASE_COLEMAK_PC_COLOR (RGB){0, 0, 50}
#define BASE_COLEMAK_MAC_COLOR (RGB){50, 50, 50}
#define BASE_QWERTY_GAMING_COLOR (RGB){50, 0, 0}
#define NUMBERS_LAYER_COLOR (RGB){255, 128, 0}
#define FUNCTION_LAYER_COLOR (RGB){50, 50, 0}
#define SYMBOLS_LAYER_COLOR (RGB){0, 50, 0}
#define BRACKETS_LAYER_COLOR (RGB){0, 50, 50}
#define NAVIGATION_LAYER_COLOR (RGB){50, 0, 50}
#define SHORTCUTS_LAYER_COLOR (RGB){25, 0, 50}
#define TMUX_LAYER_COLOR (RGB){80, 45, 0}
#define MODIFIER_COLOR (RGB){80, 0, 0}

// LED indices for thumb keys
const uint8_t thumb_keys[] = {15, 16, 17, 18, 19, 20};

// LED indices for home row modifier keys
const uint8_t gui_keys[] = {9, 26};
const uint8_t alt_keys[] = {8, 27};
const uint8_t ctrl_keys[] = {7, 28};
const uint8_t shift_keys[] = {6, 29};

// LED indices for function layer base layer switch keys
const uint8_t fn_pc_key[] = {0, 35};
const uint8_t fn_mac_key[] = {9, 26};
const uint8_t fn_gaming_key[] = {10, 25};

void set_color(RGB rgb) {
    rgb_matrix_set_color_all(rgb.r, rgb.g, rgb.b);
}

void set_keys_color(const uint8_t* keys, uint8_t num_keys, RGB rgb) {
    for (uint8_t i = 0; i < num_keys; i++) {
        rgb_matrix_set_color(keys[i], rgb.r, rgb.g, rgb.b);
    }
}

bool rgb_matrix_indicators_user(void) {
    RGB base_color;
    uint8_t current_base_layer = get_highest_layer(default_layer_state);

    switch (current_base_layer) {
        case _COLEMAK_MAC:
            base_color = BASE_COLEMAK_MAC_COLOR;
            break;
        case _QWERTY_GAMING:
            base_color = BASE_QWERTY_GAMING_COLOR;
            break;
        case _COLEMAK_PC:
        default:
            base_color = BASE_COLEMAK_PC_COLOR;
            break;
    }

    uint8_t current_layer = get_highest_layer(layer_state);
    RGB layer_color;

    switch (current_layer) {
        case _NUMBERS:
            layer_color = NUMBERS_LAYER_COLOR;
            break;
        case _FUNCTION:
            layer_color = FUNCTION_LAYER_COLOR;
            break;
        case _SYMBOLS:
            layer_color = SYMBOLS_LAYER_COLOR;
            break;
        case _BRACKETS_PC:
        case _BRACKETS_MAC:
            layer_color = BRACKETS_LAYER_COLOR;
            break;
        case _NAVIGATION_PC:
        case _NAVIGATION_MAC:
            layer_color = NAVIGATION_LAYER_COLOR;
            break;
        case _SHORTCUTS_PC:
        case _SHORTCUTS_MAC:
            layer_color = SHORTCUTS_LAYER_COLOR;
            break;
        case _TMUX:
            layer_color = TMUX_LAYER_COLOR;
            break;
        default:
            layer_color = base_color;
            break;
    }

    set_color(layer_color);
    set_keys_color(thumb_keys, ARRAY_SIZE(thumb_keys), base_color);

    if (current_layer == _FUNCTION) {
        set_keys_color(fn_pc_key, ARRAY_SIZE(fn_pc_key), BASE_COLEMAK_PC_COLOR);
        set_keys_color(fn_mac_key, ARRAY_SIZE(fn_mac_key), BASE_COLEMAK_MAC_COLOR);
        set_keys_color(fn_gaming_key, ARRAY_SIZE(fn_gaming_key), BASE_QWERTY_GAMING_COLOR);
    }

    uint8_t mods = get_mods();
    if (mods & MOD_MASK_SHIFT) {
        set_keys_color(shift_keys, ARRAY_SIZE(shift_keys), MODIFIER_COLOR);
    }
    if (mods & MOD_MASK_CTRL) {
        set_keys_color(ctrl_keys, ARRAY_SIZE(ctrl_keys), MODIFIER_COLOR);
    }
    if (mods & MOD_MASK_ALT) {
        set_keys_color(alt_keys, ARRAY_SIZE(alt_keys), MODIFIER_COLOR);
    }
    if (mods & MOD_MASK_GUI) {
        set_keys_color(gui_keys, ARRAY_SIZE(gui_keys), MODIFIER_COLOR);
    }

    return false;
}

void keyboard_post_init_user(void) {
    rgb_matrix_enable();
    rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR);
    rgb_matrix_set_flags(LED_FLAG_ALL);
    rgb_matrix_indicators_user();
}

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (keycode >= TMUX_FIRST && keycode <= TMUX_LAST) {
        if (record->event.pressed) {
            tap_code16(C(KC_A));
            tap_code16(tmux_command_keys[keycode - TMUX_FIRST]);
        }
        return false;
    }

    switch (keycode) {
        // Multi-key macros
        case PC_DLLS:
            if (record->event.pressed) {
                tap_code16(S(KC_HOME));
                tap_code(KC_BSPC);
            }
            return false;
        case PC_DLLE:
            if (record->event.pressed) {
                tap_code16(S(KC_END));
                tap_code(KC_DEL);
            }
            return false;
        // RGB update triggers
        case HM_A:
        case HM_R:
        case HM_S:
        case HM_T:
        case HM_N:
        case HM_E:
        case HM_I:
        case HM_O:
        case LT_SHRT_PC:
        case LT_SHRT_MAC:
        case LT_BRKT_PC:
        case LT_BRKT_MAC:
        case LT_NAV_PC:
        case LT_NAV_MAC:
        case LT_NUM:
        case LT_SYM:
        case LT_FN:
        case LT_TMUX_L:
        case LT_TMUX_R:
            rgb_matrix_indicators_user();
            break;
    }
    return true;
}

bool process_detected_host_os_kb(os_variant_t detected_os) {
    if (!process_detected_host_os_user(detected_os)) {
        return false;
    }

    switch (detected_os) {
        case OS_MACOS:
        case OS_IOS:
            default_layer_set(1UL << _COLEMAK_MAC);
            break;
        case OS_WINDOWS:
        case OS_LINUX:
        default:
            default_layer_set(1UL << _COLEMAK_PC);
            break;
    }
    rgb_matrix_indicators_user();
    return true;
}

layer_state_t layer_state_set_user(layer_state_t state) {
    rgb_matrix_indicators_user();
    return state;
}

layer_state_t default_layer_state_set_user(layer_state_t state) {
    rgb_matrix_indicators_user();
    return state;
}

bool get_permissive_hold(uint16_t keycode, keyrecord_t *record) {
    switch (keycode) {
        case HM_T:
        case HM_N:
        case LT_SHRT_PC:
        case LT_SHRT_MAC:
        case LT_BRKT_PC:
        case LT_BRKT_MAC:
        case LT_NAV_PC:
        case LT_NAV_MAC:
        case LT_NUM:
        case LT_SYM:
        case LT_FN:
        case LT_TMUX_L:
        case LT_TMUX_R:
            return true;
        default:
            return false;
    }
}
