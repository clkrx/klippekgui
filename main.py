import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt, QTimer, QDateTime, QSize
from PySide6.QtGui import QIcon, QPixmap, QFontDatabase, QFont


class KlippekGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Frameless window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setWindowTitle("Klippek v0.0.1")
        self.setGeometry(50, 50, 1400, 900)
        self.setMinimumSize(900, 600)

        # Track drag for frameless window
        self._drag_pos = None

        # Resolve asset path relative to this script
        self._base_dir = os.path.dirname(os.path.abspath(__file__))

        # Load custom font, fall back to Arial / Segoe UI
        font_path = os.path.join(self._base_dir, "LexendDecaFont.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            self.custom_font_family = families[0] if families else "Segoe UI"
        else:
            self.custom_font_family = "Segoe UI"

        # ── Central widget ──────────────────────────────────────────────
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #1a2a2a;")

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(20, 18, 20, 20)
        root_layout.setSpacing(6)

        # ── Top row: nav bar (left) + clock (right) ────────────────────
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        # Nav-bar container (rounded rectangle, dark bg, subtle border)
        nav_container = QFrame()
        nav_container.setFixedHeight(64)
        nav_container.setStyleSheet("""
            QFrame {
                background-color: #0f1c1c;
                border: 1px solid #2a3f3f;
                border-radius: 14px;
            }
        """)
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(10, 6, 10, 6)
        nav_layout.setSpacing(6)

        # Five navigation icon buttons
        icon_map = [
            ("mainlogo.png", "Home"),
            ("clipbutton.png", "Clips"),
            ("rewardbutton.png", "Rewards"),
            ("socialbutton.png", "Social"),
            ("settingsbutton.png", "Settings"),
        ]

        nav_button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 10px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #1e3838;
            }
            QPushButton:pressed {
                background-color: #142a2a;
            }
        """

        for icon_file, tooltip in icon_map:
            btn = QPushButton()
            icon_path = os.path.join(self._base_dir, icon_file)
            btn.setIcon(QIcon(icon_path))
            # Use a slightly smaller size for the logo to keep it proportional
            if icon_file == "mainlogo.png":
                btn.setIconSize(QSize(44, 44))
                btn.setFixedSize(50, 50)
            else:
                btn.setIconSize(QSize(34, 34))
                btn.setFixedSize(46, 46)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(nav_button_style)
            btn.setCursor(Qt.PointingHandCursor)
            nav_layout.addWidget(btn)

        top_row.addWidget(nav_container)
        top_row.addStretch()

        # Clock / date label (top-right, orange-gold)
        self.datetime_label = QLabel()
        self.datetime_label.setStyleSheet(f"""
            color: #FFA726;
            font-size: 34px;
            font-weight: bold;
            font-family: '{self.custom_font_family}', 'Segoe UI', Arial, sans-serif;
            background-color: transparent;
        """)
        self.datetime_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_row.addWidget(self.datetime_label)

        root_layout.addLayout(top_row)

        # ── Purple accent label ─────────────────────────────────────────
        accent_label = QLabel("✦ Main Window")
        accent_label.setStyleSheet(f"""
            color: #9b59b6;
            font-size: 14px;
            font-weight: bold;
            font-family: '{self.custom_font_family}', 'Segoe UI', Arial, sans-serif;
            padding-left: 6px;
            background-color: transparent;
        """)
        root_layout.addWidget(accent_label)

        # Fill remaining space (content area placeholder)
        root_layout.addStretch()

        # ── Close / minimize bar (bottom-right, since frameless) ───────
        controls_row = QHBoxLayout()
        controls_row.addStretch()

        ctrl_btn_style = f"""
            QPushButton {{
                background-color: #0f1c1c;
                color: #aaaaaa;
                border: 1px solid #2a3f3f;
                border-radius: 8px;
                padding: 6px 18px;
                font-size: 13px;
                font-family: '{self.custom_font_family}', 'Segoe UI', Arial, sans-serif;
            }}
            QPushButton:hover {{
                background-color: #1e3838;
                color: #ffffff;
            }}
        """

        minimize_btn = QPushButton("—")
        minimize_btn.setFixedSize(44, 32)
        minimize_btn.setStyleSheet(ctrl_btn_style)
        minimize_btn.setCursor(Qt.PointingHandCursor)
        minimize_btn.clicked.connect(self.showMinimized)
        controls_row.addWidget(minimize_btn)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(44, 32)
        close_btn.setStyleSheet(ctrl_btn_style.replace("#1e3838", "#5c2020"))
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        controls_row.addWidget(close_btn)

        root_layout.addLayout(controls_row)

        # ── Timer for live clock ────────────────────────────────────────
        self.update_datetime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)

    # ── Live clock: HH:MM - M/DD/YYYY ──────────────────────────────────
    def update_datetime(self):
        now = QDateTime.currentDateTime()
        formatted = now.toString("HH:mm - M/dd/yyyy")
        self.datetime_label.setText(formatted)

    # ── Frameless window dragging ───────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    # ── Double-click title area to toggle maximized ─────────────────────
    def mouseDoubleClickEvent(self, event):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


def main():
    app = QApplication(sys.argv)

    # Global application stylesheet
    app.setStyleSheet("""
        QToolTip {
            background-color: #0f1c1c;
            color: #cccccc;
            border: 1px solid #2a3f3f;
            padding: 4px 8px;
            font-size: 12px;
        }
    """)

    window = KlippekGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
