"""
Open Source Location Data Visualizer - github.com/btc-git/OSLDV
Licensed under the GNU General Public License v3.0 - see LICENSE file for details
"""

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def heading_anchors(text):
    anchors = set()
    counts = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        slug = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(f"{slug}-{count}" if count else slug)
    return anchors


class DocumentationTests(unittest.TestCase):
    def test_readme_keeps_basic_import_and_stable_release_guidance(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        how_to_use = readme.split("## How to Use\n", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(
            ["1", "2", "3", "4", "5", "6", "7"],
            re.findall(r"^(\d+)\. ", how_to_use, re.MULTILINE),
        )
        for action in (
            "Browse for File", "Import Original Records", "Markers",
            "Process", "Process and Open in Viewer", "Open Viewer",
            "Load GeoJSON", "TXT log",
        ):
            with self.subTest(action=action):
                self.assertIn(action, how_to_use)
        self.assertIn(
            "Download and run `OSLDV.exe` (see [Download](#download)).",
            how_to_use,
        )
        self.assertIn("(docs/TECHNICAL.md)", how_to_use)
        self.assertIn(
            "[Download OSLDV.exe]"
            "(https://github.com/btc-git/OSLDV/releases/latest/download/OSLDV.exe)",
            readme,
        )
        self.assertIn(
            "In active development and testing. Not a validated forensic tool; "
            "verify all findings independently.",
            readme,
        )
        self.assertIn(
            "OSLDV is a preliminary location-data triage and visualization aid.",
            readme,
        )
        for disclaimer in (
            "continuous development and may contain errors",
            "visual aids only and are not RF coverage estimates",
            "Verify all findings independently",
            "Work from copies of original records",
            "not a replacement for professional forensic analysis",
        ):
            with self.subTest(disclaimer=disclaimer):
                self.assertIn(disclaimer, readme)
        self.assertNotRegex(
            readme, r"(?i)\b(?:beta|pre-release|prerelease|development preview)\b"
        )
        for guide in ("TECHNICAL", "EXPORTING", "BUILDING"):
            self.assertIn(f"(docs/{guide}.md)", readme)

    def test_build_guide_keeps_locked_spec_and_test_commands(self):
        guide = (ROOT / "docs" / "BUILDING.md").read_text(encoding="utf-8")
        self.assertIn("Python 3.11.3", guide)
        for command in (
            "python -m pip install -r requirements.txt",
            "python app.py",
            "python -m pip install -r requirements-build.txt",
            "python -m PyInstaller --clean app.spec",
            "python -m unittest discover -s tests -v",
            "node tests/test_plugin_simplified_chrome.mjs",
            "node --check tools/plugin_performance_harness.mjs",
        ):
            with self.subTest(command=command):
                self.assertIn(command, guide)
        self.assertIn("Always build through `app.spec`", guide)
        self.assertIn("`OSLDV.exe`", guide)

    def test_technical_reference_retains_removed_dialog_guidance(self):
        technical = (ROOT / "docs" / "TECHNICAL.md").read_text(encoding="utf-8")
        for detail in (
            "wedge is 120 degrees wide and extends 1 mile",
            "does not establish that a device",
            "Azimuth is measured in degrees",
            "including both endpoints",
            "OSLDV does not upload source",
            "user's IP address",
            "viewed map area",
        ):
            with self.subTest(detail=detail):
                self.assertIn(detail, technical)

    def test_local_documentation_links_and_anchors_resolve(self):
        documents = [
            *ROOT.glob("*.md"),
            *(ROOT / "docs").glob("*.md"),
            ROOT / ".github" / "copilot-instructions.md",
            *(ROOT / name / "README.md" for name in (
                "tests", "tools", "GeoLibre-Plugin", "GeoLibre-Viewer",
            )),
        ]
        for document in documents:
            text = document.read_text(encoding="utf-8")
            links = re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", text)
            links += re.findall(r'\b(?:href|src)="([^"]+)"', text)
            for link in links:
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc:
                    continue
                with self.subTest(document=document.relative_to(ROOT), link=link):
                    target = (
                        (document.parent / unquote(parsed.path)).resolve()
                        if parsed.path else document
                    )
                    self.assertTrue(target.is_relative_to(ROOT), target)
                    self.assertTrue(target.exists(), target)
                    if parsed.fragment and target.suffix == ".md":
                        self.assertIn(
                            unquote(parsed.fragment),
                            heading_anchors(target.read_text(encoding="utf-8")),
                        )


if __name__ == "__main__":
    unittest.main()
