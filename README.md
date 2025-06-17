# MH Renamer Tool for Autodesk Maya

A powerful, fully-featured renaming tool for Autodesk Maya written in Python using `maya.cmds`.

---

## 🚀 Features

- ✅ Rename selected objects
- ✅ Add prefix to names
- ✅ Auto-numbered suffix (_01, _02, etc.)
- ✅ Apply to entire hierarchy (children included)
- ✅ Remove duplicate suffixes (_1, _2, etc.)
- ✅ Search and Replace
- ✅ Preview new names before applying
- ✅ Persistent settings (remembers last used input)
- ✅ Save & Load presets
- ✅ Strip whitespace option
- ✅ Convert to lowercase option
- ✅ Safe grouped undo (Ctrl+Z supported)

---

## 📦 Installation

1. **Save the Script:**

   Save the Python file as `mh_renamer.py`

2. **Run in Maya Script Editor:**

   ```python
   exec(open("C:/Path/To/mh_renamer.py").read())  # Update to your path
   ```

   ✅ Works in Maya 2022+

3. **(Optional) Add to Shelf:**

   - Drag the above code into a custom shelf button.
   - Set an icon and tooltip for quick access.

---

## 📄 Usage

- Fill in the **Prefix** and **New Name** fields
- Enable any of the options:
  - Strip whitespace
  - Lowercase
  - Remove `_1`, `_2` suffixes
  - Apply to hierarchy
- Click **Rename Selection** to apply

### 🔍 Search & Replace

- Fill in the **Search** and **Replace** fields
- Select objects
- Click **Search & Replace**

### 👁 Preview

- Click **Preview** to see what the names will look like before applying changes

---

## 💾 Presets

- Save common renaming setups with **Save Preset**
- Load saved presets from the dropdown menu

Presets are stored using `optionVar`, persistent across sessions.

---

## 📁 File Structure

```
mh_renamer.py        # The main script
README.txt           # This file
```

---

## 🔧 Requirements

- Autodesk Maya (any version that supports Python 2.7 or 3.x)
- No external dependencies required

---

## 🧠 Author

**Sphynx**

Crafted with Maya users in mind — productivity meets polish.
