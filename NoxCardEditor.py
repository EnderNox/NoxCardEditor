import sys
import os
import pandas as pd
import csv
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QScrollArea, QFormLayout, QLineEdit, QCheckBox, 
                             QPushButton, QLabel, QFileDialog, QComboBox, QTabWidget,
                             QGroupBox, QTextEdit, QDialog, QDialogButtonBox, QMessageBox)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QWheelEvent, QBrush, QFont
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsItem

# --- CROPPER IMAGE (UNCHANGED) ---
class ResizableRect(QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.setPen(QPen(QColor(255, 215, 0), 2))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.handle_size = 12
        self.ratio = 196 / 250
        self.is_resizing = False

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        painter.setBrush(QBrush(QColor(255, 215, 0)))
        r = self.rect()
        painter.drawRect(r.right() - self.handle_size, r.bottom() - self.handle_size, self.handle_size, self.handle_size)

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
        self.setBackgroundBrush(QColor(30, 30, 30))

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

# --- ADD CARD DIALOG (ENGLISH + FIXED TID LOGIC) ---
class AddCardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Card")
        self.resize(500, 400)
        self.layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Characters", "Buildings", "Spells", "Projectiles"])
        self.type_combo.currentIndexChanged.connect(self.on_type_change)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Ex: MegaKnight")
        self.name_edit.textChanged.connect(self.auto_fill)
        
        self.tid_edit = QLineEdit()
        self.tid_edit.setPlaceholderText("Ex: TID_SPELL_MEGA_KNIGHT")
        
        self.game_name_edit = QLineEdit()
        self.game_name_edit.setPlaceholderText("Ex: Mega Knight")
        
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("Card description...")
        self.desc_edit.setMaximumHeight(80)
        
        self.info_lbl = QLabel("")
        self.info_lbl.setStyleSheet("color: orange;")

        form.addRow("Type:", self.type_combo)
        form.addRow("Internal Name (ID):", self.name_edit)
        form.addRow("Text Key (TID):", self.tid_edit)
        form.addRow("In-Game Name:", self.game_name_edit)
        form.addRow("Description:", self.desc_edit)
        
        self.layout.addLayout(form)
        self.layout.addWidget(self.info_lbl)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)
        
        self.on_type_change()

    def on_type_change(self):
        t = self.type_combo.currentText()
        if t == "Projectiles":
            self.desc_edit.setEnabled(False)
            self.desc_edit.setPlaceholderText("No description for projectiles.")
            self.info_lbl.setText("⚠️ Note: Projectiles have no mana cost and no description.")
        else:
            self.desc_edit.setEnabled(True)
            self.desc_edit.setPlaceholderText("Card description...")
            self.info_lbl.setText("")

    def auto_fill(self, text):
        if not text: return
        clean = text.upper().replace(" ", "_")
        
        # --- FIXED TID LOGIC ---
        if self.type_combo.currentText() == "Projectiles":
             self.tid_edit.setText(f"{clean}") 
        else:
             self.tid_edit.setText(f"TID_SPELL_{clean}")
        
        # CamelCase Space Splitter
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

