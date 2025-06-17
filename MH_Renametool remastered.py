import maya.cmds as cmds
import re
import json

class MhRenamer:
    def __init__(self):
        self.window_name = "MhRenamerWindow"
        self.settings_prefix = "MH_RENAMER_SETTINGS"
        self.presets_var = "MH_RENAMER_PRESETS"

        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

        self.window = cmds.window(self.window_name, title="MH Renamer Tool", widthHeight=(370, 400))
        cmds.columnLayout(adjustableColumn=True, rowSpacing=8)

        # Presets section
        cmds.frameLayout(label="Presets", collapsable=True, collapse=True, marginWidth=10)
        self.preset_menu = cmds.optionMenu(label="Preset:")
        self.refresh_presets()
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(label="Save Preset", command=self.save_current_preset)
        cmds.button(label="Load Preset", command=self.load_selected_preset)
        cmds.setParent("..")
        cmds.setParent("..")

        # Rename options
        cmds.frameLayout(label="Rename Options", collapsable=True, collapse=False, marginWidth=10)
        self.prefix_field = cmds.textFieldGrp(label="Prefix:", columnWidth=[(1, 80), (2, 220)])
        self.rename_field = cmds.textFieldGrp(label="New Name:", columnWidth=[(1, 80), (2, 220)])
        self.clean_duplicates = cmds.checkBox(label="Remove duplicate suffixes (_1, _2, etc)", value=True)
        self.rename_hierarchy = cmds.checkBox(label="Apply to entire hierarchy (children too)", value=False)
        self.strip_whitespace = cmds.checkBox(label="Strip whitespace", value=True)
        self.make_lowercase = cmds.checkBox(label="Convert to lowercase", value=False)
        cmds.setParent("..")

        # Search & Replace
        cmds.frameLayout(label="Search & Replace", collapsable=True, collapse=True, marginWidth=10)
        self.search_field = cmds.textFieldGrp(label="Search:", columnWidth=[(1, 80), (2, 220)])
        self.replace_field = cmds.textFieldGrp(label="Replace:", columnWidth=[(1, 80), (2, 220)])
        cmds.setParent("..")

        # Buttons
        cmds.separator(height=10)
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.button(label="Preview", width=100, command=self.preview_renames)
        cmds.button(label="Rename Selection", width=150, command=self.rename_selection)
        cmds.button(label="Search & Replace", width=150, command=self.search_and_replace)
        cmds.setParent("..")

        self.load_settings()
        cmds.showWindow(self.window)

    # -------- Settings and Presets --------

    def get_setting(self, key, default=''):
        option_key = f"{self.settings_prefix}_{key}"
        if cmds.optionVar(exists=option_key):
            return cmds.optionVar(q=option_key)
        return default

    def save_setting(self, key, value):
        cmds.optionVar(sv=(f"{self.settings_prefix}_{key}", value))

    def load_settings(self):
        cmds.textFieldGrp(self.prefix_field, edit=True, text=self.get_setting('prefix'))
        cmds.textFieldGrp(self.rename_field, edit=True, text=self.get_setting('rename'))
        cmds.checkBox(self.clean_duplicates, edit=True, value=bool(int(self.get_setting('clean', '1'))))
        cmds.checkBox(self.rename_hierarchy, edit=True, value=bool(int(self.get_setting('hierarchy', '0'))))
        cmds.checkBox(self.strip_whitespace, edit=True, value=bool(int(self.get_setting('stripws', '1'))))
        cmds.checkBox(self.make_lowercase, edit=True, value=bool(int(self.get_setting('lowercase', '0'))))

    def save_all_settings(self):
        self.save_setting('prefix', cmds.textFieldGrp(self.prefix_field, q=True, text=True))
        self.save_setting('rename', cmds.textFieldGrp(self.rename_field, q=True, text=True))
        self.save_setting('clean', str(int(cmds.checkBox(self.clean_duplicates, q=True, value=True))))
        self.save_setting('hierarchy', str(int(cmds.checkBox(self.rename_hierarchy, q=True, value=True))))
        self.save_setting('stripws', str(int(cmds.checkBox(self.strip_whitespace, q=True, value=True))))
        self.save_setting('lowercase', str(int(cmds.checkBox(self.make_lowercase, q=True, value=True))))

    def refresh_presets(self):
        if cmds.optionVar(exists=self.presets_var):
            try:
                presets = json.loads(cmds.optionVar(q=self.presets_var))
                cmds.optionMenu(self.preset_menu, e=True, deleteAllItems=True)
                for name in presets.keys():
                    cmds.menuItem(label=name, parent=self.preset_menu)
            except:
                cmds.warning("Could not read presets.")
        else:
            cmds.optionVar(sv=(self.presets_var, json.dumps({})))

    def save_current_preset(self, *args):
        name = cmds.promptDialog(title="Save Preset", message="Preset Name:", button=["OK", "Cancel"], defaultButton="OK", cancelButton="Cancel", dismissString="Cancel")
        if name == "OK":
            preset_name = cmds.promptDialog(query=True, text=True).strip()
            if not preset_name:
                return

            preset_data = {
                'prefix': cmds.textFieldGrp(self.prefix_field, q=True, text=True),
                'rename': cmds.textFieldGrp(self.rename_field, q=True, text=True),
                'clean': int(cmds.checkBox(self.clean_duplicates, q=True, value=True)),
                'hierarchy': int(cmds.checkBox(self.rename_hierarchy, q=True, value=True)),
                'stripws': int(cmds.checkBox(self.strip_whitespace, q=True, value=True)),
                'lowercase': int(cmds.checkBox(self.make_lowercase, q=True, value=True)),
            }

            all_presets = json.loads(cmds.optionVar(q=self.presets_var))
            all_presets[preset_name] = preset_data
            cmds.optionVar(sv=(self.presets_var, json.dumps(all_presets)))
            self.refresh_presets()

    def load_selected_preset(self, *args):
        selected = cmds.optionMenu(self.preset_menu, q=True, value=True)
        all_presets = json.loads(cmds.optionVar(q=self.presets_var))
        if selected in all_presets:
            p = all_presets[selected]
            cmds.textFieldGrp(self.prefix_field, e=True, text=p.get('prefix', ''))
            cmds.textFieldGrp(self.rename_field, e=True, text=p.get('rename', ''))
            cmds.checkBox(self.clean_duplicates, e=True, value=bool(p.get('clean', 1)))
            cmds.checkBox(self.rename_hierarchy, e=True, value=bool(p.get('hierarchy', 0)))
            cmds.checkBox(self.strip_whitespace, e=True, value=bool(p.get('stripws', 1)))
            cmds.checkBox(self.make_lowercase, e=True, value=bool(p.get('lowercase', 0)))

    # -------- Core Renaming Functions --------

    def apply_filters(self, name):
        if cmds.checkBox(self.strip_whitespace, q=True, value=True):
            name = name.replace(" ", "")
        if cmds.checkBox(self.make_lowercase, q=True, value=True):
            name = name.lower()
        return name

    def rename_selection(self, *args):
        self.save_all_settings()

        prefix = self.apply_filters(cmds.textFieldGrp(self.prefix_field, q=True, text=True).strip())
        base_name = self.apply_filters(cmds.textFieldGrp(self.rename_field, q=True, text=True).strip())
        clean = cmds.checkBox(self.clean_duplicates, q=True, value=True)
        include_children = cmds.checkBox(self.rename_hierarchy, q=True, value=True)

        selection = cmds.ls(selection=True, long=True)
        if not selection:
            cmds.warning("Nothing selected.")
            return
        if not base_name:
            cmds.warning("Please enter a base name.")
            return

        if include_children:
            all_objs = []
            for obj in selection:
                all_objs += cmds.listRelatives(obj, allDescendents=True, fullPath=True) or []
                all_objs.append(obj)
            selection = sorted(set(all_objs), key=lambda x: x.count('|'))

        cmds.undoInfo(openChunk=True)
        try:
            for i, obj in enumerate(selection):
                new_name = f"{prefix}{base_name}_{str(i+1).zfill(2)}" if len(selection) > 1 else f"{prefix}{base_name}"
                try:
                    renamed = cmds.rename(obj, new_name)
                    if clean:
                        cleaned = self.remove_duplicate_suffix(renamed)
                        if cleaned != renamed:
                            cmds.rename(renamed, cleaned)
                except Exception as e:
                    cmds.warning(f"Rename failed for {obj}: {e}")
        finally:
            cmds.undoInfo(closeChunk=True)

    def preview_renames(self, *args):
        prefix = self.apply_filters(cmds.textFieldGrp(self.prefix_field, q=True, text=True).strip())
        base_name = self.apply_filters(cmds.textFieldGrp(self.rename_field, q=True, text=True).strip())
        include_children = cmds.checkBox(self.rename_hierarchy, q=True, value=True)

        selection = cmds.ls(selection=True, long=True)
        if not selection or not base_name:
            cmds.warning("Selection or name missing.")
            return

        if include_children:
            all_objs = []
            for obj in selection:
                all_objs += cmds.listRelatives(obj, allDescendents=True, fullPath=True) or []
                all_objs.append(obj)
            selection = sorted(set(all_objs), key=lambda x: x.count('|'))

        preview_lines = []
        for i, obj in enumerate(selection):
            short = obj.split('|')[-1]
            new_name = f"{prefix}{base_name}_{str(i+1).zfill(2)}" if len(selection) > 1 else f"{prefix}{base_name}"
            preview_lines.append(f"{short} → {new_name}")

        if cmds.window("previewWin", exists=True):
            cmds.deleteUI("previewWin")
        cmds.window("previewWin", title="Rename Preview", widthHeight=(300, 300))
        cmds.scrollLayout()
        cmds.columnLayout(adjustableColumn=True)
        for line in preview_lines:
            cmds.text(label=line, align="left")
        cmds.showWindow("previewWin")

    def search_and_replace(self, *args):
        search = cmds.textFieldGrp(self.search_field, q=True, text=True)
        replace = cmds.textFieldGrp(self.replace_field, q=True, text=True)
        selection = cmds.ls(selection=True, long=True)

        if not selection or not search:
            cmds.warning("Selection or search term missing.")
            return

        cmds.undoInfo(openChunk=True)
        try:
            for obj in selection:
                short = obj.split('|')[-1]
                if search in short:
                    new_name = short.replace(search, replace)
                    new_name = self.apply_filters(new_name)
                    cmds.rename(obj, new_name)
        finally:
            cmds.undoInfo(closeChunk=True)

    def remove_duplicate_suffix(self, name):
        return re.sub(r"_\d+$", "", name)


# Launch
MhRenamer()