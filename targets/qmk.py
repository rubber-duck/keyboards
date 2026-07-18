"""QMK definition module for the 36-key 3w6 (wired, RGB).

Owns everything QMK-specific: the license header, layer/custom-keycode enums, the
tmux command table, RGB indicators, OS auto-detection, and hold-tap handling.  The
shared canonical layers are rendered by ``layout.engine`` (``outer_keys=False`` so
the two Totem outer columns are dropped, giving 36 keys).

The Totem-only names ``TM_*`` (tmux) and ``PC_DLLS``/``PC_DLLE`` are C ``enum``
custom keycodes here rather than ``#define`` aliases, so the registry marks them as
identity for QMK and no ``#define`` is emitted for them.
"""

from layout import engine
from layout.layers import GRIDS

OUTPUT = "3w6/3w6_rgb/keymaps/default/keymap.c"
TARGET = "qmk"
OUTER_KEYS = False

_LICENSE = """\
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
"""

# Custom keycodes (multi-key macros + tmux).  Names match the canonical tokens,
# so the shared layers reference these enum members directly.
_ENUM_KEYCODES = """\
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
"""

# tmux command keys, indexed by (keycode - TMUX_FIRST).  Order matches the enum.
_TMUX_TABLE = """\
#define TMUX_FIRST TM_W1
#define TMUX_LAST TM_RRGT

static const uint16_t tmux_command_keys[] = {
    KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0,
    KC_C, KC_P, KC_N, KC_L, KC_W,
    KC_LEFT, KC_DOWN, KC_UP, KC_RIGHT,
    KC_H, KC_V, KC_Z, KC_X, KC_COMM, KC_D,
    S(KC_H), S(KC_J), S(KC_K), S(KC_L),
};
"""

_FOOTER = """\


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
"""


def _enum_layers():
    keys = engine.target_layers(TARGET)
    lines = ["enum layers", "{"]
    for i, k in enumerate(keys):
        lines.append(f"    _{k} = 0," if i == 0 else f"    _{k},")
    lines.append("};")
    return "\n".join(lines) + "\n"


def render():
    header = "".join([
        _LICENSE,
        "\n",
        _enum_layers(),
        "\n",
        _ENUM_KEYCODES,
        "\n",
        engine.define_lines(TARGET),
        "\n",
        _TMUX_TABLE,
    ])

    keys = engine.target_layers(TARGET)
    body = "const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {\n"
    for i, key in enumerate(keys):
        body += engine.format_qmk_layer(f"_{key}", GRIDS[key])
        if i < len(keys) - 1:
            body += "\n"
        body += "\n"
    body += "};"

    return header + body + _FOOTER