# --- DATA MANAGER (WITH DELETE FUNCTION) ---
class DataManager:
    def __init__(self, base_path):
        self.csv_path = base_path
        self.dfs = {}
        self.types = {}
        self.file_map = {
            "Characters": {"logic": "characters.csv", "spell": "spells_characters.csv"},
            "Buildings":  {"logic": "buildings.csv",  "spell": "spells_buildings.csv"},
            "Spells":     {"logic": "spells_other.csv", "spell": "spells_other.csv"},
            "Projectiles":{"logic": "projectiles.csv","spell": None}
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

    def add_new_card(self, card_data):
        cat = card_data['type']
        name = card_data['name']
        tid = card_data['tid']
        game_name = card_data['game_name']
        desc = card_data['desc']
        if not name: return False

        # --- TID GENERATION FIX ---
        # If TID matches standard format "TID_SPELL_XXX", Info should be "TID_SPELL_INFO_XXX"
        tid_info = ""
        if desc:
            if "TID_SPELL_" in tid:
                tid_info = tid.replace("TID_SPELL_", "TID_SPELL_INFO_")
            elif "TID_" in tid:
                tid_info = tid.replace("TID_", "TID_INFO_")
            else:
                tid_info = f"TID_INFO_{tid}"

        # 1. Texts
        if "texts.csv" in self.dfs:
            text_df = self.dfs["texts.csv"]
            new_row_text = pd.Series([tid] + [game_name]*(len(text_df.columns)-1), index=text_df.columns)
            self.dfs["texts.csv"] = pd.concat([text_df, new_row_text.to_frame().T], ignore_index=True)
            
            if desc:
                new_row_desc = pd.Series([tid_info] + [desc]*(len(text_df.columns)-1), index=text_df.columns)
                self.dfs["texts.csv"] = pd.concat([self.dfs["texts.csv"], new_row_desc.to_frame().T], ignore_index=True)

        # 2. Logic File
        files = self.file_map[cat]
        if files['logic'] and files['logic'] in self.dfs:
            logic_df = self.dfs[files['logic']]
            new_logic = pd.Series(index=logic_df.columns, dtype='object')
            new_logic['Name'] = name
            if 'TID' in new_logic.index: new_logic['TID'] = tid
            self.dfs[files['logic']] = pd.concat([logic_df, new_logic.to_frame().T], ignore_index=True)

        # 3. Spell File
        if files['spell'] and files['spell'] in self.dfs:
            spell_df = self.dfs[files['spell']]
            new_spell = pd.Series(index=spell_df.columns, dtype='object')
            new_spell['Name'] = name
            if 'TID' in new_spell.index: new_spell['TID'] = tid
            if desc and 'TID_INFO' in new_spell.index: new_spell['TID_INFO'] = tid_info
            self.dfs[files['spell']] = pd.concat([spell_df, new_spell.to_frame().T], ignore_index=True)
            
        return True

    def delete_card(self, category, card_name):
        """ Supprime la carte de la mémoire (Logic + Spell + Text) """
        files = self.file_map.get(category)
        if not files: return False
        
        tids_to_remove = []

        # 1. Delete from Spell File
        if files['spell'] and files['spell'] in self.dfs:
            df = self.dfs[files['spell']]
            # Find rows
            mask = df['Name'] == card_name
            rows = df[mask]
            
            # Capture TIDs before deleting
            for _, row in rows.iterrows():
                if 'TID' in row and pd.notnull(row['TID']): tids_to_remove.append(row['TID'])
                if 'TID_INFO' in row and pd.notnull(row['TID_INFO']): tids_to_remove.append(row['TID_INFO'])
            
            # Delete
            self.dfs[files['spell']] = df[~mask].reset_index(drop=True)

        # 2. Delete from Logic File
        if files['logic'] and files['logic'] in self.dfs:
            df = self.dfs[files['logic']]
            mask = df['Name'] == card_name
            
            # If Projectile (no spell file), capture TID here if exists
            if category == "Projectiles":
                rows = df[mask]
                for _, row in rows.iterrows():
                     # Projectiles don't usually have TID column, but just in case
                     if 'TID' in row and pd.notnull(row['TID']): tids_to_remove.append(row['TID'])

            self.dfs[files['logic']] = df[~mask].reset_index(drop=True)

        # 3. Delete from Texts
        if "texts.csv" in self.dfs and tids_to_remove:
            df = self.dfs["texts.csv"]
            # Column 0 is usually the TID key
            key_col = df.columns[0]
            self.dfs["texts.csv"] = df[~df[key_col].isin(tids_to_remove)].reset_index(drop=True)
            
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

        target_name = card_name 
        if files['logic'] and files['logic'] in self.dfs:
            df_logic = self.dfs[files['logic']]
            rows = df_logic[df_logic['Name'] == target_name]
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
                                if s_val.lower() == "true": line.append('"true"')
                                else: line.append("") 
                            elif "int" in col_type and (s_val.isdigit() or (s_val.startswith('-') and s_val[1:].isdigit())):
                                line.append(s_val)
                            else:
                                line.append(f'"{s_val}"')
                    f.write(",".join(line) + "\n")

# --- MAIN INTERFACE (TRANSLATED) ---
class CRCardEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nox CR Creator v2.4 (English)")
        self.resize(1400, 900)
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_dir = os.path.join(base_dir, "csv")
        self.db = DataManager(self.csv_dir)
        
        self.current_cat = "Characters"
        self.current_card_name = None
        self.current_composite = None
        
        self.setup_ui()
        self.populate_list()

    def setup_ui(self):
        main = QWidget()
        self.setCentralWidget(main)
        layout = QHBoxLayout(main)

        # Sidebar
        side_panel = QWidget()
        side_layout = QVBoxLayout(side_panel)
        side_panel.setFixedWidth(320)
        
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(["Characters", "Buildings", "Spells", "Projectiles"])
        self.cat_combo.currentIndexChanged.connect(self.change_category)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search...")
        self.search_bar.textChanged.connect(self.filter_list)
        
        self.card_list = QListWidget()
        self.card_list.currentItemChanged.connect(self.on_card_selected)
        
        # Buttons
        btn_layout = QVBoxLayout() # Vertical for more buttons
        
        row_add = QHBoxLayout()
        add_btn = QPushButton("➕ Add Card")
        add_btn.setStyleSheet("background-color: #1976D2; color: white; font-weight: bold; padding: 8px;")
        add_btn.clicked.connect(self.open_add_dialog)
        row_add.addWidget(add_btn)
        
        # --- REMOVE BUTTON ---
        self.del_btn = QPushButton("🗑️ Remove Card")
        self.del_btn.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; padding: 8px;")
        self.del_btn.setEnabled(False) # Disabled until selection
        self.del_btn.clicked.connect(self.delete_current_card)
        row_add.addWidget(self.del_btn)
        
        save_btn = QPushButton("💾 Save All CSVs")
        save_btn.setStyleSheet("background-color: #388E3C; color: white; font-weight: bold; padding: 12px;")
        save_btn.clicked.connect(self.save_data)
        
        btn_layout.addLayout(row_add)
        btn_layout.addWidget(save_btn)
        
        side_layout.addWidget(QLabel("Category:"))
        side_layout.addWidget(self.cat_combo)
        side_layout.addWidget(self.search_bar)
        side_layout.addWidget(self.card_list)
        side_layout.addLayout(btn_layout)
        
        layout.addWidget(side_panel)

        # Tabs
        self.main_tabs = QTabWidget()
        
        self.tab_overview = QWidget()
        self.ui_overview = self.setup_overview_tab()
        self.main_tabs.addTab(self.tab_overview, "📝 Info & Texts")

        self.tab_combat = QScrollArea()
        self.tab_combat.setWidgetResizable(True)
        self.ui_combat = QWidget()
        self.tab_combat.setWidget(self.ui_combat)
        self.combat_layout = QVBoxLayout(self.ui_combat)
        self.main_tabs.addTab(self.tab_combat, "⚔️ Combat")
        
        self.tab_deploy = QScrollArea()
        self.tab_deploy.setWidgetResizable(True)
        self.ui_deploy = QWidget()
        self.tab_deploy.setWidget(self.ui_deploy)
        self.deploy_layout = QVBoxLayout(self.ui_deploy)
        self.main_tabs.addTab(self.tab_deploy, "✨ Spawn/Death")

        self.tab_image = QWidget()
        img_layout = QVBoxLayout(self.tab_image)
        self.cropper = ImageCropper()
        ctrl_img = QHBoxLayout()
        btn_load = QPushButton("Load Image"); btn_load.clicked.connect(self.import_img)
        btn_save_icon = QPushButton("Export Icon"); btn_save_icon.clicked.connect(self.export_img)
        ctrl_img.addWidget(btn_load); ctrl_img.addWidget(btn_save_icon)
        img_layout.addWidget(QLabel("Drag & Drop | Scroll Zoom | Resize Yellow Corner"))
        img_layout.addWidget(self.cropper)
        img_layout.addLayout(ctrl_img)
        self.main_tabs.addTab(self.tab_image, "🖼️ Icon")
        
        layout.addWidget(self.main_tabs)

    def open_add_dialog(self):
        dlg = AddCardDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            if self.db.add_new_card(data):
                idx = self.cat_combo.findText(data['type'])
                if idx >= 0: self.cat_combo.setCurrentIndex(idx)
                self.populate_list()
                items = self.card_list.findItems(data['name'], Qt.MatchExactly)
                if items: self.card_list.setCurrentItem(items[0])
                QMessageBox.information(self, "Success", f"Card {data['name']} added!\nDon't forget to SAVE.")

    def delete_current_card(self):
        if not self.current_card_name: return
        
        reply = QMessageBox.question(self, 'Confirm Delete', 
                                     f"Are you sure you want to delete '{self.current_card_name}'?\nThis will remove it from Logic, Spells and Texts.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            success = self.db.delete_card(self.current_cat, self.current_card_name)
            if success:
                self.populate_list()
                self.current_card_name = None
                self.del_btn.setEnabled(False)
                # Clear UI
                self.txt_name_edit.clear()
                self.txt_desc_edit.clear()
                # Clear Dynamic Tabs
                for layout in [self.combat_layout, self.deploy_layout]:
                    while layout.count(): 
                        child = layout.takeAt(0)
                        if child.widget(): child.widget().deleteLater()
                
                QMessageBox.information(self, "Deleted", "Card removed from memory.\nClick SAVE to apply changes to files.")

    def setup_overview_tab(self):
        layout = QVBoxLayout(self.tab_overview)
        grp_text = QGroupBox("Texts (texts.csv)")
        form_text = QFormLayout()
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["EN", "FR", "DE", "ES", "IT", "RU", "JP", "KR", "CN"]) 
        self.lang_combo.currentIndexChanged.connect(self.refresh_texts)
        
        self.txt_tid_name = QLineEdit(); self.txt_tid_name.setReadOnly(True)
        self.txt_name_edit = QLineEdit()
        self.txt_name_edit.textChanged.connect(self.update_text_name)
        
        self.txt_tid_desc = QLineEdit(); self.txt_tid_desc.setReadOnly(True)
        self.txt_desc_edit = QTextEdit()
        self.txt_desc_edit.setMaximumHeight(80)
        self.txt_desc_edit.textChanged.connect(self.update_text_desc)
        
        form_text.addRow("Language:", self.lang_combo)
        form_text.addRow("Name Key:", self.txt_tid_name)
        form_text.addRow("In-Game Name:", self.txt_name_edit)
        form_text.addRow("Desc Key:", self.txt_tid_desc)
        form_text.addRow("Description:", self.txt_desc_edit)
        grp_text.setLayout(form_text)
        
        grp_meta = QGroupBox("Properties (spells.csv)")
        self.form_meta = QFormLayout()
        grp_meta.setLayout(self.form_meta)
        
        layout.addWidget(grp_text)
        layout.addWidget(grp_meta)
        layout.addStretch()

    def change_category(self):
        self.current_cat = self.cat_combo.currentText()
        self.populate_list()

    def populate_list(self):
        self.card_list.clear()
        target_file = self.db.file_map[self.current_cat]['spell']
        if not target_file: target_file = self.db.file_map[self.current_cat]['logic']
        
        if target_file and target_file in self.db.dfs:
            names = self.db.dfs[target_file]['Name'].astype(str).tolist()
            self.card_list.addItems(names)

    def filter_list(self):
        t = self.search_bar.text().lower()
        for i in range(self.card_list.count()):
            it = self.card_list.item(i)
            it.setHidden(t not in it.text().lower())

    def on_card_selected(self, current, prev):
        if not current: 
            self.del_btn.setEnabled(False)
            return
        
        self.del_btn.setEnabled(True)
        self.current_card_name = current.text()
        self.current_composite = self.db.get_combined_data(self.current_cat, self.current_card_name)
        if not self.current_composite: return
        self.load_overview()
        self.load_dynamic_tabs()

    def load_overview(self):
        spell_data = self.current_composite.get('spell', {})
        self.txt_tid_name.setText(self.db.get_safe_val(spell_data.get('TID', '')))
        self.txt_tid_desc.setText(self.db.get_safe_val(spell_data.get('TID_INFO', '')))
        self.refresh_texts() 
        while self.form_meta.count(): self.form_meta.takeAt(0).widget().deleteLater()
        
        key_meta = ['Rarity', 'ManaCost', 'UnlockArena', 'IconFile']
        if 'spell' in self.current_composite:
            for k in key_meta:
                if k in spell_data:
                    filename = self.current_composite['spell_file']
                    col_type = self.db.get_col_type(filename, k)
                    val = self.db.get_safe_val(spell_data[k])
                    if "boolean" in col_type.lower():
                        w = QCheckBox()
                        w.setChecked(val.lower() == 'true')
                        w.toggled.connect(lambda v, c=k: self.update_data('spell', c, str(v).lower()))
                    else:
                        w = QLineEdit(val)
                        w.textChanged.connect(lambda v, c=k: self.update_data('spell', c, v))
                    self.form_meta.addRow(k, w)

    def refresh_texts(self):
        lang = self.lang_combo.currentText()
        tid_n = self.txt_tid_name.text()
        tid_d = self.txt_tid_desc.text()
        self.txt_name_edit.blockSignals(True)
        self.txt_desc_edit.blockSignals(True)
        self.txt_name_edit.setText(self.db.get_text(tid_n, lang))
        self.txt_desc_edit.setText(self.db.get_text(tid_d, lang))
        self.txt_name_edit.blockSignals(False)
        self.txt_desc_edit.blockSignals(False)

    def update_text_name(self, txt):
        self.db.set_text(self.txt_tid_name.text(), txt, self.lang_combo.currentText())

    def update_text_desc(self):
        self.db.set_text(self.txt_tid_desc.text(), self.txt_desc_edit.toPlainText(), self.lang_combo.currentText())

    def load_dynamic_tabs(self):
        for layout in [self.combat_layout, self.deploy_layout]:
            while layout.count(): 
                child = layout.takeAt(0)
                if child.widget(): child.widget().deleteLater()

        if 'logic' not in self.current_composite: return
        logic_data = self.current_composite['logic']
        logic_file = self.current_composite['logic_file']
        
        groups = {
            "Combat": ["Hitpoints", "Damage", "HitSpeed", "Speed", "Range", "MinimumRange", "DamageSpecial", "AreaDamageRadius", "TargetsAir", "TargetsGround"],
            "Deploy": ["DeployTime", "SightRange", "CollisionRadius", "Mass", "Scale"],
            "Death": ["DeathDamage", "DeathDamageRadius", "DeathEffect", "DeathSpawnCharacter", "DeathSpawnCount"],
            "Summon": ["SpawnCharacter", "SpawnNumber", "SpawnInterval", "SpawnLimit"]
        }
        all_cols = list(logic_data.keys())
        processed = []
        
        def create_group(title, keys, target_layout):
            box = QGroupBox(title)
            form = QFormLayout()
            added = False
            for k in keys:
                if k in logic_data:
                    processed.append(k)
                    val = self.db.get_safe_val(logic_data[k])
                    col_type = self.db.get_col_type(logic_file, k)
                    
                    if "boolean" in col_type.lower():
                        w = QCheckBox()
                        w.setChecked(val.lower() == 'true')
                        w.toggled.connect(lambda v, c=k: self.update_data('logic', c, str(v).lower()))
                    else:
                        w = QLineEdit(val)
                        w.textChanged.connect(lambda v, c=k: self.update_data('logic', c, v))
                    form.addRow(k, w)
                    added = True
            box.setLayout(form)
            if added: target_layout.addWidget(box)

        create_group("Combat Stats", groups["Combat"], self.combat_layout)
        create_group("Deployment", groups["Deploy"], self.deploy_layout)
        create_group("Death", groups["Death"], self.deploy_layout)
        create_group("Summon", groups["Summon"], self.deploy_layout)
        others = [c for c in all_cols if c not in processed and c != "Name"]
        create_group("Others", others, self.combat_layout)

    def update_data(self, source_type, col, val):
        if not self.current_composite or source_type not in self.current_composite: return
        self.db.update_cell(self.current_composite[f"{source_type}_file"], 
                            self.current_composite[f"{source_type}_idx"], col, val)

    def import_img(self):
        p, _ = QFileDialog.getOpenFileName(self, "Image", "", "Images (*.png *.jpg)")
        if p: self.cropper.load_image(p)

    def export_img(self):
        img = self.cropper.get_cropped_image()
        if img:
            p, _ = QFileDialog.getSaveFileName(self, "Save Icon", f"{self.current_card_name or 'icon'}.png", "PNG (*.png)")
            if p: img.save(p)

    def save_data(self):
        self.db.save_all()
        QMessageBox.information(self, "Save", "All CSV files have been updated successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = CRCardEditor()
    ex.show()
    sys.exit(app.exec())