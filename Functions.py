import maya.cmds as cmds
import maya.OpenMaya as om
#-------------------------------------------------------------------
def matcher():
    pc = cmds.parentConstraint(mo=0)
    cmds.delete(pc)
#-------------------------------------------------------------------
def deleteConst():
    selection = cmds.ls(sl=True)
    for i in selection:
        cmds.DeleteConstraints()
#-------------------------------------------------------------------
def defControl():
    grp = cmds.group(em=True, name="_ctrl_grp")
    ctrl = cmds.circle(name="_ctrl")
    loc_name = "_CTRL_LOC"
    loc = cmds.CreateLocator()
    cmds.rename(loc, loc_name)
    cmds.parent(ctrl, loc_name)
    cmds.parent(loc_name, grp)
    cmds.DeleteHistory(ctrl)
#-------------------------------------------------------------------
def make_ref():
    selection = cmds.ls(sl=True)
    for i in selection:
        cmds.setAttr("{}.overrideEnabled".format(i), 1)
        cmds.setAttr("{}.overrideDisplayType".format(i), 2)
#-------------------------------------------------------------------
def return_normal():
    selection = cmds.ls(sl=True)
    for i in selection:
        cmds.setAttr("{}.overrideEnabled".format(i), 1)
        cmds.setAttr("{}.overrideDisplayType".format(i), 0)
#-------------------------------------------------------------------
