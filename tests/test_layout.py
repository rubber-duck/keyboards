"""Checks that work without the retired per-board repositories or firmware SDKs."""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check_equivalence
import generate
from layout import engine, names
from layout.layers import GRIDS


class GeneratedFilesTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        root_patch = patch.object(generate, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        quiet = contextlib.redirect_stdout(io.StringIO())
        quiet.__enter__()
        self.addCleanup(quiet.__exit__, None, None, None)

    def test_check_missing_files_fails_without_writing(self):
        self.assertEqual(generate.main(["all", "--check"]), 1)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_check_detects_stale_output_without_repairing_it(self):
        self.assertEqual(generate.main(["all"]), 0)
        self.assertEqual(generate.main(["all", "--check"]), 0)
        output = self.root / generate.TARGETS["3w6"].OUTPUT
        output.write_text("stale keymap\n")
        self.assertEqual(generate.main(["all", "--check"]), 1)
        self.assertEqual(output.read_text(), "stale keymap\n")

    def test_every_layer_has_the_board_key_count_and_valid_bindings(self):
        for target, count in (("qmk", 36), ("zmk", 38)):
            for layer in engine.target_layers(target):
                with self.subTest(target=target, layer=layer):
                    cells = list(engine.iter_cells(GRIDS[layer], target == "zmk"))
                    self.assertEqual(len(cells), count)
                    for token in cells:
                        self.assertIsNotNone(names.expansion(token, target))


class MigrationTest(unittest.TestCase):
    def compare(self, kind, old, new):
        with contextlib.redirect_stdout(io.StringIO()):
            return check_equivalence.compare(kind, old, new)

    def test_home_row_tmux_move_is_accepted_for_both_boards(self):
        for kind, old_keys, new_keys in (
            ("qmk", ["LT(_TMUX, KC_B)", "LT(_TMUX, KC_J)", "KC_G", "KC_M"],
             ["KC_B", "KC_J", "LT(_TMUX, KC_G)", "LT(_TMUX, KC_M)"]),
            ("zmk", ["&lt TMUX B", "&lt TMUX J", "&kp G", "&kp M"],
             ["&kp B", "&kp J", "&lt TMUX G", "&lt TMUX M"]),
        ):
            for layer in ("COLEMAK_PC", "COLEMAK_MAC"):
                with self.subTest(kind=kind, layer=layer):
                    old, new = ["unchanged"] * 36, ["unchanged"] * 36
                    for i, before, after in zip((4, 5, 14, 15), old_keys, new_keys):
                        old[i], new[i] = before, after
                    self.assertTrue(self.compare(kind, {layer: old}, {layer: new}))
                    new[14] = "unexpected binding"
                    self.assertFalse(self.compare(kind, {layer: old}, {layer: new}))

    def test_relocation_exception_does_not_apply_to_other_layers(self):
        old, new = ["unchanged"] * 36, ["unchanged"] * 36
        old[4], new[4] = "&lt TMUX B", "&kp B"
        self.assertFalse(self.compare("zmk", {"QWERTY_GAMING": old}, {"QWERTY_GAMING": new}))

    def test_layer_addition_removal_and_key_count_changes_fail(self):
        old = {"SYMBOLS": ["KC_A"] * 36}
        for new in ({}, {**old, "EXTRA": []}, {"SYMBOLS": ["KC_A"] * 35}):
            with self.subTest(new=new):
                self.assertFalse(self.compare("qmk", old, new))


if __name__ == "__main__":
    unittest.main()
