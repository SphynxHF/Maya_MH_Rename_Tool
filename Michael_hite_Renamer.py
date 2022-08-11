import maya.cmds as cmds


class MhRenamer(object):
    def __init__(self):
        # This is a simple renamer tool that renames selected object to the name entered #

        """window Parameters"""
        self.window = "MhRenamer"
        self.title = "MH Renamer Tool"
        self.size = (200, 200)

        """delete the window if its already open"""
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        """create the window"""
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        cmds.columnLayout(adjustableColumn=True)
        cmds.separator(height=20)
        self.renameTo = cmds.textFieldGrp(label="Rename to: ")

        self.renameBtn = cmds.button(label="Rename Selection", command=self.rename)
        cmds.separator(height=20)
        cmds.showWindow()

    def rename(self, *args):
        name = cmds.textFieldGrp(self.renameTo, query=True, text=True)
        selection = cmds.ls(sl=True)
        if len(selection) < 1:
            cmds.error("Make a selection to rename.")
        else:
            for obj in selection:
                cmds.rename(obj, name)


window = MhRenamer()