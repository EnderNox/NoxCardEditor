import sys
import os
import pandas as pd
import csv
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QScrollArea, QFormLayout, QLineEdit, QCheckBox,
                             QPushButton, QLabel, QFileDialog, QComboBox, QTabWidget,
                             QGroupBox, QTextEdit, QDialog, QMessageBox,
                             QFrame, QListWidgetItem, QToolButton)
from PySide6.QtCore import Qt, QRectF, QTimer, QSize
from PySide6.QtGui import (QPixmap, QImage, QPainter, QPen, QColor, QWheelEvent, QBrush,
                           QFont, QPalette, QShortcut, QKeySequence, QCursor, QIcon)
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsItem
import base64

_SVG_ICONS = {
    # Sidebar / rail nav
    "tab_info": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>""",
    "tab_all":  """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>""",
    "tab_combat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m11 19-6-6"/><path d="m5 21-2-2"/><path d="m8 16-4 4"/><path d="M9.5 17.5 21 6V3h-3L6.5 14.5"/></svg>""",
    "tab_spawn": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>""",
    "tab_icon": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>""",
    # Sidebar logo
    "logo": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 17H5"/><path d="M19 7h-9"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/></svg>""",
    # Category buttons
    "cat_chars": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>""",
    "cat_bldg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>""",
    "cat_spells": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/></svg>""",
    "cat_proj": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>""",
    # Action buttons
    "add":    """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>""",
    "dup":    """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>""",
    "delete": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>""",
    "save":   """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>""",
    "search": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>""",
    "load":   """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>""",
    "export": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>""",
}


def svg_pixmap(key: str, size: int = 20, color: str = "#EAE8E0") -> QPixmap:
    """Render an inline SVG icon to a QPixmap at the given size and color."""
    svg_src = _SVG_ICONS.get(key, "")
    if not svg_src:
        return QPixmap()
    svg_colored = svg_src.replace("{color}", color)
    svg_bytes = svg_colored.encode("utf-8")
    from PySide6.QtSvg import QSvgRenderer
    from PySide6.QtGui import QPixmap as _QPixmap
    renderer = QSvgRenderer(svg_bytes)
    px = QPixmap(size, size)
    px.fill(QColor(0, 0, 0, 0))
    painter = QPainter(px)
    renderer.render(painter)
    painter.end()
    return px


def svg_icon(key: str, size: int = 18, color: str = "#EAE8E0") -> QIcon:
    """Return a QIcon from an inline SVG."""
    from PySide6.QtGui import QIcon as _QIcon
    return QIcon(svg_pixmap(key, size, color))


# ─────────────────────────────────────────────
#  DESIGN TOKENS
# ─────────────────────────────────────────────
class Theme:
    # Backgrounds
    BG_BASE       = "#0D0F14"
    BG_PANEL      = "#13161E"
    BG_CARD       = "#1A1E2A"
    BG_ELEVATED   = "#21263A"
    BG_INPUT      = "#181C28"
    BG_INPUT_FOCUS= "#1E2333"

    # Accents
    GOLD          = "#F0B429"
    GOLD_DARK     = "#C8870A"
    GOLD_GLOW     = "#F0B42933"
    BLUE_ACT      = "#3D7BF0"
    BLUE_DIM      = "#2A56C6"
    RED_ACT       = "#E84040"
    RED_DIM       = "#A52020"
    GREEN_ACT     = "#27C45E"
    GREEN_DIM     = "#1A8A41"
    TEAL          = "#1AAFB8"

    # Text
    TEXT_PRIMARY  = "#EAE8E0"
    TEXT_SECONDARY= "#8A8EA8"
    TEXT_MUTED    = "#4D5270"
    TEXT_LABEL    = "#C0B890"

    # Borders
    BORDER        = "#262B3E"
    BORDER_ACTIVE = "#F0B42966"

    # Category colours (sidebar pills)
    CAT_CHARS     = "#4D9EF0"
    CAT_BLDG      = "#E07840"
    CAT_SPELL     = "#9B62E8"
    CAT_PROJ      = "#40C4C4"

    @staticmethod
    def cat_color(cat):
        return {
            "Characters":  Theme.CAT_CHARS,
            "Buildings":   Theme.CAT_BLDG,
            "Spells":      Theme.CAT_SPELL,
            "Projectiles": Theme.CAT_PROJ,
        }.get(cat, Theme.GOLD)

    @staticmethod
    def apply(app):
        palette = QPalette()
        palette.setColor(QPalette.Window,          QColor(Theme.BG_BASE))
        palette.setColor(QPalette.WindowText,      QColor(Theme.TEXT_PRIMARY))
        palette.setColor(QPalette.Base,            QColor(Theme.BG_INPUT))
        palette.setColor(QPalette.AlternateBase,   QColor(Theme.BG_CARD))
        palette.setColor(QPalette.Text,            QColor(Theme.TEXT_PRIMARY))
        palette.setColor(QPalette.Button,          QColor(Theme.BG_ELEVATED))
        palette.setColor(QPalette.ButtonText,      QColor(Theme.TEXT_PRIMARY))
        palette.setColor(QPalette.Highlight,       QColor(Theme.GOLD))
        palette.setColor(QPalette.HighlightedText, QColor(Theme.BG_BASE))
        palette.setColor(QPalette.PlaceholderText, QColor(Theme.TEXT_MUTED))
        palette.setColor(QPalette.ToolTipBase,     QColor(Theme.BG_ELEVATED))
        palette.setColor(QPalette.ToolTipText,     QColor(Theme.TEXT_PRIMARY))
        app.setPalette(palette)


# ─────────────────────────────────────────────
#  GLOBAL STYLESHEET
# ─────────────────────────────────────────────
STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {Theme.BG_BASE};
    color: {Theme.TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    font-size: 13px;
}}
/* ── Scrollbars ── */
QScrollBar:vertical {{
    background: {Theme.BG_BASE};
    width: 7px;
    margin: 0;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {Theme.BG_ELEVATED};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: {Theme.GOLD_DARK}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {Theme.BG_BASE};
    height: 7px;
    border-radius: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {Theme.BG_ELEVATED};
    border-radius: 3px;
    min-width: 30px;
}}
/* ── QLineEdit / QTextEdit ── */
QLineEdit, QTextEdit {{
    background-color: {Theme.BG_INPUT};
    border: 1px solid {Theme.BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    color: {Theme.TEXT_PRIMARY};
    selection-background-color: {Theme.GOLD_DARK};
}}
QLineEdit:focus, QTextEdit:focus {{
    border: 1px solid {Theme.GOLD};
    background-color: {Theme.BG_INPUT_FOCUS};
}}
QLineEdit:read-only {{
    color: {Theme.TEXT_SECONDARY};
    background-color: {Theme.BG_BASE};
    border: 1px solid {Theme.BORDER};
}}
/* ── QComboBox ── */
QComboBox {{
    background-color: {Theme.BG_INPUT};
    border: 1px solid {Theme.BORDER};
    border-radius: 6px;
    padding: 5px 10px;
    color: {Theme.TEXT_PRIMARY};
}}
QComboBox:hover {{ border-color: {Theme.GOLD_DARK}; }}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    image: none;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {Theme.TEXT_SECONDARY};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background: {Theme.BG_ELEVATED};
    border: 1px solid {Theme.BORDER};
    selection-background-color: {Theme.GOLD_DARK};
    outline: none;
    padding: 4px;
}}
/* ── QListWidget ── */
QListWidget {{
    background-color: {Theme.BG_PANEL};
    border: 1px solid {Theme.BORDER};
    border-radius: 8px;
    outline: none;
    padding: 4px;
}}
QListWidget::item {{
    border-radius: 5px;
    padding: 6px 10px;
    margin: 1px 2px;
    color: {Theme.TEXT_PRIMARY};
}}
QListWidget::item:hover {{
    background-color: {Theme.BG_ELEVATED};
}}
QListWidget::item:selected {{
    background-color: {Theme.GOLD_DARK};
    color: {Theme.BG_BASE};
    font-weight: 600;
}}
/* ── QTabWidget ── */
QTabWidget::pane {{
    border: 1px solid {Theme.BORDER};
    border-radius: 0 8px 8px 8px;
    background: {Theme.BG_PANEL};
    top: -1px;
}}
QTabBar::tab {{
    background: {Theme.BG_BASE};
    color: {Theme.TEXT_SECONDARY};
    border: 1px solid {Theme.BORDER};
    border-bottom: none;
    padding: 8px 18px;
    margin-right: 3px;
    border-radius: 7px 7px 0 0;
    font-size: 12px;
    font-weight: 500;
}}
QTabBar::tab:selected {{
    background: {Theme.BG_PANEL};
    color: {Theme.GOLD};
    border-color: {Theme.GOLD_DARK};
    font-weight: 700;
}}
QTabBar::tab:hover:!selected {{
    background: {Theme.BG_CARD};
    color: {Theme.TEXT_PRIMARY};
}}
/* ── QGroupBox ── */
QGroupBox {{
    border: 1px solid {Theme.BORDER};
    border-radius: 8px;
    margin-top: 14px;
    padding: 8px;
    color: {Theme.TEXT_LABEL};
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    top: 2px;
    background: {Theme.BG_PANEL};
    padding: 0 6px;
}}
/* ── QCheckBox ── */
QCheckBox {{
    spacing: 8px;
    color: {Theme.TEXT_PRIMARY};
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {Theme.BORDER};
    border-radius: 4px;
    background: {Theme.BG_INPUT};
}}
QCheckBox::indicator:checked {{
    background: {Theme.GOLD};
    border-color: {Theme.GOLD};
}}
QCheckBox::indicator:hover {{
    border-color: {Theme.GOLD_DARK};
}}
/* ── QSplitter ── */
QSplitter::handle {{
    background: {Theme.BORDER};
    width: 2px;
}}
QSplitter::handle:hover {{
    background: {Theme.GOLD_DARK};
}}
/* ── QScrollArea ── */
QScrollArea {{
    border: none;
    background: transparent;
}}
/* ── QStatusBar ── */
QStatusBar {{
    background: {Theme.BG_PANEL};
    color: {Theme.TEXT_SECONDARY};
    border-top: 1px solid {Theme.BORDER};
    font-size: 12px;
    padding: 3px 8px;
}}
/* ── QDialog ── */
QDialog {{
    background: {Theme.BG_PANEL};
}}
QDialogButtonBox QPushButton {{
    min-width: 80px;
}}
/* ── FormLayout labels ── */
QFormLayout QLabel {{
    color: {Theme.TEXT_SECONDARY};
    font-size: 12px;
    padding-right: 6px;
}}
"""


# ─────────────────────────────────────────────
#  HELPER: Styled Buttons
# ─────────────────────────────────────────────
def make_btn(label, color_bg, color_hover=None, icon_text=None, small=False):
    """Create a styled QPushButton with consistent look."""
    btn = QPushButton(label)
    if color_hover is None:
        color_hover = color_bg
    size = "9px 14px" if small else "8px 16px"
    font_size = "11px" if small else "13px"
    btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {color_bg};
            color: {'#0D0F14' if color_bg == Theme.GOLD else Theme.TEXT_PRIMARY};
            border: none;
            border-radius: 6px;
            padding: {size};
            font-weight: 600;
            font-size: {font_size};
        }}
        QPushButton:hover {{
            background-color: {color_hover};
        }}
        QPushButton:pressed {{
            opacity: 0.8;
        }}
        QPushButton:disabled {{
            background-color: {Theme.BG_ELEVATED};
            color: {Theme.TEXT_MUTED};
        }}
    """)
    return btn


def make_icon_btn(icon_key: str, tooltip: str, color: str = Theme.BG_ELEVATED,
                  icon_color: str = Theme.TEXT_PRIMARY, size: int = 18) -> QToolButton:
    """QToolButton with an SVG icon (no text, no emoji rendering issues)."""
    btn = QToolButton()
    btn.setIcon(svg_icon(icon_key, size, icon_color))
    btn.setIconSize(QSize(size, size))
    btn.setToolTip(tooltip)
    btn.setCursor(QCursor(Qt.PointingHandCursor))
    btn.setFixedSize(36, 36)
    btn.setStyleSheet(f"""
        QToolButton {{
            background: {color};
            border: 1px solid {Theme.BORDER};
            border-radius: 7px;
            padding: 0px;
        }}
        QToolButton:hover {{
            border-color: {Theme.GOLD_DARK};
            background: {Theme.BG_CARD};
        }}
        QToolButton:pressed {{
            background: {Theme.BG_BASE};
        }}
        QToolButton:disabled {{
            opacity: 0.35;
            border-color: {Theme.BORDER};
            background: {Theme.BG_BASE};
        }}
    """)
    return btn


def section_label(text):
    """Return a styled uppercase section header label."""
    lbl = QLabel(text.upper())
    lbl.setStyleSheet(f"""
        color: {Theme.TEXT_MUTED};
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
        padding: 0px 4px 4px 4px;
    """)
    return lbl


def separator():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"background: {Theme.BORDER}; max-height: 1px; margin: 4px 0;")
    return line


# ─────────────────────────────────────────────
#  CROPPER (unchanged logic, restyled widget)
# ─────────────────────────────────────────────
class ResizableRect(QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.setPen(QPen(QColor(Theme.GOLD), 2))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.handle_size = 14
        self.ratio = 196 / 250
        self.is_resizing = False

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.setBrush(QBrush(QColor(Theme.GOLD)))
        r = self.rect()
        painter.drawRect(r.right() - self.handle_size, r.bottom() - self.handle_size, self.handle_size, self.handle_size)
        # Corner guides
        pen = QPen(QColor(Theme.GOLD + "88"), 1, Qt.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

    def mousePressEvent(self, event):
        r = self.rect()
        handle_rect = QRectF(r.right() - self.handle_size, r.bottom() - self.handle_size, self.handle_size, self.handle_size)
        if handle_rect.contains(event.pos()):
            self.is_resizing = True
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_resizing:
            new_w = max(40, event.pos().x() - self.rect().left())
            new_h = new_w / self.ratio
            self.setRect(self.rect().left(), self.rect().top(), new_w, new_h)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.is_resizing = False
        super().mouseReleaseEvent(event)


class ImageCropper(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.pixmap_item = None
        self.selection_rect = None
        self.setAcceptDrops(True)
        self.setBackgroundBrush(QColor(Theme.BG_BASE))
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setStyleSheet(f"border: 1px solid {Theme.BORDER}; border-radius: 8px;")

    def wheelEvent(self, event: QWheelEvent):
        factor = 1.2 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files: self.load_image(files[0])

    def load_image(self, path):
        pixmap = QPixmap(path)
        if pixmap.isNull(): return
        self.scene.clear()
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.pixmap_item.setTransformationMode(Qt.SmoothTransformation)
        self.scene.addItem(self.pixmap_item)
        self.selection_rect = ResizableRect(0, 0, 196, 250)
        self.scene.addItem(self.selection_rect)
        self.setSceneRect(pixmap.rect())

    def get_cropped_image(self):
        if not self.pixmap_item or not self.selection_rect: return None
        self.selection_rect.setVisible(False)
        rect = self.selection_rect.rect().translated(self.selection_rect.pos())
        output = QImage(196, 250, QImage.Format_ARGB32)
        output.fill(Qt.transparent)
        painter = QPainter(output)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        self.scene.render(painter, target=QRectF(0, 0, 196, 250), source=rect)
        painter.end()
        self.selection_rect.setVisible(True)
        return output


# ─────────────────────────────────────────────
#  ADD / DUPLICATE DIALOG  (restyled)
# ─────────────────────────────────────────────
class AddCardDialog(QDialog):
    def __init__(self, parent=None, is_duplicate=False, source_name=""):
        super().__init__(parent)
        title = f"Duplicate  ›  {source_name}" if is_duplicate else "Add New Card"
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(520, 440)
        self.setStyleSheet(f"""
            QDialog {{
                background: {Theme.BG_PANEL};
                border: 1px solid {Theme.BORDER};
                border-radius: 12px;
            }}
            QLabel {{
                color: {Theme.TEXT_SECONDARY};
                font-size: 12px;
            }}
        """)
        self.is_duplicate = is_duplicate

        outer = QVBoxLayout(self)
        outer.setSpacing(0)
        outer.setContentsMargins(0, 0, 0, 0)

        # ── Header ──────────────────────────────
        header = QWidget()
        header.setStyleSheet(f"""
            background: {Theme.BG_CARD};
            border-radius: 10px 10px 0 0;
        """)
        hdr_layout = QHBoxLayout(header)
        hdr_layout.setContentsMargins(20, 16, 20, 16)
        icon_key = "dup" if is_duplicate else "add"
        icon_color = Theme.BLUE_ACT if is_duplicate else Theme.GREEN_ACT
        ico = QLabel()
        ico.setPixmap(svg_pixmap(icon_key, 22, icon_color))
        ico.setStyleSheet("background: transparent;")
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-size: 16px; font-weight: 700; background: transparent;")
        hdr_layout.addWidget(ico)
        hdr_layout.addWidget(title_lbl)
        hdr_layout.addStretch()
        outer.addWidget(header)

        # ── Form ────────────────────────────────
        body = QWidget()
        body.setStyleSheet(f"background: {Theme.BG_PANEL};")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(20, 20, 20, 10)
        body_layout.setSpacing(14)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Characters", "Buildings", "Spells", "Projectiles"])
        self.type_combo.currentIndexChanged.connect(self.on_type_change)
        if is_duplicate:
            self.type_combo.setEnabled(False)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g.  SuperKnight")
        self.name_edit.textChanged.connect(self.auto_fill)

        self.tid_edit = QLineEdit()
        self.tid_edit.setPlaceholderText("e.g.  TID_SPELL_SUPER_KNIGHT")

        self.game_name_edit = QLineEdit()
        self.game_name_edit.setPlaceholderText("e.g.  Super Knight")

        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("In-game description…")
        self.desc_edit.setMaximumHeight(80)

        self.info_lbl = QLabel("")
        self.info_lbl.setStyleSheet(f"color: {Theme.GOLD}; font-size: 11px;")

        def fl(text): 
            l = QLabel(text)
            l.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px;")
            return l

        form.addRow(fl("Type:"),         self.type_combo)
        form.addRow(fl("Internal ID:"),  self.name_edit)
        form.addRow(fl("Text Key TID:"), self.tid_edit)
        form.addRow(fl("Display Name:"), self.game_name_edit)
        form.addRow(fl("Description:"),  self.desc_edit)

        body_layout.addLayout(form)
        body_layout.addWidget(self.info_lbl)

        # ── Buttons ─────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 8, 0, 0)
        cancel_btn = make_btn("Cancel", Theme.BG_ELEVATED, Theme.BG_CARD)
        ok_btn = make_btn("✓  Confirm", Theme.GOLD, Theme.GOLD_DARK)
        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.accept)
        btn_row.addStretch()
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(ok_btn)
        body_layout.addLayout(btn_row)

        outer.addWidget(body)
        self.on_type_change()

    def on_type_change(self):
        t = self.type_combo.currentText()
        no_desc = t == "Projectiles"
        self.desc_edit.setEnabled(not no_desc)
        if no_desc:
            self.desc_edit.setPlaceholderText("Projectiles have no description.")
        else:
            self.desc_edit.setPlaceholderText("In-game description…")

    def auto_fill(self, text):
        if not text: return
        clean = text.upper().replace(" ", "_")
        if self.type_combo.currentText() == "Projectiles":
            self.tid_edit.setText(clean)
        else:
            self.tid_edit.setText(f"TID_SPELL_{clean}")
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', text)
        self.game_name_edit.setText(s1)

    def get_data(self):
        return {
            "type": self.type_combo.currentText(),
            "name": self.name_edit.text(),
            "tid": self.tid_edit.text(),
            "game_name": self.game_name_edit.text(),
            "desc": self.desc_edit.toPlainText()
        }


# ─────────────────────────────────────────────
#  DATA MANAGER  (unchanged)
# ─────────────────────────────────────────────
class DataManager:
    def __init__(self, base_path):
        self.csv_path = base_path
        self.dfs = {}
        self.types = {}
        self.file_map = {
            "Characters": {"logic": "characters.csv",    "spell": "spells_characters.csv"},
            "Buildings":  {"logic": "buildings.csv",     "spell": "spells_buildings.csv"},
            "Spells":     {"logic": "spells_other.csv",  "spell": "spells_other.csv"},
            "Projectiles":{"logic": "projectiles.csv",   "spell": None}
        }
        self.load_data()

    def load_data(self):
        files = ["characters.csv", "buildings.csv", "projectiles.csv",
                 "spells_characters.csv", "spells_buildings.csv", "spells_other.csv", "texts.csv"]
        for f in files:
            p = os.path.join(self.csv_path, f)
            if os.path.exists(p):
                try:
                    df = pd.read_csv(p, low_memory=False, header=None)
                    self.types[f] = df.iloc[1].tolist()
                    cols = df.iloc[0].tolist()
                    self.dfs[f] = df.iloc[2:].reset_index(drop=True)
                    self.dfs[f].columns = cols
                except: pass

    def get_col_type(self, filename, col_name):
        if filename not in self.dfs or filename not in self.types: return "string"
        try:
            idx = self.dfs[filename].columns.get_loc(col_name)
            return str(self.types[filename][idx]).lower()
        except: return "string"

    def get_safe_val(self, val):
        if pd.isna(val) or str(val).lower() == "nan": return ""
        return str(val)

    def get_text(self, tid, lang="EN"):
        if "texts.csv" not in self.dfs or not tid: return ""
        df = self.dfs["texts.csv"]
        row = df[df.iloc[:, 0] == tid]
        if not row.empty:
            val = row[lang].values[0] if lang in row.columns else row.iloc[0, 1]
            return self.get_safe_val(val)
        return ""

    def set_text(self, tid, text, lang="EN"):
        if "texts.csv" not in self.dfs or not tid: return
        df = self.dfs["texts.csv"]
        idx = df.index[df.iloc[:, 0] == tid].tolist()
        if idx:
            if lang in df.columns:
                df.at[idx[0], lang] = text

    def _generate_tid_info(self, tid, desc):
        if not desc: return ""
        if "TID_SPELL_" in tid: return tid.replace("TID_SPELL_", "TID_SPELL_INFO_")
        if "TID_" in tid: return tid.replace("TID_", "TID_INFO_")
        return f"TID_INFO_{tid}"

    def add_card_common(self, card_data, copy_source=None):
        cat = card_data['type']; name = card_data['name']
        tid = card_data['tid'];  game_name = card_data['game_name']
        desc = card_data['desc']
        if not name: return False
        tid_info = self._generate_tid_info(tid, desc)
        if "texts.csv" in self.dfs:
            text_df = self.dfs["texts.csv"]
            new_row_text = pd.Series([tid] + [game_name]*(len(text_df.columns)-1), index=text_df.columns)
            self.dfs["texts.csv"] = pd.concat([text_df, new_row_text.to_frame().T], ignore_index=True)
            if desc:
                new_row_desc = pd.Series([tid_info] + [desc]*(len(text_df.columns)-1), index=text_df.columns)
                self.dfs["texts.csv"] = pd.concat([self.dfs["texts.csv"], new_row_desc.to_frame().T], ignore_index=True)
        files = self.file_map[cat]
        if files['logic'] and files['logic'] in self.dfs:
            df = self.dfs[files['logic']]
            new_row = pd.Series(index=df.columns, dtype='object')
            if copy_source:
                src = df[df['Name'] == copy_source]
                if not src.empty: new_row = src.iloc[0].copy()
            new_row['Name'] = name
            if 'TID' in new_row.index: new_row['TID'] = tid
            self.dfs[files['logic']] = pd.concat([df, new_row.to_frame().T], ignore_index=True)
        if files['spell'] and files['spell'] in self.dfs:
            df = self.dfs[files['spell']]
            new_row = pd.Series(index=df.columns, dtype='object')
            if copy_source:
                src = df[df['Name'] == copy_source]
                if not src.empty: new_row = src.iloc[0].copy()
            new_row['Name'] = name
            if 'TID' in new_row.index: new_row['TID'] = tid
            if desc and 'TID_INFO' in new_row.index: new_row['TID_INFO'] = tid_info
            self.dfs[files['spell']] = pd.concat([df, new_row.to_frame().T], ignore_index=True)
        return True

    def add_new_card(self, data):   return self.add_card_common(data, copy_source=None)
    def duplicate_card(self, src, data): return self.add_card_common(data, copy_source=src)

    def delete_card(self, category, card_name):
        files = self.file_map.get(category)
        if not files: return False
        tids_to_remove = []
        if files['spell'] and files['spell'] in self.dfs:
            df = self.dfs[files['spell']]
            mask = df['Name'] == card_name
            for _, row in df[mask].iterrows():
                if 'TID' in row and pd.notnull(row['TID']): tids_to_remove.append(row['TID'])
                if 'TID_INFO' in row and pd.notnull(row['TID_INFO']): tids_to_remove.append(row['TID_INFO'])
            self.dfs[files['spell']] = df[~mask].reset_index(drop=True)
        if files['logic'] and files['logic'] in self.dfs:
            df = self.dfs[files['logic']]
            mask = df['Name'] == card_name
            if category == "Projectiles":
                for _, row in df[mask].iterrows():
                    if 'TID' in row and pd.notnull(row['TID']): tids_to_remove.append(row['TID'])
            self.dfs[files['logic']] = df[~mask].reset_index(drop=True)
        if "texts.csv" in self.dfs and tids_to_remove:
            df = self.dfs["texts.csv"]
            self.dfs["texts.csv"] = df[~df[df.columns[0]].isin(tids_to_remove)].reset_index(drop=True)
        return True

    def get_combined_data(self, category, card_name):
        data = {}
        files = self.file_map.get(category)
        if not files: return None
        if files['spell'] and files['spell'] in self.dfs:
            df_spell = self.dfs[files['spell']]
            rows = df_spell[df_spell['Name'] == card_name]
            if not rows.empty:
                data['spell'] = rows.iloc[0].to_dict()
                data['spell_idx'] = rows.index[0]
                data['spell_file'] = files['spell']
        if files['logic'] and files['logic'] in self.dfs:
            df_logic = self.dfs[files['logic']]
            rows = df_logic[df_logic['Name'] == card_name]
            if not rows.empty:
                data['logic'] = rows.iloc[0].to_dict()
                data['logic_idx'] = rows.index[0]
                data['logic_file'] = files['logic']
        return data

    def update_cell(self, filename, row_idx, col_name, value):
        if filename in self.dfs:
            self.dfs[filename].at[row_idx, col_name] = value

    def save_all(self):
        for filename, df in self.dfs.items():
            path = os.path.join(self.csv_path, filename)
            type_list = self.types[filename]
            with open(path, 'w', newline='', encoding='utf-8') as f:
                f.write(",".join([f'"{c}"' for c in df.columns]) + "\n")
                f.write(",".join([f'"{t}"' for t in type_list]) + "\n")
                for _, row in df.iterrows():
                    line = []
                    for i, val in enumerate(row):
                        col_type = str(type_list[i]).lower() if i < len(type_list) else "string"
                        if pd.isna(val) or str(val) == "" or str(val).lower() == "nan":
                            line.append("")
                        else:
                            s_val = str(val)
                            if "boolean" in col_type:
                                line.append('"true"' if s_val.lower() == "true" else "")
                            elif "int" in col_type and (s_val.isdigit() or (s_val.startswith('-') and s_val[1:].isdigit())):
                                line.append(s_val)
                            else:
                                line.append(f'"{s_val}"')
                    f.write(",".join(line) + "\n")


# ─────────────────────────────────────────────
#  CATEGORY PILL BUTTON
# ─────────────────────────────────────────────
class CategoryButton(QPushButton):
    def __init__(self, label: str, icon_key: str, color: str, parent=None):
        super().__init__(label, parent)
        self.color = color
        self.icon_key = icon_key
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setIconSize(QSize(15, 15))
        self._update_style(False)

    def _update_style(self, checked: bool):
        icon_color = self.color if checked else Theme.TEXT_MUTED
        self.setIcon(svg_icon(self.icon_key, 15, icon_color))
        if checked:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {self.color}1A;
                    color: {self.color};
                    border: 1px solid {self.color}55;
                    border-radius: 6px;
                    padding: 6px 10px 6px 8px;
                    font-weight: 700;
                    font-size: 12px;
                    text-align: left;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {Theme.TEXT_SECONDARY};
                    border: 1px solid transparent;
                    border-radius: 6px;
                    padding: 6px 10px 6px 8px;
                    font-weight: 500;
                    font-size: 12px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background: {Theme.BG_CARD};
                    color: {Theme.TEXT_PRIMARY};
                    border-color: {Theme.BORDER};
                }}
            """)

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._update_style(checked)


