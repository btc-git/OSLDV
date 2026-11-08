"""
Open Source Location Data Visualizer - github.com/btc-git/OSLDV
Licensed under the GNU General Public License v3.0 - see LICENSE file for details
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from license_dialog import LicenseDialog
from version import APP_VERSION

# License Label
class LicenseClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

class DisclaimerDialog(QDialog):


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Important Disclaimers")
        self.setModal(True)
        self.setMinimumSize(600, 430)
        self.setMaximumSize(800, 650)
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        # Header
        header_label = QLabel("Open Source Location Data Visualizer")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setStyleSheet("color: #0078d4; margin: 10px;")
        layout.addWidget(header_label)

        # Subtitle
        subtitle_label = QLabel("Important Disclaimers")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #cccccc; margin-bottom: 15px;")
        layout.addWidget(subtitle_label)

        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Disclaimer
        disclaimer_text = f"""
<div style='font-family: "Segoe UI", Arial, sans-serif; line-height: 1.6; padding: 15px;'>

<h3 style='color: #ff6b6b; margin-top: 0;'>In active development and testing</h3>
<p><strong>Not a validated forensic tool; verify all findings independently.</strong></p>
<ul>
    <li><strong>Preliminary visualization only:</strong> OSLDV is a location-data triage and visualization aid, not a validated forensic tool.</li>
    <li><strong>No RF coverage estimates:</strong> Shaded areas, wedges, circles, lines, and bands are visual aids only. They do not show radio signal coverage or calculate a device location.</li>
    <li>This software is in active development and testing and may contain errors.</li>
    <li>Verify all source values, settings, assumptions, conversions, visualizations, and findings independently before formal or legal use.</li>
    <li>Work from copies of original records and preserve the originals.</li>
    <li>OSLDV does not replace professional forensic analysis or expert review.</li>
    <li>OSLDV was developed with AI assistance and has undergone human review and testing. The program itself does not use AI.</li>
</ul>

<p>
Full disclaimers and documentation:
<a href="https://github.com/btc-git/OSLDV#readme" style="color:#4ecdc4;">README</a> &middot;
<a href="https://github.com/btc-git/OSLDV/tree/master/docs" style="color:#4ecdc4;">docs</a>
</p>

<p style='text-align: center; margin-top: 20px; color: #999999; font-style: italic;'>
Version {APP_VERSION}<br/>
Open Source Location Data Visualization Tool<br/>
<br/>
<strong>📜 Licenses &amp; Notices:</strong> <a href="license://show" style="color:#4ecdc4; text-decoration:underline; cursor:pointer;">View license texts</a><br/>
OSLDV is licensed under GNU GPL v3.0 and includes GeoLibre 3.7.0 under the MIT License.<br/>
</p>

</div>
                """

        disclaimer_label = QLabel(disclaimer_text)
        disclaimer_label.setWordWrap(True)
        disclaimer_label.setTextFormat(Qt.TextFormat.RichText)
        disclaimer_label.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                border: 1px solid #444444;
                border-radius: 8px;
                padding: 0px;
                margin: 0px;
            }
        """)
        disclaimer_label.setOpenExternalLinks(False)
        disclaimer_label.linkActivated.connect(self.handle_license_link)
        content_layout.addWidget(disclaimer_label)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # Buttons
        button_layout = QHBoxLayout()
        self.understand_button = QPushButton("Close")
        self.understand_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        self.understand_button.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(self.understand_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def handle_license_link(self, link):
        if link == "license://show":
            self.show_license_dialog()
        elif link.startswith("http://") or link.startswith("https://"):
            import webbrowser
            webbrowser.open(link)

    def show_license_dialog(self):
        self.license_window = LicenseDialog(self)
        self.license_window.show()

        # Dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QScrollArea {
                border: none;
                background-color: #2b2b2b;
            }
            QScrollBar:vertical {
                background-color: #404040;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #606060;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #707070;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator::unchecked {
                border: 2px solid #555555;
                border-radius: 3px;
                background-color: #2b2b2b;
            }
            QCheckBox::indicator::checked {
                border: 2px solid #0078d4;
                border-radius: 3px;
                background-color: #0078d4;
                image: url(data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3E%3Cpath d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/%3E%3C/svg%3E);
            }
        """)
