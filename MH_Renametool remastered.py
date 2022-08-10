import maya.cmds as cmds
'''
    mhrename function will set a list to selection name 
    then if the selection is more than 1 object 
    will rename the items to mh rename mode then number of unit
'''
def mhrename():
    selection= cmds.ls(sl=True)
    if len(selection)<0:
        print("Make a selection to rename.")
    else:
     for obj in selection:
        cmds.rename(obj, "MH_Rename_Model_#")
mhrename()