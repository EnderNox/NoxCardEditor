# ⚔️ Nox CR Creator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green?style=for-the-badge&logo=qt)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

**Nox CR Creator** is a comprehensive, all-in-one tool designed for **Clash Royale Private Server** developers. It simplifies the process of creating, editing, and managing game assets by automatically linking logic files, spell definitions, and localization texts.

No more manual editing of misaligned CSV lines or broken TIDs!

---

## ✨ Features

* **🔗 Linked Data Editing**: Automatically connects `characters.csv` (Logic), `spells_characters.csv` (Meta), and `texts.csv` (Localization). Edit a card's HP and its description in the same window.
* **➕ Smart Card Creation**:
    * Wizard to add Characters, Buildings, Spells, or Projectiles.
    * **Auto-TID Generation**: Automatically generates `TID_SPELL_NAME` and `TID_SPELL_INFO_NAME` following Supercell's standards.
* **🖼️ Integrated Icon Editor**:
    * Built-in image cropper.
    * **Auto-Resize**: Automatically exports icons to the standard **196x250** format required by the game.
    * High-quality smooth scaling.
* **💾 Safe CSV Saving**:
    * Handles Supercell's specific CSV format (quoting strings vs integers).
    * Prevents server crashes due to malformatted data (handling of `NaN`, empty booleans, etc.).
* **🗑️ Clean Removal**: One-click button to remove a card from all linked CSV files simultaneously.
* **🌍 Multilingual Support**: Manage card names and descriptions for all supported languages (EN, FR, DE, etc.).

---

## 📸 Screenshots

---

## 🛠️ Installation

### Prerequisites
* Python 3.9 or higher
* pip

### Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YourUsername/NoxCRCreator.git](https://github.com/YourUsername/NoxCRCreator.git)
    cd NoxCRCreator
    ```

2.  **Install dependencies**
    ```bash
    pip install pandas PySide6
    ```

3.  **Prepare your CSV files**
    Create a folder named `csv` in the root directory and place your server files there. The structure **must** look like this:

    ```text
    NoxCRCreator/
    ├── NoxCardEditor.py
    ├── README.md
    └── csv/                 <-- Your server files go here
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
    python NoxCardEditor.py
    ```

---

## 🚀 Usage Guide

1.  **Select a Category**: Choose between Characters, Buildings, Spells, or Projectiles from the sidebar.
2.  **Edit a Card**: Click on any card in the list.
    * **Info & Texts Tab**: Edit the Name, TID, and Description (supports multiple languages).
    * **Combat Tab**: Edit HP, Damage, Hit Speed, Range, etc.
    * **Spawn/Death Tab**: Configure Death Effects, Spawned units (e.g., Witch skeletons), etc.
3.  **Create a New Card**: Click the **➕ Add Card** button.
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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---

## ⚠️ Disclaimer

This tool is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell's Fan Content Policy.
