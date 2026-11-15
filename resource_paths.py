"""
Open Source Location Data Visualizer - github.com/btc-git/OSLDV
Licensed under the GNU General Public License v3.0 - see LICENSE file for details
"""

import sys
from pathlib import Path


def bundled_resource_path(relative_path):
    """Resolve a resource in a source checkout or a frozen PyInstaller app."""
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return bundle_root / relative_path
