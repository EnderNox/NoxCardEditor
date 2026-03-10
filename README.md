# Nox Card Editor

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green?style=for-the-badge&logo=qt)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

**Nox Card Editor** is a comprehensive, all-in-one tool designed for **Clash Royale Private Server** developers. It simplifies the process of creating, editing, and managing game assets by automatically linking logic files, spell definitions, and localization texts.

No more manual editing of misaligned CSV lines or broken TIDs!

---

## Core Features

* **Linked Data Editing:** Automatically connects `characters.csv` (Logic), `spells_characters.csv` (Meta), and `texts.csv` (Localization). Modifying a card updates all relevant files simultaneously.
* **Smart Card Operations:** * **Create:** Wizard to easily add new Characters, Buildings, Spells, or Projectiles.
* **Duplicate (V2):** Clone an existing card's stats to create a new one instantly.
* **Remove:** Safely delete a card and all its associated data across the database.
* **Auto-TIDs:** Automatically generates `TID_SPELL_NAME` and `TID_SPELL_INFO_NAME` to match Supercell's standards.

* **Advanced Search (V2):** Filter the card list or use the global attribute search to quickly locate specific stats (e.g., finding "Radius" or "HitSpeed" across hundreds of parameters).
* **Safe CSV Saving:** Strictly adheres to Supercell's specific CSV formatting rules (e.g., proper quoting for strings vs. integers, handling empty boolean fields) to ensure server stability.
* **Integrated Icon Cropper:** A built-in graphical tool to load, scale, and crop custom images. It locks to the required `196x250` aspect ratio and exports game-ready icons.
* **Multilingual Support:** View and edit card names and descriptions for all supported languages directly in the editor.

---

## 🛠️ Installation

### Prerequisites
* Python 3.9 or higher
* pip

### Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/EnderNox/NoxCardEditor
    cd NoxCardEditor
    ```

2.  **Install dependencies**
    ```bash
    pip install pandas PySide6
    ```

3. **Prepare your workspace**
Create a folder named `csv` in the directory and place your decrypted server's CSV files inside it. Your directory structure must look exactly like this:
```
NoxCardEditor/
├── NoxCardEditor.py      <-- Legacy version
├── NoxCardEditorV2.py    <-- V2 version (Recommended)
└── csv/                  <-- Drop your server files here
    ├── buildings.csv
    ├── characters.csv
    ├── projectiles.csv
    ├── spells_buildings.csv
    ├── spells_characters.csv
    ├── spells_other.csv
    └── texts.csv

```

4.  **Run the tool**
    ```bash
    python NoxCardEditorV3.py
    ```
---

## Keyboard Shortcuts (V2)

To speed up your workflow, V2 includes the following shortcuts:

* `Ctrl + S`: Save all CSV files
* `Ctrl + N`: Add a new card
* `Ctrl + D`: Duplicate the currently selected card
* `Del`: Delete the currently selected card
* `Ctrl + F`: Focus the card search bar

---

## Usage Guide

1.  **Select a Category**: Choose between Characters, Buildings, Spells, or Projectiles from the sidebar.
2.  **Edit a Card**: Click on any card in the list.
    * **Info & Texts Tab**: Edit the Name, TID, and Description (supports multiple languages).
    * **all attributes tab**: Edit everything.
    * **Combat Tab**: Edit HP, Damage, Hit Speed, Range, etc.
    * **Spawn/Death Tab**: Configure Death Effects, Spawned units (e.g., Witch skeletons), etc.
3.  **Create a New Card**: Click the **➕** button.
    * Select the type.
    * Enter the Internal Name (e.g., `MegaKnight`).
    * The tool auto-fills the TIDs.
    * Click OK.
4.  **Card Icon**: Go to the **Image** tab.
    * Load any image (PNG/JPG).
    * Zoom and move the image.
    * Resize the **Yellow Box** (it locks to the correct aspect ratio).
    * Click **Export Icon**.
5.  **Save**: Click **💾 Save All CSVs** to write changes to disk.

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---

## ⚠️ Disclaimer

This tool is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell's Fan Content Policy.
