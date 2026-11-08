"""
Open Source Location Data Visualizer - github.com/btc-git/OS-LOC-DAT-VIZ
Licensed under the GNU General Public License v3.0 - see LICENSE file for details
"""

import argparse
import struct
from pathlib import Path

from PyQt6.QtCore import QBuffer, QIODevice, Qt
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtSvg import QSvgRenderer


ICON_SIZES = (16, 20, 24, 32, 40, 48, 64, 96, 128, 256)
ROOT = Path(__file__).resolve().parent.parent


def build_icon_bytes():
    renderer = QSvgRenderer(str(ROOT / "wifi_icon.svg"))
    if not renderer.isValid():
        raise RuntimeError("Application icon SVG is missing or invalid")

    images = []
    for size in ICON_SIZES:
        image = QImage(size * 4, size * 4, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(image)
        renderer.render(painter)
        painter.end()
        image = image.scaled(
            size, size,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        image.setDotsPerMeterX(3780)
        image.setDotsPerMeterY(3780)
        buffer = QBuffer()
        if not buffer.open(QIODevice.OpenModeFlag.WriteOnly):
            raise RuntimeError("Could not open the icon image buffer")
        if not image.save(buffer, "PNG"):
            raise RuntimeError(f"Could not encode the {size}px icon")
        images.append(bytes(buffer.data()))

    offset = 6 + 16 * len(images)
    directory = bytearray(struct.pack("<HHH", 0, 1, len(images)))
    for size, image_bytes in zip(ICON_SIZES, images):
        dimension = size if size < 256 else 0
        directory.extend(struct.pack(
            "<BBBBHHII", dimension, dimension, 0, 0, 1, 32,
            len(image_bytes), offset,
        ))
        offset += len(image_bytes)
    return bytes(directory) + b"".join(images)


def main():
    parser = argparse.ArgumentParser(description="Generate the Windows/Qt application icon.")
    parser.add_argument("--check", action="store_true", help="Verify the ICO matches the SVG.")
    arguments = parser.parse_args()
    icon_path = ROOT / "wifi_icon.ico"
    icon_bytes = build_icon_bytes()
    if arguments.check:
        if not icon_path.is_file() or icon_path.read_bytes() != icon_bytes:
            raise RuntimeError("wifi_icon.ico does not match wifi_icon.svg; regenerate it")
        print("Application icon matches its SVG source.")
    else:
        icon_path.write_bytes(icon_bytes)
        print(f"Generated {icon_path.name}: {', '.join(map(str, ICON_SIZES))}px")


if __name__ == "__main__":
    main()
