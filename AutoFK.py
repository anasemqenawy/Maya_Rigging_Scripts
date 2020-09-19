import sys
import math
import maya.cmds as cmds
#---------------------------------------------------------
def auto_fk(*args):
    ctrl = cmds.textField("name", query=True, text=True)
    has_parent = None
    selection = cmds.ls(sl=True)
    radio = cmds.radioCollection("Constraint_Type", query=True, select=True)
    mode = cmds.radioButton(radio, query=True, label=True)
    #---------------------------------------------------------
    for i in selection:
        grp = cmds.group(em=True, name ="{}_ctrl_grp".format(i))
        # if ctrl is not exist in the scene already
        if ctrl == None or cmds.objExists(ctrl)==False:
            ctrl = cmds.circle(name = "{}_ctrl".format(i), normal=(0,1,0), radius=2)[0]
        else:
            # duplicate it and rename it
            ctrl = cmds.duplicate(ctrl, name="{}_ctrl".format(i))[0]
        #---------------------------------------------------------
        loc_name = "{}_ctrl_loc".format(i)
        loc = cmds.CreateLocator()
        cmds.rename(loc, loc_name)
        pc_grp= cmds.parentConstraint(i,grp,mo=0)
        cmds.delete(pc_grp)
        pc_ctrl = cmds.parentConstraint(i,ctrl,mo=0)
        cmds.delete(pc_ctrl)
        pc_loc = cmds.parentConstraint(i,loc_name,mo=0)
        cmds.delete(pc_loc)
        cmds.parent(loc_name, grp)
        cmds.parent(ctrl, loc_name)
        cmds.DeleteHistory(ctrl)
        #---------------------------------------------------------
        if i is not None:
            if mode == "Parent":
                cmds.parentConstraint(ctrl, i, mo=1, name="{}_parentConst".format(i))
            elif mode == "Orient":
                cmds.orientConstraint(ctrl,i, mo=1, name="{}_orientConst".format(i))
        if has_parent is not None:
            cmds.parent(grp, has_parent)
        has_parent = ctrl
#-------------------------------------------------------------------
if __init__ == "main":
    auto_fk()
