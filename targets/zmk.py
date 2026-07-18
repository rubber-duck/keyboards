"""ZMK definition module for the 38-key Totem (wireless).

Owns everything ZMK-specific: includes, layer indices, the ``&mt``/``&lt`` tuning,
the DTS ``macros {}`` node (tmux / multi-key delete / Bluetooth), and the keymap
wrapper.  The shared canonical layers are rendered by ``layout.engine``.
"""

from layout import engine
from layout.layers import GRIDS, LAYER_ORDER

OUTPUT = "totem/config/totem.keymap"
TARGET = "zmk"
OUTER_KEYS = True

_INCLUDES = """\
#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/outputs.h>
"""

# Hold-tap tuning shared by all &mt (home-row mods) and &lt (layer-taps).
_MT_TUNING = """\
&mt {
  quick-tap-ms = <100>;
  global-quick-tap;
  flavor = "tap-preferred";
  tapping-term-ms = <170>;
};
"""

# Behavior-macro nodes referenced (via #define) by the layers.  These are the
# multi-keystroke / Bluetooth behaviors that cannot be a plain #define alias.
_MACRO_NODES = """\
                // BT profile macros
                bt0_pc: bt0_pc {
                        compatible = "zmk,behavior-macro";
                        #binding-cells = <0>;
                        bindings = <&bt BT_SEL 0>, <&to COLEMAK_PC>;
                };
                bt1_mac: bt1_mac {
                        compatible = "zmk,behavior-macro";
                        #binding-cells = <0>;
                        bindings = <&bt BT_SEL 1>, <&to COLEMAK_MAC>;
                };
                bt2: bt2 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&bt BT_SEL 2>; };
                bt3: bt3 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&bt BT_SEL 3>; };
                bt4: bt4 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&bt BT_SEL 4>; };

                // Multi-step delete to line start/end macros
                pc_dlls: pc_dlls { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LS(HOME)>, <&kp BSPC>; };
                pc_dlle: pc_dlle { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LS(END)>, <&kp DEL>; };

                // tmux prefix macros. Keep these aligned with ~/.tmux/keybindings.conf.
                tm_w1: tm_w1 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N1>; };
                tm_w2: tm_w2 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N2>; };
                tm_w3: tm_w3 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N3>; };
                tm_w4: tm_w4 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N4>; };
                tm_w5: tm_w5 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N5>; };
                tm_w6: tm_w6 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N6>; };
                tm_w7: tm_w7 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N7>; };
                tm_w8: tm_w8 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N8>; };
                tm_w9: tm_w9 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N9>; };
                tm_w0: tm_w0 { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N0>; };
                tm_new: tm_new { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp C>; };
                tm_prev: tm_prev { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp P>; };
                tm_next: tm_next { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp N>; };
                tm_last: tm_last { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp L>; };
                tm_tree: tm_tree { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp W>; };
                tm_left: tm_left { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp LEFT>; };
                tm_down: tm_down { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp DOWN>; };
                tm_up: tm_up { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp UP>; };
                tm_right: tm_right { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp RIGHT>; };
                tm_splh: tm_splh { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp H>; };
                tm_splv: tm_splv { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp V>; };
                tm_zoom: tm_zoom { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp Z>; };
                tm_kill: tm_kill { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp X>; };
                tm_renm: tm_renm { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp COMMA>; };
                tm_det: tm_det { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp D>; };
                tm_rlft: tm_rlft { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp LS(H)>; };
                tm_rdwn: tm_rdwn { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp LS(J)>; };
                tm_rup: tm_rup { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp LS(K)>; };
                tm_rrgt: tm_rrgt { compatible = "zmk,behavior-macro"; #binding-cells = <0>; bindings = <&kp LC(A)>, <&kp LS(L)>; };
"""


def _layer_defines():
    return "\n".join(f"#define {key} {i}" for i, key in enumerate(LAYER_ORDER))


def render():
    header = "".join([
        _INCLUDES,
        "\n",
        _layer_defines(),
        "\n\n",
        engine.define_lines(TARGET),
        "\n",
        _MT_TUNING,
        "\n",
        "/ {\n",
        "        macros {\n",
        _MACRO_NODES,
        "        };\n",
        "\n",
        "        keymap {\n",
        '                compatible = "zmk,keymap";\n',
    ])

    body = ""
    for key in LAYER_ORDER:
        node = key.lower() + "_layer"
        label = key.replace("_", " ")
        body += "\n" + engine.format_zmk_layer(node, label, GRIDS[key]) + "\n"

    footer = "        };\n};\n"
    return header + body + footer
