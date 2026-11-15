"""
Open Source Location Data Visualizer - github.com/btc-git/OSLDV
Licensed under the GNU General Public License v3.0 - see LICENSE file for details
"""

from pathlib import Path

from PyQt6.QtCore import QStandardPaths


def default_open_directory():
    """Return a familiar, real directory for initial open dialogs."""
    desktop = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.DesktopLocation
    )
    if desktop and Path(desktop).is_dir():
        return desktop

    drive_root = Path.home().anchor
    if drive_root and Path(drive_root).is_dir():
        return drive_root
    return str(Path.home())


def suggested_save_path(filename, source_path=None):
    """Place a suggested output beside its source, or on the Desktop."""
    directory = (
        Path(source_path).parent
        if source_path
        else Path(default_open_directory())
    )
    return str(directory / filename)