# ─────────────────────────────────────────────
#  CARD LIST ITEM  (with count badge)
# ─────────────────────────────────────────────
class StyledListItem(QListWidgetItem):
    def __init__(self, text, cat_color):
        super().__init__(text)
        self.setForeground(QColor(Theme.TEXT_PRIMARY))


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class CRCardEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nox CR Editor")
        self.resize(1520, 920)
        self.setMinimumSize(1100, 700)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_dir = os.path.join(base_dir, "csv")
        self.db = DataManager(self.csv_dir)

        self.current_cat = "Characters"
        self.current_card_name = None
        self.current_composite = None
        self._unsaved = False
        self._ui_ready = False  # guard: prevents signals firing before UI is complete

        # Status bar must exist BEFORE setup_ui() because tab signals fire during construction
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background: {Theme.BG_PANEL};
                color: {Theme.TEXT_SECONDARY};
                border-top: 1px solid {Theme.BORDER};
                font-size: 12px;
                padding: 2px 10px;
            }}
        """)
        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self._clear_status)

        self.setup_ui()
        self.setup_shortcuts()
        self._ui_ready = True
        self.populate_list()

        # Auto-select first item
        if self.card_list.count() > 0:
            self.card_list.setCurrentRow(0)
        self.flash_status("Ready — Nox CR Editor", timeout=0)

    # ──────────────────────────────────────────
    #  KEYBOARD SHORTCUTS
    # ──────────────────────────────────────────
    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.save_data)
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.open_add_dialog)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self.duplicate_current)
        QShortcut(QKeySequence("Delete"), self).activated.connect(self.delete_current_card)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(lambda: self.search_bar.setFocus())

    # ──────────────────────────────────────────
    #  UI SETUP
    # ──────────────────────────────────────────
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Left Rail (nav) ───────────────────
        rail = self._build_rail()
        root.addWidget(rail)

        # ── Vertical divider ─────────────────
        div = QFrame()
        div.setFrameShape(QFrame.VLine)
        div.setStyleSheet(f"color: {Theme.BORDER}; max-width: 1px;")
        root.addWidget(div)

        # ── Card List Panel ───────────────────
        list_panel = self._build_list_panel()
        root.addWidget(list_panel)

        # ── Vertical divider ─────────────────
        div2 = QFrame()
        div2.setFrameShape(QFrame.VLine)
        div2.setStyleSheet(f"color: {Theme.BORDER}; max-width: 1px;")
        root.addWidget(div2)

        # ── Editor Panel ──────────────────────
        editor = self._build_editor_panel()
        root.addWidget(editor, stretch=1)

        # Status bar was already created in __init__ before setup_ui()

    def _build_rail(self):
        rail = QWidget()
        rail.setFixedWidth(52)
        rail.setStyleSheet(f"background: {Theme.BG_PANEL}; border-right: 1px solid {Theme.BORDER};")
        layout = QVBoxLayout(rail)
        layout.setContentsMargins(7, 14, 7, 14)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignTop)

        # Logo — sword SVG
        logo_lbl = QLabel()
        logo_lbl.setPixmap(svg_pixmap("logo", 28, Theme.GOLD))
        logo_lbl.setAlignment(Qt.AlignCenter)
        logo_lbl.setStyleSheet("padding: 4px 0 12px 0; background: transparent;")
        layout.addWidget(logo_lbl)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet(f"background: {Theme.BORDER}; max-height: 1px; margin: 2px 4px;")
        layout.addWidget(divider)
        layout.addSpacing(6)

        tab_defs = [
            ("tab_info",   "Info & Texts    (tab 1)", 0),
            ("tab_all",    "All Attributes  (tab 2)", 1),
            ("tab_combat", "Combat Stats    (tab 3)", 2),
            ("tab_spawn",  "Spawn / Death   (tab 4)", 3),
            ("tab_icon",   "Icon Cropper    (tab 5)", 4),
        ]
        self._rail_btns = []
        for icon_key, tip, idx in tab_defs:
            btn = make_icon_btn(icon_key, tip, icon_color=Theme.TEXT_SECONDARY)
            btn.clicked.connect(lambda _, i=idx: self.main_tabs.setCurrentIndex(i))
            layout.addWidget(btn, alignment=Qt.AlignHCenter)
            self._rail_btns.append(btn)

        layout.addStretch()
        return rail

    # ─────────────────── Card List Panel ──────
    def _build_list_panel(self):
        panel = QWidget()
        panel.setFixedWidth(280)
        panel.setStyleSheet(f"background: {Theme.BG_PANEL};")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(8)

        # App title
        title_row = QHBoxLayout()
        app_lbl = QLabel("NOX CR")
        app_lbl.setStyleSheet(f"""
            color: {Theme.GOLD};
            font-size: 16px;
            font-weight: 800;
            letter-spacing: 2px;
        """)
        ver_lbl = QLabel("Editor")
        ver_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 12px; font-weight: 400;")
        title_row.addWidget(app_lbl)
        title_row.addWidget(ver_lbl)
        title_row.addStretch()
        layout.addLayout(title_row)
        layout.addWidget(separator())

        # Category pills
        layout.addWidget(section_label("Category"))
        cat_grid = QHBoxLayout()
        cat_grid.setSpacing(4)

        cats = [
            ("Characters",  "cat_chars",  Theme.CAT_CHARS),
            ("Buildings",   "cat_bldg",   Theme.CAT_BLDG),
            ("Spells",      "cat_spells", Theme.CAT_SPELL),
            ("Projectiles", "cat_proj",   Theme.CAT_PROJ),
        ]
        self._cat_btns = {}
        for cat_name, icon_key, color in cats:
            btn = CategoryButton(cat_name, icon_key, color)
            btn.clicked.connect(lambda _, c=cat_name: self._select_category(c))
            layout.addWidget(btn)
            self._cat_btns[cat_name] = btn
        self._cat_btns["Characters"].setChecked(True)

        layout.addWidget(separator())

        # Search
        layout.addWidget(section_label("Search"))
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search cards…  (Ctrl+F)")
        self.search_bar.textChanged.connect(self.filter_list)
        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background: {Theme.BG_INPUT};
                border: 1px solid {Theme.BORDER};
                border-radius: 7px;
                padding: 7px 10px 7px 32px;
                color: {Theme.TEXT_PRIMARY};
                font-size: 12px;
            }}
            QLineEdit:focus {{ border-color: {Theme.GOLD}; }}
        """)
        layout.addWidget(self.search_bar)

        # Card count badge
        self.list_count_lbl = QLabel("0 cards")
        self.list_count_lbl.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 11px; padding: 0 2px;")
        layout.addWidget(self.list_count_lbl)

        # Card List
        self.card_list = QListWidget()
        self.card_list.setAlternatingRowColors(False)
        self.card_list.currentItemChanged.connect(self.on_card_selected)
        layout.addWidget(self.card_list, stretch=1)

        # Action buttons
        layout.addWidget(separator())
        action_row = QHBoxLayout()
        action_row.setSpacing(6)

        self.add_btn = make_icon_btn("add",    "Add Card (Ctrl+N)",      icon_color=Theme.GREEN_ACT)
        self.add_btn.clicked.connect(self.open_add_dialog)

        self.dup_btn = make_icon_btn("dup",    "Duplicate Card (Ctrl+D)", icon_color=Theme.BLUE_ACT)
        self.dup_btn.setEnabled(False)
        self.dup_btn.clicked.connect(self.duplicate_current)

        self.del_btn = make_icon_btn("delete", "Delete Card (Del)",       icon_color=Theme.RED_ACT)
        self.del_btn.setEnabled(False)
        self.del_btn.clicked.connect(self.delete_current_card)

        action_row.addWidget(self.add_btn)
        action_row.addWidget(self.dup_btn)
        action_row.addWidget(self.del_btn)
        action_row.addStretch()

        save_btn_full = QPushButton("  Save All  (Ctrl+S)")
        save_btn_full.setIcon(svg_icon("save", 16, Theme.GREEN_ACT))
        save_btn_full.setIconSize(QSize(16, 16))
        save_btn_full.setStyleSheet(f"""
            QPushButton {{
                background: {Theme.BG_ELEVATED};
                color: {Theme.GREEN_ACT};
                border: 1px solid {Theme.GREEN_DIM};
                border-radius: 7px;
                padding: 9px 16px;
                font-weight: 700;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {Theme.GREEN_DIM};
                color: #ffffff;
                border-color: {Theme.GREEN_ACT};
            }}
            QPushButton:pressed {{ background: {Theme.GREEN_ACT}; color: #fff; }}
        """)
        save_btn_full.clicked.connect(self.save_data)
        layout.addLayout(action_row)
        layout.addWidget(save_btn_full)

        return panel

    # ─────────────────── Editor Panel ─────────
    def _build_editor_panel(self):
        panel = QWidget()
        panel.setStyleSheet(f"background: {Theme.BG_BASE};")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Card Header Bar ──────────────────
        self.card_header = self._build_card_header()
        layout.addWidget(self.card_header)

        # ── Attribute search strip ───────────
        search_strip = QWidget()
        search_strip.setStyleSheet(f"background: {Theme.BG_PANEL}; border-bottom: 1px solid {Theme.BORDER};")
        strip_layout = QHBoxLayout(search_strip)
        strip_layout.setContentsMargins(16, 8, 16, 8)

        srch_ico = QLabel()
        srch_ico.setPixmap(svg_pixmap("search", 15, Theme.TEXT_MUTED))
        srch_ico.setStyleSheet("background: transparent; padding: 0 2px;")
        self.attr_search_bar = QLineEdit()
        self.attr_search_bar.setPlaceholderText("Filter attributes in Combat / Spawn tabs…")
        self.attr_search_bar.textChanged.connect(self.filter_attributes)
        self.attr_search_bar.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                border: none;
                color: {Theme.TEXT_PRIMARY};
                font-size: 13px;
            }}
        """)
        strip_layout.addWidget(srch_ico)
        strip_layout.addWidget(self.attr_search_bar, stretch=1)
        layout.addWidget(search_strip)

        # ── Tabs ────────────────────────────
        self.main_tabs = QTabWidget()
        self.main_tabs.setStyleSheet(f"QTabWidget::pane {{ margin: 0; }}")
        self.main_tabs.currentChanged.connect(self._on_tab_changed)

        # Tab 0: Info & Texts
        self.tab_overview = QWidget()
        self.tab_overview.setStyleSheet(f"background: {Theme.BG_PANEL};")
        self.setup_overview_tab()
        self.main_tabs.addTab(self.tab_overview, "  Info & Texts")
        self.main_tabs.setTabIcon(0, svg_icon("tab_info", 16, Theme.TEXT_SECONDARY))

        # Tab 1: All Attributes
        self.tab_all = QScrollArea()
        self.tab_all.setWidgetResizable(True)
        self.ui_all = QWidget()
        self.ui_all.setStyleSheet(f"background: {Theme.BG_PANEL};")
        self.tab_all.setWidget(self.ui_all)
        self.all_layout = QVBoxLayout(self.ui_all)
        self.all_layout.setContentsMargins(16, 16, 16, 16)
        self.all_layout.setSpacing(12)
        self.all_layout.addStretch()
        self.main_tabs.addTab(self.tab_all, "  All Attributes")
        self.main_tabs.setTabIcon(1, svg_icon("tab_all", 16, Theme.TEXT_SECONDARY))

        # Tab 2: Combat
        self.tab_combat = QScrollArea()
        self.tab_combat.setWidgetResizable(True)
        self.ui_combat = QWidget()
        self.ui_combat.setStyleSheet(f"background: {Theme.BG_PANEL};")
        self.tab_combat.setWidget(self.ui_combat)
        self.combat_layout = QVBoxLayout(self.ui_combat)
        self.combat_layout.setContentsMargins(16, 16, 16, 16)
        self.combat_layout.setSpacing(12)
        self.combat_layout.addStretch()
        self.main_tabs.addTab(self.tab_combat, "  Combat")
        self.main_tabs.setTabIcon(2, svg_icon("tab_combat", 16, Theme.TEXT_SECONDARY))

        # Tab 3: Spawn / Death
        self.tab_deploy = QScrollArea()
        self.tab_deploy.setWidgetResizable(True)
        self.ui_deploy = QWidget()
        self.ui_deploy.setStyleSheet(f"background: {Theme.BG_PANEL};")
        self.tab_deploy.setWidget(self.ui_deploy)
        self.deploy_layout = QVBoxLayout(self.ui_deploy)
        self.deploy_layout.setContentsMargins(16, 16, 16, 16)
        self.deploy_layout.setSpacing(12)
        self.deploy_layout.addStretch()
        self.main_tabs.addTab(self.tab_deploy, "  Spawn / Death")
        self.main_tabs.setTabIcon(3, svg_icon("tab_spawn", 16, Theme.TEXT_SECONDARY))

        # Tab 4: Icon Cropper
        self.tab_image = self._build_image_tab()
        self.main_tabs.addTab(self.tab_image, "  Icon")
        self.main_tabs.setTabIcon(4, svg_icon("tab_icon", 16, Theme.TEXT_SECONDARY))

        # Size icons properly in tabs
        self.main_tabs.setIconSize(QSize(16, 16))

        layout.addWidget(self.main_tabs, stretch=1)
        return panel

    def _build_card_header(self):
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {Theme.BG_CARD}, stop:1 {Theme.BG_PANEL});
            border-bottom: 1px solid {Theme.BORDER};
        """)
        h = QHBoxLayout(header)
        h.setContentsMargins(20, 0, 20, 0)

        self.header_cat_pill = QLabel("—")
        self.header_cat_pill.setStyleSheet(f"""
            background: {Theme.BG_ELEVATED};
            color: {Theme.TEXT_MUTED};
            border-radius: 4px;
            padding: 3px 9px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
        """)
        self.header_card_name = QLabel("No card selected")
        self.header_card_name.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 18px;
            font-weight: 700;
        """)
        self.header_tid = QLabel("")
        self.header_tid.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 11px;")

        name_col = QVBoxLayout()
        name_col.setSpacing(1)
        name_col.addWidget(self.header_card_name)
        name_col.addWidget(self.header_tid)

        h.addWidget(self.header_cat_pill)
        h.addSpacing(12)
        h.addLayout(name_col)
        h.addStretch()

        # Unsaved dot
        self.unsaved_lbl = QLabel("● Unsaved changes")
        self.unsaved_lbl.setStyleSheet(f"color: {Theme.GOLD}; font-size: 11px; font-weight: 600;")
        self.unsaved_lbl.hide()
        h.addWidget(self.unsaved_lbl)

        return header

    def _build_image_tab(self):
        tab = QWidget()
        tab.setStyleSheet(f"background: {Theme.BG_PANEL};")
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Header
        hdr = QLabel("Icon Cropper  —  196 × 250 export")
        hdr.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px; font-weight: 600;")
        layout.addWidget(hdr)

        hint = QLabel("Drag an image onto the canvas, position the golden crop frame, then export.")
        hint.setStyleSheet(f"color: {Theme.TEXT_MUTED}; font-size: 11px;")
        layout.addWidget(hint)

        self.cropper = ImageCropper()
        layout.addWidget(self.cropper, stretch=1)

        btn_row = QHBoxLayout()
        btn_load = make_btn("  Load Image", Theme.BG_ELEVATED, Theme.BG_CARD)
        btn_load.setIcon(svg_icon("load", 16, Theme.TEXT_SECONDARY))
        btn_load.setIconSize(QSize(16, 16))
        btn_load.clicked.connect(self.import_img)
        btn_export = make_btn("  Export 196×250", Theme.GOLD, Theme.GOLD_DARK)
        btn_export.setIcon(svg_icon("export", 16, Theme.BG_BASE))
        btn_export.setIconSize(QSize(16, 16))
        btn_export.clicked.connect(self.export_img)
        btn_row.addWidget(btn_load)
        btn_row.addStretch()
        btn_row.addWidget(btn_export)
        layout.addLayout(btn_row)
        return tab

    # ──────────────────────────────────────────
    #  OVERVIEW TAB
    # ──────────────────────────────────────────
    def setup_overview_tab(self):
        layout = QHBoxLayout(self.tab_overview)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # ── Left: Texts column ────────────────
        left = QVBoxLayout()

        grp_text = QGroupBox("Localization")
        grp_text.setStyleSheet(f"QGroupBox {{ background: {Theme.BG_CARD}; }}")
        form_text = QFormLayout()
        form_text.setSpacing(10)
        form_text.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["EN", "FR", "DE", "ES", "IT", "RU", "JP", "KR", "CN"])
        self.lang_combo.currentIndexChanged.connect(self.refresh_texts)

        self.txt_tid_name = QLineEdit(); self.txt_tid_name.setReadOnly(True)
        self.txt_name_edit = QLineEdit()
        self.txt_name_edit.textChanged.connect(self.update_text_name)

        self.txt_tid_desc = QLineEdit(); self.txt_tid_desc.setReadOnly(True)
        self.txt_desc_edit = QTextEdit()
        self.txt_desc_edit.setMaximumHeight(90)
        self.txt_desc_edit.textChanged.connect(self.update_text_desc)

        def lbl(t): 
            l = QLabel(t)
            l.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px;")
            return l

        form_text.addRow(lbl("Language:"), self.lang_combo)
        form_text.addRow(lbl("Name TID:"), self.txt_tid_name)
        form_text.addRow(lbl("Name:"),     self.txt_name_edit)
        form_text.addRow(lbl("Desc TID:"), self.txt_tid_desc)
        form_text.addRow(lbl("Desc:"),     self.txt_desc_edit)
        grp_text.setLayout(form_text)
        left.addWidget(grp_text)
        left.addStretch()

        # ── Right: Meta properties ────────────
        right = QVBoxLayout()
        grp_meta = QGroupBox("Card Properties")
        grp_meta.setStyleSheet(f"QGroupBox {{ background: {Theme.BG_CARD}; }}")
        self.form_meta = QFormLayout()
        self.form_meta.setSpacing(10)
        self.form_meta.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grp_meta.setLayout(self.form_meta)
        right.addWidget(grp_meta)
        right.addStretch()

        layout.addLayout(left, stretch=1)
        layout.addLayout(right, stretch=1)

    # ──────────────────────────────────────────
    #  CATEGORY SELECTION
    # ──────────────────────────────────────────
    def _select_category(self, cat):
        self.current_cat = cat
        for name, btn in self._cat_btns.items():
            btn.setChecked(name == cat)
        self.populate_list()

    # ──────────────────────────────────────────
    #  CARD LIST POPULATION & FILTER
    # ──────────────────────────────────────────
    def populate_list(self):
        self.card_list.clear()
        target_file = self.db.file_map[self.current_cat]['spell']
        if not target_file:
            target_file = self.db.file_map[self.current_cat]['logic']
        color = Theme.cat_color(self.current_cat)
        if target_file and target_file in self.db.dfs:
            names = self.db.dfs[target_file]['Name'].astype(str).tolist()
            for name in names:
                item = StyledListItem(name, color)
                self.card_list.addItem(item)
        total = self.card_list.count()
        self.list_count_lbl.setText(f"{total} card{'s' if total != 1 else ''}")

    def filter_list(self):
        t = self.search_bar.text().lower()
        visible = 0
        for i in range(self.card_list.count()):
            it = self.card_list.item(i)
            match = t in it.text().lower()
            it.setHidden(not match)
            if match: visible += 1
        self.list_count_lbl.setText(f"{visible} card{'s' if visible != 1 else ''} shown")

    # ──────────────────────────────────────────
    #  CARD SELECTION
    # ──────────────────────────────────────────
    def on_card_selected(self, current, prev):
        if not current:
            self.dup_btn.setEnabled(False)
            self.del_btn.setEnabled(False)
            self.header_card_name.setText("No card selected")
            self.header_cat_pill.setText("—")
            self.header_tid.setText("")
            return
        self.dup_btn.setEnabled(True)
        self.del_btn.setEnabled(True)
        self.current_card_name = current.text()
        self.current_composite = self.db.get_combined_data(self.current_cat, self.current_card_name)
        if not self.current_composite: return

        # Update header
        color = Theme.cat_color(self.current_cat)
        self.header_cat_pill.setText(self.current_cat.upper())
        self.header_cat_pill.setStyleSheet(f"""
            background: {color}22;
            color: {color};
            border-radius: 4px;
            padding: 3px 9px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
        """)
        self.header_card_name.setText(self.current_card_name)
        spell = self.current_composite.get('spell', {})
        tid = self.db.get_safe_val(spell.get('TID', ''))
        self.header_tid.setText(tid)

        self.load_overview()
        self.load_dynamic_tabs()
        self.attr_search_bar.clear()

    # ──────────────────────────────────────────
    #  OVERVIEW / TEXTS LOAD
    # ──────────────────────────────────────────
    def load_overview(self):
        spell_data = self.current_composite.get('spell', {})
        self.txt_tid_name.setText(self.db.get_safe_val(spell_data.get('TID', '')))
        self.txt_tid_desc.setText(self.db.get_safe_val(spell_data.get('TID_INFO', '')))
        self.refresh_texts()

        # Clear meta form
        while self.form_meta.rowCount():
            self.form_meta.removeRow(0)

        key_meta = ['Rarity', 'ManaCost', 'UnlockArena', 'IconFile']
        if 'spell' in self.current_composite:
            filename = self.current_composite['spell_file']
            for k in key_meta:
                if k in spell_data:
                    col_type = self.db.get_col_type(filename, k)
                    val = self.db.get_safe_val(spell_data[k])
                    if "boolean" in col_type.lower():
                        w = QCheckBox()
                        w.setChecked(val.lower() == 'true')
                        w.toggled.connect(lambda v, c=k: self._on_data_changed('spell', c, str(v).lower()))
                    else:
                        w = QLineEdit(val)
                        w.textChanged.connect(lambda v, c=k: self._on_data_changed('spell', c, v))
                    lbl = QLabel(k)
                    lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px;")
                    self.form_meta.addRow(lbl, w)

    def refresh_texts(self):
        lang = self.lang_combo.currentText()
        self.txt_name_edit.blockSignals(True); self.txt_desc_edit.blockSignals(True)
        self.txt_name_edit.setText(self.db.get_text(self.txt_tid_name.text(), lang))
        self.txt_desc_edit.setText(self.db.get_text(self.txt_tid_desc.text(), lang))
        self.txt_name_edit.blockSignals(False); self.txt_desc_edit.blockSignals(False)

    def update_text_name(self, txt):
        self.db.set_text(self.txt_tid_name.text(), txt, self.lang_combo.currentText())
        self._mark_unsaved()

    def update_text_desc(self):
        self.db.set_text(self.txt_tid_desc.text(), self.txt_desc_edit.toPlainText(), self.lang_combo.currentText())
        self._mark_unsaved()

    # ──────────────────────────────────────────
    #  DYNAMIC COMBAT / SPAWN TABS
    # ──────────────────────────────────────────
    def load_dynamic_tabs(self):
        # Clear all three dynamic layouts (except trailing stretch)
        for layout in [self.combat_layout, self.deploy_layout, self.all_layout]:
            while layout.count() > 1:
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        if 'logic' not in self.current_composite: return
        logic_data = self.current_composite['logic']
        logic_file = self.current_composite['logic_file']

        groups = {
            "Combat":  ["Hitpoints", "Damage", "HitSpeed", "Speed", "Range",
                        "MinimumRange", "DamageSpecial", "AreaDamageRadius",
                        "TargetsAir", "TargetsGround"],
            "Deploy":  ["DeployTime", "SightRange", "CollisionRadius", "Mass", "Scale"],
            "Death":   ["DeathDamage", "DeathDamageRadius", "DeathEffect",
                        "DeathSpawnCharacter", "DeathSpawnCount"],
            "Summon":  ["SpawnCharacter", "SpawnNumber", "SpawnInterval", "SpawnLimit"]
        }
        processed = []

        # Group title → accent color for the "All" tab section headers
        group_colors = {
            "Combat Stats":      Theme.CAT_CHARS,
            "Deployment":        Theme.CAT_BLDG,
            "Death":             Theme.RED_ACT,
            "Summon":            Theme.CAT_SPELL,
            "Other Attributes":  Theme.TEXT_MUTED,
        }

        def make_widget(k, source):
            val = self.db.get_safe_val(logic_data[k])
            col_type = self.db.get_col_type(logic_file, k)
            if "boolean" in col_type.lower():
                w = QCheckBox()
                w.setChecked(val.lower() == 'true')
                w.toggled.connect(lambda v, c=k: self._on_data_changed(source, c, str(v).lower()))
            else:
                w = QLineEdit(val)
                w.textChanged.connect(lambda v, c=k: self._on_data_changed(source, c, v))
            return w

        def create_group(title, keys, target_layout, also_all=True):
            form_items = []
            for k in keys:
                if k in logic_data:
                    processed.append(k)
                    form_items.append((k, make_widget(k, 'logic')))
            if not form_items: return

            accent = group_colors.get(title, Theme.TEXT_MUTED)

            def _build_box(items):
                box = QGroupBox(title)
                box.setStyleSheet(f"""
                    QGroupBox {{
                        background: {Theme.BG_CARD};
                        border: 1px solid {accent}44;
                        border-radius: 8px;
                    }}
                    QGroupBox::title {{
                        color: {accent};
                        background: {Theme.BG_PANEL};
                    }}
                """)
                form = QFormLayout()
                form.setSpacing(9)
                form.setContentsMargins(12, 16, 12, 12)
                form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
                for key, widget in items:
                    lbl = QLabel(key)
                    lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px;")
                    form.addRow(lbl, widget)
                box.setLayout(form)
                return box

            box = _build_box(form_items)
            target_layout.insertWidget(target_layout.count() - 1, box)

            # Duplicate group into All tab with fresh widgets (independent signals)
            if also_all:
                all_items = []
                for k, _ in form_items:
                    all_items.append((k, make_widget(k, 'logic')))
                all_box = _build_box(all_items)
                self.all_layout.insertWidget(self.all_layout.count() - 1, all_box)

        create_group("Combat Stats",     groups["Combat"],  self.combat_layout)
        create_group("Deployment",       groups["Deploy"],  self.deploy_layout)
        create_group("Death",            groups["Death"],   self.deploy_layout)
        create_group("Summon",           groups["Summon"],  self.deploy_layout)

        others = [c for c in logic_data.keys() if c not in processed and c != "Name"]
        create_group("Other Attributes", others,            self.combat_layout)

    # ──────────────────────────────────────────
    #  ATTRIBUTE FILTER
    # ──────────────────────────────────────────
    def filter_attributes(self, text):
        text = text.lower()
        for layout in [self.combat_layout, self.deploy_layout, self.all_layout]:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if not item: continue
                group_box = item.widget()
                if not isinstance(group_box, QGroupBox): continue
                form = group_box.layout()
                group_visible = not text  # show all when empty
                if isinstance(form, QFormLayout) and text:
                    group_visible = False
                    for j in range(form.rowCount()):
                        label_item = form.itemAt(j, QFormLayout.LabelRole)
                        field_item = form.itemAt(j, QFormLayout.FieldRole)
                        if label_item and label_item.widget():
                            match = text in label_item.widget().text().lower()
                            form.setRowVisible(j, match)
                            if match: group_visible = True
                elif isinstance(form, QFormLayout):
                    for j in range(form.rowCount()):
                        form.setRowVisible(j, True)
                group_box.setVisible(group_visible)

    # ──────────────────────────────────────────
    #  DATA MUTATIONS
    # ──────────────────────────────────────────
    def _on_data_changed(self, source_type, col, val):
        if not self.current_composite or source_type not in self.current_composite: return
        self.db.update_cell(
            self.current_composite[f"{source_type}_file"],
            self.current_composite[f"{source_type}_idx"],
            col, val
        )
        self._mark_unsaved()

    def update_data(self, source_type, col, val):
        self._on_data_changed(source_type, col, val)

    # ──────────────────────────────────────────
    #  CARD CRUD
    # ──────────────────────────────────────────
    def open_add_dialog(self):
        dlg = AddCardDialog(self, is_duplicate=False)
        if dlg.exec():
            data = dlg.get_data()
            if self.db.add_new_card(data):
                self._select_category(data['type'])
                items = self.card_list.findItems(data['name'], Qt.MatchExactly)
                if items: self.card_list.setCurrentItem(items[0])
                self.flash_status(f"Card '{data['name']}' added successfully.")
                self._mark_unsaved()

    def duplicate_current(self):
        if not self.current_card_name: return
        dlg = AddCardDialog(self, is_duplicate=True, source_name=self.current_card_name)
        idx = dlg.type_combo.findText(self.current_cat)
        if idx >= 0: dlg.type_combo.setCurrentIndex(idx)
        if dlg.exec():
            data = dlg.get_data()
            if self.db.duplicate_card(self.current_card_name, data):
                self.populate_list()
                items = self.card_list.findItems(data['name'], Qt.MatchExactly)
                if items: self.card_list.setCurrentItem(items[0])
                self.flash_status(f"Duplicated: '{self.current_card_name}'  →  '{data['name']}'.")
                self._mark_unsaved()

    def delete_current_card(self):
        if not self.current_card_name: return
        reply = QMessageBox(self)
        reply.setWindowTitle("Confirm Deletion")
        reply.setText(f"<b>Delete '{self.current_card_name}'?</b>")
        reply.setInformativeText("This will remove all associated CSV rows and text entries. This cannot be undone.")
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        reply.setDefaultButton(QMessageBox.Cancel)
        reply.setStyleSheet(f"""
            QMessageBox {{ background: {Theme.BG_PANEL}; color: {Theme.TEXT_PRIMARY}; }}
            QLabel {{ color: {Theme.TEXT_PRIMARY}; }}
            QPushButton {{ 
                background: {Theme.BG_ELEVATED}; color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.BORDER}; border-radius: 6px; padding: 6px 16px;
                min-width: 70px;
            }}
            QPushButton:default {{ background: {Theme.RED_DIM}; border-color: {Theme.RED_ACT}; }}
        """)
        if reply.exec() == QMessageBox.Yes:
            name = self.current_card_name
            if self.db.delete_card(self.current_cat, name):
                self.populate_list()
                self.current_card_name = None
                self.dup_btn.setEnabled(False)
                self.del_btn.setEnabled(False)
                self.header_card_name.setText("No card selected")
                self.header_cat_pill.setText("—")
                self.header_tid.setText("")
                self.txt_name_edit.clear(); self.txt_desc_edit.clear()
                for layout in [self.combat_layout, self.deploy_layout, self.all_layout]:
                    while layout.count() > 1:
                        item = layout.takeAt(0)
                        if item.widget(): item.widget().deleteLater()
                self.flash_status(f"Deleted: card '{name}'.")
                self._mark_unsaved()

    # ──────────────────────────────────────────
    #  IMAGE IMPORT / EXPORT
    # ──────────────────────────────────────────
    def import_img(self):
        p, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if p: self.cropper.load_image(p)

    def export_img(self):
        img = self.cropper.get_cropped_image()
        if img:
            default = f"{self.current_card_name or 'icon'}.png"
            p, _ = QFileDialog.getSaveFileName(self, "Export Icon", default, "PNG (*.png)")
            if p:
                img.save(p)
                self.flash_status(f"Exported: {os.path.basename(p)}")

    # ──────────────────────────────────────────
    #  SAVE
    # ──────────────────────────────────────────
    def save_data(self):
        try:
            self.db.save_all()
            self._mark_saved()
            self.flash_status("Saved: all CSV files written successfully.", timeout=4000)
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save:\n{e}")

    # ──────────────────────────────────────────
    #  UNSAVED INDICATOR
    # ──────────────────────────────────────────
    def _mark_unsaved(self):
        if not self._unsaved:
            self._unsaved = True
            self.unsaved_lbl.show()
            self.setWindowTitle("Nox CR Editor  (unsaved changes)")

    def _mark_saved(self):
        self._unsaved = False
        self.unsaved_lbl.hide()
        self.setWindowTitle("Nox CR Editor")

    # ──────────────────────────────────────────
    #  STATUS BAR
    # ──────────────────────────────────────────
    def flash_status(self, msg, timeout=3500):
        self.status_bar.showMessage(msg)
        if timeout > 0:
            self._status_timer.start(timeout)

    def _clear_status(self):
        self.status_bar.showMessage("Ready")

    def _on_tab_changed(self, idx):
        if not self._ui_ready:
            return
        names = ["Info & Texts", "All Attributes", "Combat Stats", "Spawn / Death", "Icon Cropper"]
        if idx < len(names):
            self.flash_status(f"Tab: {names[idx]}", timeout=1500)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    Theme.apply(app)
    app.setStyleSheet(STYLESHEET)
    ex = CRCardEditor()
    ex.show()
    sys.exit(app.exec())
