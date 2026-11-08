"""
Open Source Location Data Visualizer - github.com/btc-git/OS-LOC-DAT-VIZ
Licensed under the GNU General Public License v3.0 - see LICENSE file for details
"""

import os
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication

from main_window import MainWindow
from tools.generate_app_icon import ICON_SIZES, build_icon_bytes


class ApplicationIconTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_icon_matches_vector_source(self):
        icon_path = Path(__file__).resolve().parent.parent / "wifi_icon.ico"
        self.assertEqual(build_icon_bytes(), icon_path.read_bytes())

    def test_window_icon_has_native_sizes_and_fills_small_title_icon(self):
        window = MainWindow()
        self.addCleanup(window.close)
        icon = window.windowIcon()
        self.assertEqual(
            {QSize(size, size) for size in ICON_SIZES},
            set(icon.availableSizes()),
        )
        for size in ICON_SIZES:
            with self.subTest(size=size):
                self.assertEqual(QSize(size, size), icon.pixmap(size, size).size())

        image = icon.pixmap(16, 16).toImage()
        visible_pixels = [
            (x, y) for y in range(16) for x in range(16)
            if image.pixelColor(x, y).alpha() >= 128
        ]
        xs, ys = zip(*visible_pixels)
        self.assertGreaterEqual(max(xs) - min(xs) + 1, 14)
        self.assertGreaterEqual(max(ys) - min(ys) + 1, 13)
        self.assertEqual(0, image.pixelColor(0, 0).alpha())
        self.assertEqual(QSize(64, 64), icon.pixmap(QSize(32, 32), 2.0).size())

    def test_missing_icon_fails_explicitly(self):
        with patch("main_window.bundled_resource_path", return_value=Path("missing-icon.ico")):
            with self.assertRaisesRegex(RuntimeError, "icon is missing or invalid"):
                MainWindow()


if __name__ == "__main__":
    unittest.main()
